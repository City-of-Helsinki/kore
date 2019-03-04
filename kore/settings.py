"""
Django settings for KORE
"""
import os
import environ
import raven

root = environ.Path(__file__) - 2  # two folders back
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    ALLOWED_HOSTS=(list, []),
    ADMINS=(list, []),
    DATABASE_URL=(str, 'postgis:///kore'),
    SECURE_PROXY_SSL_HEADER=(tuple, None),
    MEDIA_ROOT=(environ.Path(), root('media')),
    STATIC_ROOT=(environ.Path(), root('static')),
    MEDIA_URL=(str, '/media/'),
    STATIC_URL=(str, '/static/'),
    SENTRY_DSN=(str, ''),
    SENTRY_ENVIRONMENT=(str, ''),
    COOKIE_PREFIX=(str, 'kore'),
    INTERNAL_IPS=(list, []),
)

env_file = root('config.env')
# read_env is stupidly verbose when this file is missing
if os.path.isfile(env_file):
    env.read_env(env_file)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

DEBUG = env('DEBUG')
SECRET_KEY = env.str('SECRET_KEY')
if DEBUG and not SECRET_KEY:
    SECRET_KEY = 'xxx'
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
ADMINS = env('ADMINS')
DATABASES = {'default': env.db()}
SECURE_PROXY_SSL_HEADER = env('SECURE_PROXY_SSL_HEADER')

MEDIA_ROOT = env('MEDIA_ROOT')
STATIC_ROOT = env('STATIC_ROOT')
MEDIA_URL = env('MEDIA_URL')
STATIC_URL = env('STATIC_URL')

SECURE_PROXY_SSL_HEADER = env('SECURE_PROXY_SSL_HEADER')
INTERNAL_IPS = env.list('INTERNAL_IPS',
                        default=(['127.0.0.1'] if DEBUG else []))
CORS_ORIGIN_ALLOW_ALL = True

CSRF_COOKIE_NAME = '{}-csrftoken'.format(env('COOKIE_PREFIX'))
SESSION_COOKIE_NAME = '{}-sessionid'.format(env('COOKIE_PREFIX'))

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'nested_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'modeltranslation',
    'leaflet',
    'munigeo',
    'schools',
    'django_filters'
]

if DEBUG:
    # INSTALLED_APPS.insert(0, 'devserver')
    # INSTALLED_APPS.insert(0, 'debug_toolbar')
    pass

if env('SENTRY_DSN'):
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
        'environment': env('SENTRY_ENVIRONMENT'),
        'release': raven.fetch_git_sha(BASE_DIR),
    }
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kore.urls'

WSGI_APPLICATION = 'kore.wsgi.application'

# Munigeo
# https://github.com/City-of-Helsinki/munigeo

PROJECTION_SRID = 3067

# If no country specified (for example through a REST API call), use this
# as default.
DEFAULT_COUNTRY = 'fi'
# The word used for municipality in the OCD identifiers in the default country.
DEFAULT_OCD_MUNICIPALITY = 'kunta'

BOUNDING_BOX = [-548576, 6291456, 1548576, 8388608]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('fi', gettext('Finnish')),
    ('sv', gettext('Swedish')),
    ('en', gettext('English')),
)

LOCALE_PATH = os.path.join(BASE_DIR, "schools", "locale")

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'MAX_PAGINATE_BY': 1000,             # Maximum limit allowed when using `?page_size=xxx`.
    'DEFAULT_FILTER_BACKENDS':
        ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
           os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
