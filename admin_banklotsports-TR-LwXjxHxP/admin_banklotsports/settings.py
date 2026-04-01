# -*- coding: utf-8 -*-
"""
settings.py — admin_banklotsports (proyecto legado)
====================================================
NOTA: Este proyecto fue migrado al Sistema Asterisco Siete (*7).
      Ver: admin_AsteriscoSiete-server/admin_AsteriscoSiete7/

      Se han eliminado dependencias deprecadas:
        - djcelery       → no compatible con Python 3.13+
        - opbeat         → reemplazado por Sentry / logging estándar
        - gunicorn       → se gestiona fuera de INSTALLED_APPS
        - debug_toolbar  → se activa solo si está instalado
        - MIDDLEWARE_CLASSES → renombrado a MIDDLEWARE (Django 2+)
        - TEMPLATE_LOADERS / TEMPLATE_DIRS → reemplazado por TEMPLATES dict
"""

import os

# ─────────────────────────────────────────────────────────────────────────────
# Rutas base
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR     = os.path.dirname(os.path.dirname(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# Debug / entorno
# ─────────────────────────────────────────────────────────────────────────────
DEBUG          = os.environ.get('PANEL_DEBUG', 'False') == 'True'
DEBUG_TOOLBAR  = os.environ.get('PANEL_DEBUG_TOOLBAR', 'False') == 'True'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '127.0.0.1',
    os.environ.get('PANEL_ALLOWED_HOSTS_IP'),
    os.environ.get('PANEL_ALLOWED_HOSTS_NAME_1'),
    os.environ.get('PANEL_ALLOWED_HOSTS_NAME_2'),
]

SECRET_KEY = os.environ.get('PANEL_SECRET_KEY', 'cambia-esto-en-produccion')

# ─────────────────────────────────────────────────────────────────────────────
# Administradores
# ─────────────────────────────────────────────────────────────────────────────
ADMINS   = ((os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_MAIL')),)
MANAGERS = ADMINS

# ─────────────────────────────────────────────────────────────────────────────
# Email
# ─────────────────────────────────────────────────────────────────────────────
EMAIL_USE_TLS       = True
EMAIL_HOST          = os.environ.get('EMAIL_HOST')
EMAIL_PORT          = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER')
SERVER_EMAIL        = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# ─────────────────────────────────────────────────────────────────────────────
# Base de datos
# ─────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     os.environ.get('PANEL_DB_NAME'),
        'USER':     os.environ.get('PANEL_DB_USER'),
        'PASSWORD': os.environ.get('PANEL_DB_PASSWORD'),
        'HOST':     os.environ.get('PANEL_DB_HOST'),
        'PORT':     os.environ.get('PANEL_DB_PORT'),
    },
}

DEFAULT_TABLESPACE       = 'ts_comer'
DEFAULT_INDEX_TABLESPACE = 'ts_comer'
TEST_RUNNER              = 'django.test.runner.DiscoverRunner'

# ─────────────────────────────────────────────────────────────────────────────
# Cache (Redis)
# ─────────────────────────────────────────────────────────────────────────────
_REDIS_ADDR = os.environ.get('REDIS_PORT_6379_TCP_ADDR', '127.0.0.1')

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:6379'.format(_REDIS_ADDR),
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
    }
}

try:
    import redis as _redis_module
    REDIS_DB = _redis_module.Redis(host=_REDIS_ADDR, port=6379)
except Exception:
    REDIS_DB = None

# ─────────────────────────────────────────────────────────────────────────────
# Apps instaladas
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',

    'crequest',
    'django_extensions',
    'rest_framework',

    'admin_apuestas',
    'admin_comercializacion',
    'admin_datamart',
    'admin_finanzas',
    'admin_historic',
    'admin_juego',
    'admin_logros',
    'admin_mail',
    'admin_permisologia',
    'admin_principal',
    'admin_profiles',
    'admin_reportes',
    'admin_resultados',
    'admin_status',
    'admin_soporte',
    'admin_themes',
    'admin_users',

    # Orden secuencial importa para el ContentType de auditoría
    'admin_lib',
    'scripts',
]

# Debug toolbar (solo si está instalado)
if DEBUG_TOOLBAR:
    try:
        import debug_toolbar  # noqa
        INSTALLED_APPS = ['debug_toolbar'] + INSTALLED_APPS
    except ImportError:
        DEBUG_TOOLBAR = False

INSTALLED_APPS = tuple(INSTALLED_APPS)

# ─────────────────────────────────────────────────────────────────────────────
# Middleware (Django 2+ usa MIDDLEWARE, no MIDDLEWARE_CLASSES)
# ─────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'admin_principal.middleware.AuthenticationAndPermissionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG_TOOLBAR:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

    def custom_show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    }

