"""
Django settings for config project.

Gerado por 'django-admin startproject' usando Django 5.1.x.
"""

from pathlib import Path
import os

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Segurança / Debug (dev) ---
# Em produção, use variáveis de ambiente:
# os.environ.get("DJANGO_SECRET_KEY"), etc.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-unsafe-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# --- Apps ---
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Utilidades
    "django.contrib.humanize",
    # Suas apps
    "financas",  # <-- corrigido
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Pasta global de templates (ex.: BASE_DIR/templates)
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# --- Banco de dados (dev) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Validação de senhas ---
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internacionalização ---
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# --- Arquivos estáticos e de mídia ---
# Em dev:
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # onde ficam seus assets durante o dev
STATIC_ROOT = BASE_DIR / "staticfiles"  # coletados p/ prod (collectstatic)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Auth redirects (login pronto do Django) ---
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# --- Padrão de PK ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CoinMarketCap
COINMARKETCAP_API_KEY = os.environ.get(
    "CMC_API_KEY", "d1851e86-4cef-4731-b897-c29fd0dacfd8"
)
