# models.py
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
TEXT_LENGTH = 256


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=TEXT_LENGTH)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title  


class Location(BaseModel):
    name = models.CharField(max_length=TEXT_LENGTH)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=TEXT_LENGTH)
    text = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to="posts_images", blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_name="posts"
    )

    class Meta:
        ordering = ("-pub_date",)
        
    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField("Текст комментария")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        
    def __str__(self):
        return f"Комментарий от {self.author} к посту '{self.post.title[:50]}'"