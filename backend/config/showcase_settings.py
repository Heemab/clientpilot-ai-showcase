"""Loopback demo settings with a dedicated local SQLite database."""

from django.core.management.utils import get_random_secret_key

from .test_settings import *  # noqa: F403


DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SECRET_KEY = get_random_secret_key()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "showcase.sqlite3",
    }
}
