# -*- coding: utf-8 -*-
"""
settings_local.py — Configuración LOCAL independiente
Parlay Match Point / admin_banklotsports
=========================================================
No hereda de settings.py para evitar los modelos rotos.
Sólo carga las apps necesarias para autenticación y admin.
"""
import os

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG          = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS  = ['*']
SECRET_KEY     = 'dev-secret-key-parlay-match-point-local-2024'

# ── Base de datos SQLite ──────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   os.path.join(BASE_DIR, 'db_local_matchpoint.sqlite3'),
    }
}

# ── Apps: SÓLO Django core (las apps del proyecto son Django 1.x, incompatibles) ──
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF     = 'admin_banklotsports.urls_local'
WSGI_APPLICATION = 'admin_banklotsports.wsgi.application'

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

# ── Sessions en DB (sin Redis) ────────────────────────────────────────────────
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'matchpoint-local',
    }
}
REDIS_DB = None

# ── Estáticos ─────────────────────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(PROJECT_PATH, 'media')

STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# ── Email consola ─────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ── Internacionalización ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'es'
TIME_ZONE     = 'America/Caracas'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = False
SITE_ID       = 1

# ── URLs del sistema ──────────────────────────────────────────────────────────
ADMIN_URL    = '/admin/'
ACCESO_URL   = '/login/'
LOGOUT_URL   = '/logout/'
INDEX_URL    = '/'

# ── Misc ──────────────────────────────────────────────────────────────────────
THEME_DEFAULT    = 'theme_default'
ACTIVATE_HISTORY = False
MENU_VALID       = False
LOGGING          = {}

CACHES_CONF_TIME = {}
MESSAGES_GLOBAL  = {}
