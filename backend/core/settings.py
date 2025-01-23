"""
Django settings for core project.
"""
import os
from datetime import timedelta

from pathlib import Path
from decouple import AutoConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_file = str(Path(BASE_DIR).resolve() / '.env')

config = AutoConfig(search_path=env_file)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-wslg-eog)!d#nh2w+z@afx$v%h%!%fb!^u-1s*-9anm&c%^r7w'

DEBUG = True

ALLOWED_HOSTS = []


DJANGO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY = [
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'rest_framework_simplejwt',
    'drf_spectacular',
]

APPS = [
    'core',
    'plan_de_estudio',
    'planificadores',
    'pomodoro',
    'users',
    'visualizacion_grafo',
]

INSTALLED_APPS = DJANGO + THIRD_PARTY + APPS

SHELL_PLUS = "ipython"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    'Authorization',
    'Content-Type',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Origen de tu frontend
    "http://127.0.0.1:5173",  # Otra forma de referirse a localhost
]


ROOT_URLCONF = 'core.urls'

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

# WSGI_APPLICATION = 'core.wsgi.application'

ASGI_APPLICATION = 'core.asgi.application'

AUTH_USER_MODEL = 'users.Usuario'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'),
    'PAGE_SIZE': (10),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

with open(config('JWT_PUB_KEY', cast=str), 'r') as public_key_file:
    public_key = public_key_file.read()

with open(config('JWT_PRIVATE_KEY', cast=str), 'r') as private_key_file:
    private_key = private_key_file.read()

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'ALGORITHM': 'RS256',
    'VERIFYING_KEY': public_key,
    'SIGNING_KEY': private_key,

    'USER_ID_FIELD': 'id',
}


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s '
                      '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        }
    },
}
# API DOCS
SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': '',
    # 'SCHEMA_PATH_PREFIX_INSERT': 'back/',
    "USER_ID_CLAIM": "user_id",
    'TITLE': 'Estudiar API',
    'DESCRIPTION': 'Esquema de APIS de la app',
    'VERSION': config('API_VERSION', default='1.0.0'),
    'SERVE_INCLUDE_SCHEMA': True,
    "SWAGGER_UI_SETTINGS": {
        "displayRequestDuration": True,
        'persistAuthorization': True,
    },
}