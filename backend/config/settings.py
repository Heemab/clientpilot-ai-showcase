"""
Django settings for AI Client Acquisition Engine.

Production-ready configuration for local development and Railway deployment.
"""

from pathlib import Path
import sys

import environ


# ==============================================================================
# Paths
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# AI Client Acquisition Engine
# ==============================================================================

ENGINE_DIR = BASE_DIR.parent / "engine"

if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))


# ==============================================================================
# Environment Variables
# ==============================================================================

env = environ.Env()

# Load .env file
environ.Env.read_env(BASE_DIR / ".env")


# ==============================================================================
# API Keys
# ==============================================================================

SERPAPI_API_KEY = env(
    "SERPAPI_API_KEY",
    default="",
)


# ==============================================================================
# Security
# ==============================================================================

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool(
    "DEBUG",
    default=False,
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
        "localhost",
    ],
)

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[],
)


# ==============================================================================
# Applications
# ==============================================================================

INSTALLED_APPS = [
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-Party Apps
    "rest_framework",

    # Local Apps
    "apps.accounts",
    "apps.organizations",
    "apps.dashboard",
    "apps.discovery",
    "apps.leads",
    "apps.audits",
    "apps.proposals",
    "apps.outreach",
    "apps.public",
    "apps.pipeline",
    "apps.crm_calendar",
]


# ==============================================================================
# Middleware
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================================
# URLs
# ==============================================================================

ROOT_URLCONF = "config.urls"


# ==============================================================================
# Templates
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==============================================================================
# WSGI
# ==============================================================================

WSGI_APPLICATION = "config.wsgi.application"


# ==============================================================================
# Database
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env.int("DB_PORT"),
    }
}


# ==============================================================================
# Password Validation
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ==============================================================================
# Internationalization
# ==============================================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# ==============================================================================
# Static Files
# ==============================================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": (
            "django.core.files.storage."
            "FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# ==============================================================================
# Media Files
# ==============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ==============================================================================
# Default Primary Key
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# Django REST Framework
# ==============================================================================

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}


# ==============================================================================
# Authentication
# ==============================================================================

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/dashboard/"

LOGOUT_REDIRECT_URL = "/"


# ==============================================================================
# Production Security
# ==============================================================================

if env.bool("TRUST_PROXY_SSL_HEADER", default=False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# ==============================================================================
# Email
# ==============================================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = env(
    "EMAIL_HOST",
    default="smtp.gmail.com",
)

# Gmail SMTP over SSL
EMAIL_PORT = env.int(
    "EMAIL_PORT",
    default=465,
)

EMAIL_USE_SSL = env.bool(
    "EMAIL_USE_SSL",
    default=True,
)

EMAIL_USE_TLS = env.bool(
    "EMAIL_USE_TLS",
    default=False,
)

EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
    default="",
)

EMAIL_HOST_PASSWORD = env(
    "EMAIL_HOST_PASSWORD",
    default="",
)

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default=EMAIL_HOST_USER,
)