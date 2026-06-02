import os
import secrets
import sys
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

if getattr(sys, "frozen", False):
    BASE_DIR = Path(getattr(sys, "_MEIPASS"))
    default_data_dir = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "MustangRoundup"
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    default_data_dir = BASE_DIR

ROUNDUP_DATA_DIR = Path(os.environ.get("MUSTANGROUNDUP_DATA_DIR", default_data_dir))
ROUNDUP_DATA_DIR.mkdir(parents=True, exist_ok=True)

def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def env_csv(name, default):
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


def generated_secret_key():
    secret_path = ROUNDUP_DATA_DIR / "secret_key.txt"
    try:
        if secret_path.exists():
            existing = secret_path.read_text(encoding="utf-8").strip()
            if existing:
                return existing

        secret = secrets.token_urlsafe(64)
        secret_path.write_text(secret, encoding="utf-8")
        try:
            secret_path.chmod(0o600)
        except OSError:
            pass
        return secret
    except OSError as exc:
        raise ImproperlyConfigured(
            "Set DJANGO_SECRET_KEY or provide a writable MUSTANGROUNDUP_DATA_DIR."
        ) from exc


IS_TESTING = "test" in sys.argv
IS_RUNSERVER = "runserver" in sys.argv
LOCAL_EVENT_MODE = env_bool(
    "MUSTANGROUNDUP_LOCAL_EVENT_MODE",
    getattr(sys, "frozen", False) or IS_RUNSERVER or IS_TESTING,
)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if LOCAL_EVENT_MODE:
        SECRET_KEY = generated_secret_key()
    else:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY is required unless MUSTANGROUNDUP_LOCAL_EVENT_MODE=1."
        )

DEBUG = env_bool("DJANGO_DEBUG", LOCAL_EVENT_MODE)
default_allowed_hosts = (
    "localhost,127.0.0.1,[::1],.local,*"
    if LOCAL_EVENT_MODE
    else "localhost,127.0.0.1,[::1]"
)
ALLOWED_HOSTS = env_csv("DJANGO_ALLOWED_HOSTS", default_allowed_hosts)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]


INSTALLED_APPS = [
    "mustangroundup.apps.MustangroundupConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mustangroundupsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

WSGI_APPLICATION = "mustangroundupsite.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SQLITE_PATH", ROUNDUP_DATA_DIR / "db.sqlite3"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "America/Los_Angeles")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets"] if (BASE_DIR / "assets").exists() else []
STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "dashboard"

SESSION_COOKIE_AGE = 60 * 60 * 12

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not LOCAL_EVENT_MODE)
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not LOCAL_EVENT_MODE)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not LOCAL_EVENT_MODE)
SECURE_HSTS_SECONDS = int(
    os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "0" if LOCAL_EVENT_MODE else "31536000")
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    False,
)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)
