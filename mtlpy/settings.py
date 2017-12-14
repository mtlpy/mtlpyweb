# Django settings for MtlPy website
#
# Note: this django settings reads os.environ to get environment specific
#       configuration.

import os
from os.path import join, dirname, abspath

import environ
import pymysql
pymysql.install_as_MySQLdb()


env = environ.Env(
    GOOGLE_ANALYTICS=(str, ''),
    YOUTUBE_API_KEY=(str, ''),
)
env.read_env('.env')

WSGI_APPLICATION = 'mtlpy.wsgi.application'

SITENAME = u"Montréal-Python"

DEBUG = env('DEBUG', cast=bool, default=False)
SQL_DEBUG = env('SQL_DEBUG', cast=bool, default=False)

CACHES = {
    'default': env.cache_url(default='dummycache://'),
}

CONTACT_EMAILS = ['mtlpyteam@googlegroups.com']

if 'CLEARDB_DATABASE_URL' in os.environ:
    os.environ['DATABASE_URL'] = os.environ['CLEARDB_DATABASE_URL']

DATABASES = {
    'default': env.db(),
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=list, default=[
    'mtlpy-prod.herokuapp.com',
    'montrealpython.org',
    'www.montrealpython.org',
    'mtlpy.org',
    'www.mtlpy.org',
    'montrealpython.com',
    'www.montrealpython.com',
])

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Montreal'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

# WARNING! Note a MTL Python staff! If you change the default language, flat
# pages will not display, you need to change the "url" specified after
# i18npage tags, in base.html, footer.html (and anywhere else i18npage
# is used)
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
)

BASE_DIR = abspath(join(dirname(__file__), '..'))

LOCALE_PATHS = (
    abspath(join(BASE_DIR, 'locale/')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_LOCATION = env('ENV')

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_FORMAT = 'PNG'

MEDIA_ROOT = join(dirname(__file__), "media")
MEDIA_URL = "/media/"
STATIC_ROOT = join(dirname(__file__), "collected_static")
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    join(dirname(__file__), "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'mtlpy.context_processors.extra_context',
        ],
    },
}]

MIDDLEWARE_CLASSES = (
    'bugsnag.django.middleware.BugsnagMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'mtlpy.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django_extensions',
    'sorl.thumbnail',
    'storages',
    'pagination_bootstrap',
    # local apps
    'mtlpy.blog',
    'mtlpy',
    'mtlpy.pages',
)

LOG_LEVEL = env('LOG_LEVEL', default='INFO')
DB_LOG_LEVEL = env('DB_LOG_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s:%(funcName)s:%(lineno)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': DB_LOG_LEVEL,
        },
        'mtlpy': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'sorl': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
    }
}

YOUTUBE_API_KEY = env('YOUTUBE_API_KEY')

DISQUS_SITENAME = "mtlpy"

PAGINATION_INVALID_PAGE_RAISES_404 = True
PAGINATION_DEFAULT_PAGINATION = 10

GOOGLE_ANALYTICS = env('GOOGLE_ANALYTICS')

BUGSNAG = {
    # Those are almost the default behaviors of the lib. But with better errors.
    'api_key': env('BUGSNAG_API_KEY', default=None),
    'release_stage': env('ENV'),
    'notify_release_stages': ['production'],
    'ignore_classes': [
        'django.http.response.Http404',
        'django.http.Http404',
    ],

}

# 1_6.W001 is triggered if the settings module "seems" old.
# Presence of TEST_RUNNER setting is a marker used by this warning. 🙄
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
