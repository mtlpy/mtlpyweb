# -*- coding: utf-8 -*-
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
    DEBUG=(bool, False),
    LOCAL=(bool, False),

    GOOGLE_ANALYTICS=(str, ''),
    YOUTUBE_API_KEY=(str, ''),

    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_STORAGE_BUCKET_NAME=(str, ''),
)
env.read_env('.env')

LOCAL = env('LOCAL')

if not LOCAL:
    # Python dotted path to the WSGI application used by Django's runserver.
    WSGI_APPLICATION = 'mtlpy.wsgi.application'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

SITENAME = u"Montréal-Python"

TINYMCE_DEFAULT_CONFIG = {
  'file_browser_callback': 'mce_filebrowser',
  'height': 600,
  'width': '100%',
}

DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_FORMAT = 'PNG'

CACHES = {
    'default': env.cache_url(default='dummycache://')
}

ADMINS = (
    ('Mtlpy Admin', 'mtlpyteam+website@googlegroups.com'),
)
CONTACT_EMAILS = ['mtlpyteam@googlegroups.com']

MANAGERS = ADMINS

if 'CLEARDB_DATABASE_URL' in os.environ:
    os.environ['DATABASE_URL'] = os.environ['CLEARDB_DATABASE_URL']

DATABASES = {
    'default': env.db(),
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'montrealpython.org',
    'www.montrealpython.org',
    'mtlpy.org',
    'www.mtlpy.org',
    'montrealpython.com',
    'www.montrealpython.com',
]

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
LANGUAGE_CODE = 'en-ca'
LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
)
LOCALE_PATHS = (
    abspath(join(dirname(__file__), '..', 'locale/')),
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


TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               'django.core.context_processors.request',
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               "mtlpy.context_processors.extra_context")

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'bugsnag.django.middleware.BugsnagMiddleware',
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'mtlpy.urls'

TEMPLATE_DIRS = (
    join(abspath(join(dirname(__file__), '..')), 'templates'),
)

INSTALLED_APPS = (
    'localeurl',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django_extensions',
    'tinymce',
    'sorl.thumbnail',
    'mce_filebrowser',
    # local apps
    'mtlpy.blog',
    'mtlpy',
    'mtlpy.pages',
    'pagination',
)

# a sample logging configuration. The only tangible logging
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
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
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
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'mtlpy': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'sorl': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
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
    'release_stage': env('BUGSNAG_RELEASE_STAGE', default='development'),
    'notify_release_stages': ['production'],
}
