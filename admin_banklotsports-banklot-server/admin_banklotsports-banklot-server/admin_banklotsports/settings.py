import os

# Configuracion de celery
import djcelery
import redis
# ejecuta tareas periodicas en tiempos exactos
from celery.schedules import crontab
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from kombu import Exchange, Queue

# from datetime import timedelta


DEBUG = True if os.environ.get('PANEL_DEBUG') == 'True' else False
DEBUG_TOOLBAR = True if os.environ.get('PANEL_DEBUG_TOOLBAR') == 'True' else False
ADD_MENU = True if os.environ.get('PANEL_ADD_MENU') == 'True' else False

ACTIVATE_HISTORY = True
MENU_VALID = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '127.0.0.1',
    os.environ.get('PANEL_ALLOWED_HOSTS_IP'),
    os.environ.get('PANEL_ALLOWED_HOSTS_NAME_1'),
    os.environ.get('PANEL_ALLOWED_HOSTS_NAME_2'),
]

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
}

CELERY_RESULT_BACKEND = 'redis://{0}:6379/1'.format(os.environ.get('REDIS_PORT_6379_TCP_ADDR'))
BROKER_URL = 'amqp://{0}:{1}@{2}:5672//'.format(
    os.environ.get('RABBITMQ_DEFAULT_USER'),
    os.environ.get('RABBITMQ_DEFAULT_PASS'),
    os.environ.get('RABBIT_PORT_5672_TCP_ADDR'),
)

REDIS_DB = redis.Redis(
    host=os.environ.get('REDIS_PORT_6379_TCP_ADDR'),
    port=6379,
)


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


SECRET_KEY = 'jd7@9#1ls=e8oa&amp;^68p90q!mdju($=r8x68j6q#yfa73$5jpf0'
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
DEFAULT_TABLESPACE = 'ts_comer'
DEFAULT_INDEX_TABLESPACE = 'ts_comer'

OPBEAT = {
    'ORGANIZATION_ID': '2608c50a398d4953b38682507fbeac4c',
    'APP_ID': 'df11eb386e',
    'SECRET_TOKEN': '1cbe115d062eba396fff05eb6dc3c1f5a34cb5c7',
}

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.security.SecurityMiddleware', # usar para SSL
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #  Proceso de verificacion de autentificacion
    'admin_principal.middleware.AuthenticationAndPermissionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'crequest.middleware.CrequestMiddleware',
    #  Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser'
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'django.contrib.humanize',
    'djcelery',
    'gunicorn',
    'crequest',
    'django_extensions',
    'rest_framework',

    'opbeat.contrib.django',

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

    # las nuevas apps que a futuro se incorporen en este archivo,
    # deben ser en orden secuelcial de aqui hacia abajo, ya que
    # dicho orden importa para el contentype de la auditoria
    'admin_lib',
    'scripts',
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
        'JQUERY_URL': '/static/js/vendor/jquery-1.11.3.min.js',
    }

# #########################
# conf personal
CACHES_CONF_TIME = {
    'reportes_csv_pdf': {
        'listado_de_tickets': 60 * 60,  # equivale a 60 seg* 60 minutos = 1 hora
        'venta_en_linea_por_ticket': 60 * 60,
        'listado_logros': 60 * 60,
        'listado_resultados': 60 * 60,
        'cuentas_cobrar_pagar': 60 * 60,
    },
    'reportes_objects': {
        'listado_de_tickets': 60 * 60,  # equivale a 60 seg* 60 minutos = 1 hora
        'venta_en_linea_por_ticket': 60 * 60,
    },
    'admin_juegos': {
        'deporte_json_event': 60 * 60 * 24,
        'torneo_json_event': 60 * 60 * 24,
        'temporada_json_event': 60 * 60 * 24,
        'jornadas_json_event': 60 * 60 * 24,
        'equipos_json_event': 60 * 60 * 24,
        'encuentros_json_event': 60 * 60 * 24,
        'encuentros_jugadas_all_json_event': 60 * 60 * 24,
        'deporte_grupo_by_encuentro_json_event': 60 * 60 * 24,
        'encuentro_modalidad_json_event': 60 * 60 * 24,
        'encuentro_jugadores_json_event': 60 * 60 * 24,
        'jugada_json_event': 60 * 60 * 24,
        'grupos_juego_json_event': 60 * 60 * 24,
    },
    'keys_filtros': {
        'key_encuentros': 60 * 60 * 2,
        'key_logros': 60 * 60 * 2,
    },
    'admin_comercializacion': {
        'print_detail': 60 * 60 * 2,
    },
    'registros_db': {
        'menu': 60 * 60 * 24 * 7,
        'menu_permisos': 60 * 60 * 24 * 7,
        'user_type': 60 * 60 * 24 * 7,
        'user_process': 60 * 60 * 24 * 7,
        'sistemajuego': 60 * 60 * 24 * 7,
        'theme': 60 * 60 * 24 * 7,
        'company': 60 * 60 * 24 * 7,
        'status': 60 * 60 * 24 * 7,
        'type_bet': 60 * 60 * 24 * 7,
        'everyone': 60 * 60 * 24 * 7,

        'user': 60 * 60 * 24,
        'session_expire': 60 * 20,
        'dia_trabajo': 60 * 60,
        'comercializacion': 60 * 60 * 24,
        'objects_games': 60 * 60 * 24,
        'encuentros': 60 * 60 * 24 * 3,

        'workers': 60 * 60 * 24 * 3,
        'tickets': 60 * 60 * 24 * 3,
    }
}
###########################

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_KEY = 'public_key_admin_banklotsports'

