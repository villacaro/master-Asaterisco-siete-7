import os
import sys

# Configuracion de celery
import djcelery
from kombu import Exchange, Queue

DEBUG = True if os.environ.get('WS_DEBUG') == 'True' else False
DEBUG_TOOLBAR = True if os.environ.get('WS_DEBUG_TOOLBAR') == 'True' else False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '127.0.0.1',
    os.environ.get('WS_ALLOWED_HOSTS_IP'),
    os.environ.get('WS_ALLOWED_HOSTS_NAME_1'),
    os.environ.get('WS_ALLOWED_HOSTS_NAME_2'),
]

ACCESS_TO_DEVELOPER = {
    'taquilla_id': os.environ.get('WS_ACCESS_TO_DEVELOPER')
}

ADMINS = (
    (os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_MAIL')),
)
MANAGERS = ADMINS
ADMIN_FOR = MANAGERS

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PANEL_DB_NAME'),
        'USER': os.environ.get('PANEL_DB_USER'),
        'PASSWORD': os.environ.get('PANEL_DB_PASSWORD'),
        'HOST': os.environ.get('PANEL_DB_HOST'),
        'PORT': os.environ.get('PANEL_DB_PORT'),
    },
    'webservice_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('WS_DB_NAME'),
        'USER': os.environ.get('WS_DB_USER'),
        'PASSWORD': os.environ.get('WS_DB_PASSWORD'),
        'HOST': os.environ.get('WS_DB_HOST'),
        'PORT': os.environ.get('WS_DB_PORT'),
    }
}

CELERY_RESULT_BACKEND = 'redis://{0}:6379/1'.format(os.environ.get('REDIS_PORT_6379_TCP_ADDR'))
BROKER_URL = 'amqp://{0}:{1}@{2}:5672//'.format(
    os.environ.get('RABBITMQ_DEFAULT_USER'),
    os.environ.get('RABBITMQ_DEFAULT_PASS'),
    os.environ.get('RABBIT_PORT_5672_TCP_ADDR'),
)

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{0}:6379'.format(os.environ.get('REDIS_PORT_6379_TCP_ADDR')),
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        }
    }
}

SECRET_KEY = 'gdkk-s082^6sn2i)8vv^=ta)!+zuek64ae=hy%_(48u7ljxtj0'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

KEY_RSA_LEN = 1024

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_L10N = True
USE_TZ = False

PANEL_USING = os.environ.get('WS_PANEL_USING')

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(sys.path[0].replace('ws_sportparley', PANEL_USING))

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
# Admin
ADMIN_URL = '/admin/'
# Media
MEDIA_URL = '/media/'
# Public links
PUBLIC_URL = '/public/'
# Connection
CONN_URL = '/connection/'
# GetFiles
UPDATE_URL = '/getfiles/'
MEDIA_PATH = PROJECT_PATH.replace('ws_sportparley', PANEL_USING)
MEDIA_ROOT = os.path.join(MEDIA_PATH, 'media')

ROOT_URLCONF = 'ws_sportparley.urls'
WSGI_APPLICATION = 'ws_sportparley.wsgi.application'
DEFAULT_TABLESPACE = 'ts_comer'
DEFAULT_INDEX_TABLESPACE = 'ts_comer'

OPBEAT = {
    'ORGANIZATION_ID': '2608c50a398d4953b38682507fbeac4c',
    'APP_ID': 'a2cc6af875',
    'SECRET_TOKEN': '1cbe115d062eba396fff05eb6dc3c1f5a34cb5c7',
}

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'opbeat.contrib.django',
    'ws_auth',
    'ws_client',
    'ws_notifications',
    'ws_requests',
    'ws_sport_requests',
    'ws_sportparley',
    'ws_process',
    'ws_mail',
    'admin_apuestas',
    'admin_comercializacion',
    'admin_finanzas',
    'admin_reportes',
    'admin_historic',
    'admin_juego',
    'admin_logros',
    'admin_permisologia',
    'admin_principal',
    'admin_profiles',
    'admin_status',
    'admin_themes',
    'admin_users',
    'admin_soporte',
    'admin_datamart',
    'admin_resultados',
    'admin_mail'
)

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'ws_auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES

    INSTALLED_APPS = (
        'debug_toolbar',
    ) + INSTALLED_APPS

    def custom_show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    }

DATABASE_ROUTERS = ['ws_client.routers.DatabaseAppsRouter', ]
DATABASE_APPS_MAPPING = {'ws_client': 'webservice_db'}

CACHES_CONF_TIME = {
    'getJuegos': {
        'deportes': 60 * 60,
        'temporadas': 60 * 60,
        'jornadas': 60 * 60,
        'encuentros': 60 * 60,
        'jugadas': 60 * 60,
        'all': 60 * 60,
    },
    'Consultas': {
        'ListadoTickets': 60 * 60,
        'get_data_juegos': 60 * 60 * 24,
    },
    'Auth': {
        'ws_session': (60 * 60),
    },
    'registros_db': {
        'ClientIPAddress': 60 * 60 * 24 * 7,
        'ClientVersion': 60 * 60 * 24 * 7,
    }
}

djcelery.setup_loader()

CELERY_TIMEZONE = TIME_ZONE
CELERY_MESSAGE_COMPRESSION = 'zlib'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_TRACK_STARTED = True
CELERY_SEND_TASK_ERROR_EMAILS = True
# La concurrencia esta comentada xq se audita desde los worker directamente,
# ya que algunos usan la maxima y otros la minima
# CELERYD_CONCURRENCY = 1
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_RESULT_PERSISTENT = True
CELERYD_POOL_RESTARTS = True

CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True

CELERY_IMPORTS = (
    'admin_apuestas.task',
    'admin_datamart.task',
    'admin_juego.task',
    'admin_finanzas.task',
    'admin_resultados.task',
)  # importa app donde hay tareas periodicas

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('resultados', Exchange('resultados'), routing_key='resultados'),
    Queue('tickets_items', Exchange('tickets_items'), routing_key='tickets_items'),
    Queue('tickets', Exchange('tickets'), routing_key='tickets'),
    Queue('porcentajes_cadena', Exchange('porcentajes_cadena'), routing_key='porcentajes_cadena'),
    Queue('reportes', Exchange('reportes'), routing_key='reportes'),
    Queue('reportes_async', Exchange('reportes_async'), routing_key='reportes_async'),
)
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'
