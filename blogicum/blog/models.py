from django.contrib.auth import get_user_model
from django.db import models

from core.models import PublishedModel, CreatedModel  # базовые абстрактные модели

# Получаем модель пользователя Django
User = get_user_model()
# Константа для максимальной длины текстовых полей
TEXT_LENGTH = 256


class Category(PublishedModel, CreatedModel):
    # Название категории
    title = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name="Заголовок",
    )
    # Подробное описание категории
    description = models.TextField(
        verbose_name="Описание",
    )
    # Уникальный идентификатор для URL
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(PublishedModel, CreatedModel):
    # Название местоположения
    name = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name="Название места",
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(PublishedModel, CreatedModel):
    # Заголовок публикации
    title = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name="Заголовок",
    )
    # Основное содержимое поста
    text = models.TextField(
        verbose_name="Текст",
    )
    # Дата и время публикации (может быть установлена в будущем)
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    # Изображение для публикации (необязательное поле)
    image = models.ImageField(
        upload_to="posts_images",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    # Автор публикации (связь с моделью пользователя)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении автора удаляются его посты
        related_name="posts",
        verbose_name="Автор публикации",
    )
    # Местоположение (необязательное поле)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,  # При удалении местоположения поле становится NULL
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="Местоположение",
    )
    # Категория публикации
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # При удалении категории поле становится NULL
        null=True,
        related_name="posts",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title


class Comment(CreatedModel):
    # Текст комментария
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    # Публикация, к которой оставлен комментарий
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # При удалении поста удаляются все комментарии
        related_name="comments",
        verbose_name="Публикация",
    )
    # Автор комментария
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя удаляются его комментарии
        verbose_name="Автор комментария",
    )
    is_approved = models.BooleanField(
        default=False,  
        verbose_name="Одобрено",
        help_text="Одобрен ли комментарий модератором",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)  # Старые комментарии сначала

    def __str__(self):
        return f"Комментарий от {self.author} к посту «{self.post.title[:50]}»"