# PREPEND_WWW = True
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = 'DENY'

USE_THOUSAND_SEPARATOR = False
DECIMAL_SEPARATOR = ','

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/La_Paz'

# este formato se usa en la data de juegos mas que todo
# para las notificaciones y format los json
FORMAT_STR_DATE = '%d-%m-%Y'
FORMAT_STR_DATE_2 = '%d/%m/%Y'
FORMAT_STR_DATE_REPORTS = '%Y-%m-%d'
FORMAT_STR_TIME = '%I:%M %p'
FORMAT_STR_DATETIME = '%d%m%y%H%M'
FORMAT_STR_DATETIME_SECONDS = '%d%m%y%H%M%S'
FORMAT_STR_DATE_3 = '%d/%m/%Y %I:%M:%S %p'
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = '/media/'
ADMIN_URL = '/admin/'
ACCESO_URL = '/login/'
LOGOUT_URL = '/logout/'
INDEX_URL = '/'
# Example: 'http://media.lawrence.com/static/'
STATIC_URL = '/static/'
THEMES_URL = '/themes/'

PAGE_404_URL = '#404-page-not-found'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
STATIC_ROOT = 'staticfiles'  # /var/www/admin_banklotsports/static/'

# URL prefix for static files.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static'),
)

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFileStorage'
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)


ROOT_URLCONF = 'admin_banklotsports.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'admin_banklotsports.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like '/home/html/django_templates' or 'C:/www/django/templates'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
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
    'admin_comercializacion.task',
    'admin_datamart.task',
    'admin_juego.task',
    'admin_finanzas.task',
    'admin_resultados.task',
    'admin_mail.task',
)  # importa app donde hay tareas periodicas


CELERYBEAT_SCHEDULE = {
    # Todos los dias a las 4:30 de la madrugada
    'add-AsyncCloseDayAutomaticGeneral': {
        'task': 'AsyncCloseDayAutomaticGeneral',
        'schedule': crontab(hour=4, minute=30),
        # 'schedule': timedelta(seconds=2),
        'args': (),
        'kwargs': {'distribute': True, 'tipo': 'Operadoras'},
    },
    # Todos los dias a las 4:35 de la madrugada
    'add-AsyncCreateAutomaticTemporadas': {
        'task': 'AsyncCreateAutomaticTemporadas',
        'schedule': crontab(hour=4, minute=35),
        # 'schedule': timedelta(seconds=2),
        'args': (),
        'kwargs': {},
    },
    # Todos los dias a las 4:40 de la madrugada
    'add-AsyncCuadreParleyAutomaticGeneral': {
        'task': 'AsyncCuadreParleyAutomaticGeneral',
        'schedule': crontab(hour=4, minute=40),
        # 'schedule': timedelta(seconds=2),
        'args': (),
        'kwargs': {},
    },
    # Todos los dias a las 4:50 de la madrugada
    'add-AsyncTruncarEventNotification': {
        'task': 'AsyncTruncarEventNotification',
        'schedule': crontab(hour=4, minute=50),
        # 'schedule': timedelta(seconds=2),
        'args': (),
        'kwargs': {},
    },
    # Todos los dias a las 5 de la madrugada
    'add-AsyncProcesarTicketsGanadosNoCobrados': {
        'task': 'AsyncProcesarTicketsGanadosNoCobrados',
        'schedule': crontab(hour=5, minute=0),
        # 'schedule': timedelta(seconds=3),
        'args': (),
        'kwargs': {},
    },
    # Todos los dias a las 5 de la madrugada
    'add-AsyncProcesarBoot': {
        'task': 'AsyncProcesarBoot',
        'schedule': crontab(hour=8, minute=00),
        # 'schedule': timedelta(seconds=3),
        'args': (),
        'kwargs': {},
    },
    # Todos los Lunes a las 5:10 de la madrugada
    'add-AsyncGestion_GainComercializadora_AlquiladosSemanal': {
        'task': 'AsyncGestion_GainComercializadora_AlquiladosSemanal',
        'schedule': crontab(day_of_week=1, hour=5, minute=10),
        # 'schedule': timedelta(seconds=2),
        'args': (),
        'kwargs': {},
    },
    # Todos los primeros y 15 de cada mes a las 5:20 de la madrugada
    'add-AsyncGestion_GainComercializadora_AlquiladosQuincenal': {
        'task': 'AsyncGestion_GainComercializadora_AlquiladosQuincenal',
        'schedule': crontab(day_of_month='1,15', hour=5, minute=20),
        # 'schedule': timedelta(seconds=2),
        'args': (),
        'kwargs': {},
    },
    # Todos los primeros de cada mes a las 5:30 de la madrugada
    'add-AsyncGestion_GainComercializadora_AlquiladosMensual': {
        'task': 'AsyncGestion_GainComercializadora_AlquiladosMensual',
        'schedule': crontab(day_of_month=1, hour=5, minute=30),
        # 'schedule': timedelta(seconds=2),
        'args': (),
        'kwargs': {},
    },
}


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

MESSAGES_GLOBAL = {
    'consulta_por_juegos': 'El siguiente reporte puede tener un margen de error del 0.3%'
}


THEME_DEFAULT = 'theme_default'


TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
