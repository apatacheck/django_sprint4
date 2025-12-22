from django.contrib.auth import get_user_model
from django.db import models

# Получаем модель пользователя Django
User = get_user_model()

# Константа для максимальной длины текстовых полей
TEXT_LENGTH = 256


class Category(models.Model):
    
    # Название категории
    title = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name="Заголовок категории"
    )
    
    # Подробное описание категории
    description = models.TextField(
        verbose_name="Описание категории"
    )
    
    # Уникальный идентификатор для URL 
    slug = models.SlugField(
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Используйте латинские буквы, цифры, дефисы и подчёркивания"
    )
    
    # Флаг видимости категории
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Отображать категорию на сайте"
    )
    
    # Автоматически устанавливаемая дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["title"]  # Сортировка по названию

    def __str__(self):
        return self.title


class Location(models.Model):
    
    # Название местоположения
    name = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name="Название места"
    )
    
    # Флаг видимости местоположения
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Отображать местоположение на сайте"
    )
    
    # Автоматически устанавливаемая дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "местоположения"
        ordering = ["name"]  # Сортировка по названию

    def __str__(self):
        return self.name


class Post(models.Model):
    
    # Заголовок публикации
    title = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name="Заголовок публикации"
    )
    
    # Основное содержимое поста
    text = models.TextField(
        verbose_name="Текст публикации"
    )
    
    # Дата и время публикации (может быть установлена в будущем)
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text="Установите будущую дату для отложенной публикации"
    )
    
    # Изображение для публикации (необязательное поле)
    image = models.ImageField(
        upload_to="posts_images/%Y/%m/%d/",  # Организация по папкам дат
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для публикации"
    )
    
    # Автор публикации (связь с моделью пользователя)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении автора удаляются его посты
        related_name="posts",
        verbose_name="Автор публикации"
    )
    
    # Местоположение (необязательное поле)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,  # При удалении местоположения поле становится NULL
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="Местоположение"
    )
    
    # Категория публикации
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # При удалении категории поле становится NULL
        null=True,
        related_name="posts",
        verbose_name="Категория"
    )
    
    # Флаг видимости публикации
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Отображать публикацию на сайте"
    )
    
    # Автоматически устанавливаемая дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "публикации"
        ordering = ["-pub_date"]  # Новые публикации сначала
        indexes = [
            models.Index(fields=["-pub_date", "is_published"]),
            models.Index(fields=["author", "is_published"]),
        ]

    def __str__(self):
        return self.title



class Comment(models.Model):
    
    # Текст комментария
    text = models.TextField(
        verbose_name="Текст комментария"
    )
    
    # Публикация, к которой оставлен комментарий
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # При удалении поста удаляются все комментарии
        related_name="comments",
        verbose_name="Публикация"
    )
    
    # Автор комментария
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя удаляются его комментарии
        related_name="comments",
        verbose_name="Автор комментария"
    )
    
    # Автоматически устанавливаемая дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    # Флаг одобрения комментария (новое поле для модерации)
    is_approved = models.BooleanField(
        default=True,
        verbose_name="Одобрен",
        help_text="Отображать комментарий на сайте"
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        ordering = ["created_at"]  # Старые комментарии сначала
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["author", "created_at"]),
        ]

    def __str__(self):
        post_title = self.post.title[:30] + "..." if len(self.post.title) > 30 else self.post.title
        return f"Комментарий от {self.author.username} к '{post_title}'"
    