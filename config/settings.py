"""
Django settings for config project.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# --- НАСТРОЙКА ПУТЕЙ ДЛЯ PYINSTALLER ---
if getattr(sys, 'frozen', False):
    # Если программа запущена как EXE
    BASE_DIR = Path(sys.executable).parent
    # Папка, куда PyInstaller распаковывает шаблоны и статику
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    # Если программа запущена из PyCharm
    BASE_DIR = Path(__file__).resolve().parent.parent
    BUNDLE_DIR = BASE_DIR

# Загружаем .env из папки с EXE-файлом (или из корня проекта)
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-key")

# Для EXE-программы лучше оставить DEBUG=True, чтобы Django отдавал ошибки
DEBUG = os.getenv("DEBUG", "True") == "True"

# Разрешаем подключение с локального компьютера
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Наши приложения
    "apps.accounts",
    "apps.directories",
    "apps.employees",
    "apps.contracts",
    "apps.vacations",
    "apps.notifications",
    "apps.events",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- WhiteNoise для статики в EXE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BUNDLE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Minsk"
USE_I18N = True
USE_TZ = True

# Форматы дат (ДД.ММ.ГГГГ)
DATE_FORMAT = "d.m.Y"
SHORT_DATE_FORMAT = "d.m.Y"
DATETIME_FORMAT = "d.m.Y H:i"
SHORT_DATETIME_FORMAT = "d.m.Y H:i"

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BUNDLE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Настройки WhiteNoise для раздачи статики в EXE
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Авторизация
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'