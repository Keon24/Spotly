import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")  # Fallback for dev
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'parking',
    'reservation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spotly.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spotly.wsgi.application'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_DB', 'spotly_db'),
        'USER': os.getenv('PG_USER', 'spotly_user'),
        'PASSWORD': os.getenv('PG_PASSWORD', 'securepassword'),
        'HOST': os.getenv('PG_HOST', 'spotly_postgres'),
        'PORT': os.getenv('PG_PORT', '5432'),
    }
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = 'static/'

# CUSTOM USER
AUTH_USER_MODEL = 'users.User'

# JWT AUTH
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# GOOGLE OAUTH (now secure)
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH2_CLIENT_SECRET")
GOOGLE_OAUTH2_REDIRECT_URI = os.getenv("GOOGLE_OAUTH2_REDIRECT_URI", "http://localhost:8000/auth/google/callback/")