# ─────────────────────────────────────────────────────────────────────────────
# URLs y WSGI
# ─────────────────────────────────────────────────────────────────────────────
ROOT_URLCONF      = 'admin_banklotsports.urls'
WSGI_APPLICATION  = 'admin_banklotsports.wsgi.application'

# ─────────────────────────────────────────────────────────────────────────────
# Templates (formato moderno Django 2+)
# ─────────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────────
# REST Framework
# ─────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# Internacionalización
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE          = 'es'
TIME_ZONE              = 'America/Caracas'
USE_I18N               = True
USE_L10N               = True
USE_TZ                 = False
USE_THOUSAND_SEPARATOR = False
DECIMAL_SEPARATOR      = ','
SITE_ID                = 1

# Formatos de fecha/hora usados en notificaciones y JSON
FORMAT_STR_DATE             = '%d-%m-%Y'
FORMAT_STR_DATE_2           = '%d/%m/%Y'
FORMAT_STR_DATE_REPORTS     = '%Y-%m-%d'
FORMAT_STR_TIME             = '%I:%M %p'
FORMAT_STR_DATETIME         = '%d%m%y%H%M'
FORMAT_STR_DATETIME_SECONDS = '%d%m%y%H%M%S'
FORMAT_STR_DATE_3           = '%d/%m/%Y %I:%M:%S %p'

# ─────────────────────────────────────────────────────────────────────────────
# Archivos estáticos y media
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(PROJECT_PATH, 'media')
THEMES_URL  = '/themes/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# ─────────────────────────────────────────────────────────────────────────────
# URLs internas del sistema
# ─────────────────────────────────────────────────────────────────────────────
ADMIN_URL   = '/admin/'
ACCESO_URL  = '/login/'
LOGOUT_URL  = '/logout/'
INDEX_URL   = '/'
PAGE_404_URL = '#404-page-not-found'

# ─────────────────────────────────────────────────────────────────────────────
# Sesiones
# ─────────────────────────────────────────────────────────────────────────────
SESSION_ENGINE     = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_KEY = 'public_key_admin_asterisco7'

# ─────────────────────────────────────────────────────────────────────────────
# Seguridad
# ─────────────────────────────────────────────────────────────────────────────
X_FRAME_OPTIONS = 'DENY'

# ─────────────────────────────────────────────────────────────────────────────
# Tiempos de caché por categoría (en segundos)
# ─────────────────────────────────────────────────────────────────────────────
CACHES_CONF_TIME = {
    'reportes_csv_pdf': {
        'listado_de_tickets':       60 * 60,
        'venta_en_linea_por_ticket': 60 * 60,
        'listado_logros':           60 * 60,
        'listado_resultados':       60 * 60,
        'cuentas_cobrar_pagar':     60 * 60,
    },
    'reportes_objects': {
        'listado_de_tickets':        60 * 60,
        'venta_en_linea_por_ticket': 60 * 60,
    },
    'admin_comercializacion': {
        'print_detail': 60 * 60 * 2,
    },
    'registros_db': {
        'menu':            60 * 60 * 24 * 7,
        'menu_permisos':   60 * 60 * 24 * 7,
        'user_type':       60 * 60 * 24 * 7,
        'user_process':    60 * 60 * 24 * 7,
        'sistemajuego':    60 * 60 * 24 * 7,
        'theme':           60 * 60 * 24 * 7,
        'company':         60 * 60 * 24 * 7,
        'status':          60 * 60 * 24 * 7,
        'type_bet':        60 * 60 * 24 * 7,
        'everyone':        60 * 60 * 24 * 7,

        'user':            60 * 60 * 24,
        'session_expire':  60 * 20,
        'dia_trabajo':     60 * 60,
        'comercializacion': 60 * 60 * 24,
        'objects_games':   60 * 60 * 24,
        'encuentros':      60 * 60 * 24 * 3,
        'workers':         60 * 60 * 24 * 3,
        'tickets':         60 * 60 * 24 * 3,
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level':   'ERROR',
            'filters': ['require_debug_false'],
            'class':   'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers':  ['mail_admins'],
            'level':     'ERROR',
            'propagate': True,
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Misc
# ─────────────────────────────────────────────────────────────────────────────
MESSAGES_GLOBAL = {
    'consulta_por_juegos': 'El siguiente reporte puede tener un margen de error del 0.3%'
}

THEME_DEFAULT    = 'theme_default'
ACTIVATE_HISTORY = True
MENU_VALID       = False
