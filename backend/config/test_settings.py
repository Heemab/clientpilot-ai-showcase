"""Offline defaults for the showcase's isolated SQLite test suite."""

import os

from django.core.management.utils import get_random_secret_key


os.environ.setdefault("SECRET_KEY", get_random_secret_key())
os.environ.setdefault("DB_NAME", "unused")
os.environ.setdefault("DB_USER", "unused")
os.environ.setdefault("DB_PASSWORD", "unused")
os.environ.setdefault("DB_HOST", "127.0.0.1")
os.environ.setdefault("DB_PORT", "5432")

from .settings import *  # noqa: E402,F403


DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
SERPAPI_API_KEY = ""
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
STORAGES = {
    **STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
