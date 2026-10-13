"""Minimal, loopback-first settings for the scaffold and offline development."""

from __future__ import annotations

import os
import secrets
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _read_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ImproperlyConfigured(f"{name} must be a boolean value")


def _read_list(name: str, default: list[str]) -> list[str]:
    value = os.environ.get(name)
    if value is None:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


def _read_path(name: str, default: str) -> Path:
    value = Path(os.environ.get(name, default)).expanduser()
    return value.resolve() if value.is_absolute() else (BASE_DIR / value).resolve()


def _ensure_private_directory(path: Path) -> None:
    path.mkdir(parents=True, mode=0o700, exist_ok=True)
    if path.stat().st_mode & 0o077:
        raise ImproperlyConfigured(f"{path} must be private to the current user")


APP_ENV = os.environ.get("CAREER_HELPER_ENV", "development").strip().lower()
if APP_ENV not in {"development", "test", "production"}:
    raise ImproperlyConfigured("CAREER_HELPER_ENV must be development, test, or production")

DEBUG = _read_bool("CAREER_HELPER_DEBUG", APP_ENV == "development")
SECRET_KEY = os.environ.get("CAREER_HELPER_SECRET_KEY", "").strip()
if not SECRET_KEY:
    if DEBUG and APP_ENV == "development":
        # Development sessions are intentionally invalidated when the process restarts.
        SECRET_KEY = secrets.token_urlsafe(48)
    else:
        raise ImproperlyConfigured("CAREER_HELPER_SECRET_KEY is required outside local development")

ALLOWED_HOSTS = _read_list(
    "CAREER_HELPER_ALLOWED_HOSTS", ["localhost", "127.0.0.1", "[::1]"]
)
DATA_ROOT = _read_path("CAREER_HELPER_DATA_ROOT", ".local/dev-synthetic")
TEST_DATA_ROOT = _read_path("CAREER_HELPER_TEST_DATA_ROOT", ".local/test")
_ensure_private_directory(DATA_ROOT)
FIXTURE_MODE = _read_bool("CAREER_HELPER_FIXTURE_MODE", True)
EXTERNAL_NETWORK_ENABLED = _read_bool("CAREER_HELPER_EXTERNAL_NETWORK_ENABLED", False)

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "career_helper.apps.CareerHelperConfig",
]

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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(DATA_ROOT / "career-helper.sqlite3"),
        "OPTIONS": {"timeout": 5},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = str(DATA_ROOT / "staticfiles")
MEDIA_ROOT = str(DATA_ROOT / "media")
FILE_UPLOAD_PERMISSIONS = 0o600
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
