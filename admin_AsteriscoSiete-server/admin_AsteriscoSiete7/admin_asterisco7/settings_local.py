# -*- coding: utf-8 -*-
"""
settings_local.py — Configuración LOCAL para desarrollo sin infraestructura
===========================================================================
Anula las dependencias de producción (djcelery, Redis, RabbitMQ, opbeat)
para poder ejecutar manage.py makemigrations / migrate / runserver en Windows.

Uso:
    python manage.py makemigrations admin_juego --settings=admin_asterisco7.settings_local
    python manage.py migrate             --settings=admin_asterisco7.settings_local
    python manage.py runserver           --settings=admin_asterisco7.settings_local

O establece la variable de entorno de forma permanente:
    $env:DJANGO_SETTINGS_MODULE = "admin_asterisco7.settings_local"
"""
import os

# ── Omitimos settings.py principal para evitar djcelery / Redis / RabbitMQ ───
DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_TOOLBAR = False
ADD_MENU = False
ACTIVATE_HISTORY = True
MENU_VALID = False

SECRET_KEY = 'dev-secret-key-local-asterisco-siete-7'

ALLOWED_HOSTS = ['*']

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR     = os.path.dirname(os.path.dirname(__file__))

# ── Base de datos local (SQLite para desarrollo sin PostgreSQL) ───────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_local_asterisco7.sqlite3'),
    }
}

# ── Apps instaladas — MÍNIMO ABSOLUTO para migrar admin_juego ────────────────
# Todas las demás apps del proyecto usan APIs de Django <2.0 y fallan en Django 6
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django_extensions',
    'rest_framework',
    # Apps del proyecto Asterisco Siete (lista completa)
    'admin_lib',
    'admin_historic',
    'admin_juego',
    'admin_apuestas',
    'admin_comercializacion',
    'admin_datamart',
    'admin_finanzas',
    'admin_logros',
    'admin_mail',
    'admin_permisologia',
    'admin_principal',
    'admin_profiles',
    'admin_reportes',
    'admin_resultados',
    'admin_soporte',
    'admin_status',
    'admin_themes',
    'admin_users',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Django 6+ usa MIDDLEWARE (lista), no MIDDLEWARE_CLASSES (tupla)
MIDDLEWARE = list(MIDDLEWARE_CLASSES)



ROOT_URLCONF   = 'admin_asterisco7.urls'
WSGI_APPLICATION = 'admin_asterisco7.wsgi.application'

TIME_ZONE     = 'America/Caracas'
LANGUAGE_CODE = 'es'
SITE_ID       = 1
USE_I18N      = True
USE_L10N      = True
USE_TZ        = False

MEDIA_ROOT  = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL   = '/media/'
STATIC_URL  = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'static'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'static'),       # sirve static/dashboard/index.html
            os.path.join(PROJECT_PATH, 'templates'), # templates propios del proyecto
        ],
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

# ── Cache local (memoria, sin Redis) ─────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ── Admin y URLs ─────────────────────────────────────────────────────────────
ADMIN_URL   = '/admin/'
ACCESO_URL  = '/login/'
LOGOUT_URL  = '/logout/'
INDEX_URL   = '/'

# ── REST Framework ────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
}

# ── Opciones adicionales del proyecto ─────────────────────────────────────────
DEFAULT_TABLESPACE       = 'ts_parley'
DEFAULT_INDEX_TABLESPACE = 'ts_parley'
X_FRAME_OPTIONS          = 'DENY'
USE_THOUSAND_SEPARATOR   = False
DECIMAL_SEPARATOR        = ','
FORMAT_STR_DATE          = '%d-%m-%Y'
FORMAT_STR_DATE_2        = '%d/%m/%Y'
FORMAT_STR_DATE_REPORTS  = '%Y-%m-%d'
FORMAT_STR_TIME          = '%I:%M %p'
FORMAT_STR_DATETIME      = '%d%m%y%H%M'
THEME_DEFAULT            = 'theme_default'

MESSAGES_GLOBAL = {
    'consulta_por_juegos': 'El siguiente reporte puede tener un margen de error del 0.3%'
}

# ── Logging mínimo ────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# ── jsonfield ─────────────────────────────────────────────────────────────────
# Si no está instalado: pip install jsonfield
