"""
Django settings for Hello project.
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import config
import dj_database_url
import cloudinary
import cloudinary.uploader

BASE_DIR = Path(__file__).resolve().parent.parent

# ====================
# SECURITY SETTINGS
# ====================

SECRET_KEY = config('SECRET_KEY', default='django-insecure-render-deploy-fallback-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ON_RENDER = os.environ.get('RENDER') == 'true'

# ====================
# ALLOWED HOSTS - FIXED
# ====================

# Ensure ALLOWED_HOSTS is always a list
ALLOWED_HOSTS: list[str] = []

# Load from environment
allowed_hosts_env = config('ALLOWED_HOSTS', default='127.0.0.1,localhost')
if allowed_hosts_env and isinstance(allowed_hosts_env, str):
    ALLOWED_HOSTS = [host.strip() for host in str(allowed_hosts_env).split(',') if host.strip()]

# Safety: ensure it's a list
if not isinstance(ALLOWED_HOSTS, list):
    ALLOWED_HOSTS = [ALLOWED_HOSTS] if ALLOWED_HOSTS else []

# Add Render hostname
RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_HOSTNAME and isinstance(RENDER_HOSTNAME, str):
    if RENDER_HOSTNAME not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_HOSTNAME)

# Add localhost for development
if DEBUG:
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])

# ====================
# CSRF TRUSTED ORIGINS - FIXED
# ====================

# Start with empty list
CSRF_TRUSTED_ORIGINS: list[str] = []

# Load from environment
csrf_env = config('CSRF_TRUSTED_ORIGINS', default='')
if csrf_env and isinstance(csrf_env, str):
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in str(csrf_env).split(',') if origin.strip()]

# Safety: ensure it's a list
if not isinstance(CSRF_TRUSTED_ORIGINS, list):
    CSRF_TRUSTED_ORIGINS = [CSRF_TRUSTED_ORIGINS] if CSRF_TRUSTED_ORIGINS else []

# Add Render hostname
if RENDER_HOSTNAME and isinstance(RENDER_HOSTNAME, str):
    render_origin = f'https://{RENDER_HOSTNAME}'
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

# ====================
# INSTALLED APPS
# ====================

INSTALLED_APPS = [
    'home.apps.HomeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'cloudinary_storage',
    'cloudinary',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# ====================
# MIDDLEWARE
# ====================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Hello.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.category_choices',
                'home.context_processors.notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'Hello.wsgi.application'

# ====================
# DATABASE
# ====================

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=ON_RENDER and bool(config('DATABASE_URL', default='')),
    )
}

# ====================
# AUTHENTICATION
# ====================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# ====================
# SOCIAL ACCOUNT
# ====================

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
    }
}

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = True

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_METHODS = {'email', 'username'}

# ====================
# STATIC & MEDIA FILES
# ====================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====================
# CLOUDINARY
# ====================

CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default='')
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default='')
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default='')

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
    )

# ====================
# EMAIL
# ====================

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_BACKEND = (
    'django.core.mail.backends.smtp.EmailBackend'
    if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
    else 'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or 'noreply@example.com'

# ====================
# MESSAGE TAGS
# ====================

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ====================
# SECURITY (Production)
# ====================

if ON_RENDER:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True