from django.contrib import admin
from .models import Post, Category, Location, Comment

# Регистрация модели категорий с настройкой отображения
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')  # Поля, отображаемые в списке категорий
    prepopulated_fields = {'slug': ('title',)}  # Автозаполнение slug по названию
    list_filter = ('is_published',)  # Фильтр по полю публикации
    search_fields = ('title', 'description')  # Поля для поиска

# Регистрация модели местоположений
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')  # Отображаемые поля
    list_filter = ('is_published',)  # Фильтр по публикации
    search_fields = ('name',)  # Поле поиска

# Регистрация модели публикаций
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'location',
                    'is_published', 'pub_date', 'created_at')  # Отображаемые поля
    list_filter = ('is_published', 'category', 'location', 'author')  # Фильтры
    search_fields = ('title', 'text')  # Поля для поиска публикаций
    date_hierarchy = 'pub_date'  # Навигация по дате публикации

# Регистрация модели комментариев
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_at')  # Поля списка комментариев
    search_fields = ('author__username', 'text', 'post__title')  # Поля для поиска
    date_hierarchy = 'created_at'  # Навигация по дате добавления