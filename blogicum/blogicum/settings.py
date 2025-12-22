from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Корневая директория проекта

SECRET_KEY = "django-insecure-xn5)z4fdefk$^j!_&-!xukk-d@@eprv!nes2l_wp5f2=6_!l(a"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"  # Используем файловый бэкенд для писем
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"  # Папка для сохранения писем

MEDIA_ROOT = BASE_DIR / "media"  # Папка для загружаемых файлов
STATICFILES_DIRS = [BASE_DIR / "static"]  # Дополнительные папки со статикой

LOGIN_REDIRECT_URL = "blog:index"  # URL после входа
LOGIN_URL = "login"  # URL страницы входа
CSRF_FAILURE_VIEW = "pages.views.csrf_failure"  # Кастомная страница ошибки CSRF

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig", # Приложение core
    "blog.apps.BlogConfig",  # Приложение блога
    "pages.apps.PagesConfig",  # Приложение статических страниц
    "django_bootstrap5",  # Bootstrap для шаблонов
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blogicum.urls"
TEMPLATES_DIR = BASE_DIR / "templates"  # Директория с шаблонами

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "blogicum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # База данных SQLite
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"  # URL для статических файлов
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
