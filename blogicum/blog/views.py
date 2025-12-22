from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post

User = get_user_model()  # Получение текущей модели пользователя
PAGINATE_BY = 10  # Количество публикаций на одной странице


class PostQuerysetMixin:
    # Миксин для получения queryset с выборкой связанных объектов и подсчетом комментариев
    def get_queryset(self):
        return Post.objects.select_related("category", "location", "author").annotate(
            comment_count=Count("comments")
        )


class PostListView(PostQuerysetMixin, ListView):
    template_name = "blog/index.html"  # Шаблон главной страницы
    context_object_name = "page_obj"  # Имя объекта в контексте
    paginate_by = PAGINATE_BY  # Пагинация

    def get_queryset(self):
        # Выбираем только опубликованные посты с опубликованными категориями
        return (
            super()
            .get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=datetime.now(),
            )
            .order_by("-pub_date")  # Сортировка по дате публикации
        )


class CategoryPostListView(PostQuerysetMixin, ListView):
    template_name = "blog/post_list.html"  # Шаблон страницы категории
    context_object_name = "page_obj"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        # Получаем категорию по slug
        self.category = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        # Фильтруем посты по выбранной категории
        return (
            super()
            .get_queryset()
            .filter(
                category=self.category,
                is_published=True,
                pub_date__lte=datetime.now(),
            )
            .order_by("-pub_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category  # Передаем категорию в шаблон
        return context


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = "post_id"  # Имя параметра в URL
    template_name = "blog/post_detail.html"

    def get_object(self):
        # Получаем пост, учитывая права доступа
        post = get_object_or_404(
            Post.objects.annotate(comment_count=Count("comments")),   
            id=self.kwargs["post_id"]
        )
        if self.request.user != post.author:
            post = get_object_or_404(
                Post,
                id=self.kwargs["post_id"],
                is_published=True,
                category__is_published=True,
                pub_date__lte=datetime.now(),
            )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()  # Форма для добавления комментария
        context["comments"] = Comment.objects.select_related("author").filter(
            post=self.object
        )  # Список комментариев к посту
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm  # Форма создания поста
    template_name = "blog/create.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user  # Устанавливаем автора поста
        post.save()
        return redirect("blog:profile", self.request.user.username)  # Переадресация на профиль


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = "post_id"
    template_name = "blog/create.html"

    def dispatch(self, request, *args, **kwargs):
        # Проверка, что пользователь является автором поста
        post = self.get_object()
        if post.author != request.user:
            return redirect("blog:post_detail", post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Переадресация на страницу отредактированного поста
        return reverse_lazy("blog:post_detail", kwargs={"post_id": self.object.id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = "post_id"
    template_name = "blog/create.html"
    success_url = reverse_lazy("blog:index")  # Переадресация после удаления

    def dispatch(self, request, *args, **kwargs):
        # Проверка прав на удаление
        post = self.get_object()
        if post.author != request.user:
            return redirect("blog:post_detail", post.id)
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm  # Форма для комментария

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        comment = form.save(commit=False)
        comment.author = self.request.user  # Автор комментария
        comment.post = post  # Связь с постом
        comment.save()
        return redirect("blog:post_detail", post.id)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:  # Проверка авторства комментария
            return redirect("blog:post_detail", comment.post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"post_id": self.object.post.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:  # Проверка авторства
            return redirect("blog:post_detail", comment.post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"post_id": self.object.post.id})


class UserProfileView(PostQuerysetMixin, ListView):
    template_name = "blog/profile.html"
    context_object_name = "page_obj"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        # Получаем пользователя профиля и фильтруем его посты
        self.profile_user = get_object_or_404(User, username=self.kwargs["username"])
        qs = super().get_queryset().filter(author=self.profile_user)

        if self.request.user != self.profile_user:
            qs = qs.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=datetime.now(),
            )
        return qs.order_by("-pub_date")  # Сортировка по дате публикации

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile_user  # Передаем пользователя в шаблон
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "blog/user.html"

    def get_object(self):
        return self.request.user  # Редактирование профиля текущего пользователя

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )  # Переадресация на профиль
