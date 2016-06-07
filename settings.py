# Django settings for project.
import os
import django
import sys
import datetime #for FROZEN_CHECK_EXPIRE_TIME

# Path of Django framework files (no trailing /):
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
# Path of this "site" (no trailing /):
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Michael Huynh', 'mike.huynh@gmail.com'),
)
#Modify if mail servers are rejecting this default email address:
#SERVER_EMAIL = 'root@localhost'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'development.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admineral/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q_ou*rndj_kcfnq5*#$od0923q&r99w+lrhfbowunxat5y#l^g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django_fakewall.middleware.FakewallMiddleware', #maintenance mode
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes', #required by auth
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.admindocs',
    'annoying', #django-annoying
    'south', #migrations
    'django_rpx_plus', 
    'celery', #messaging queue
    'base',
    'tracker',
    'subscription',
)

#The following is not in the default generated settings.py file:

AUTHENTICATION_BACKENDS = (
    'django_rpx_plus.backends.RpxBackend', 
    'django.contrib.auth.backends.ModelBackend', #default django auth
    #'tracker.backends.CustomPermBackend', #if we want obj-level perm
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request', #for request object
    'django.core.context_processors.csrf', #to get just the token
    'django.contrib.messages.context_processors.messages',
    #Above are the default template context processors
    #'tracker.helpers.context_processor',
)

#Additional user data (ie. User Profile)
#AUTH_PROFILE_MODULE = 'base.UserProfile'

# Here are some settings related to auth urls. django has default values for them
# as specified on page: http://docs.djangoproject.com/en/dev/ref/settings/. You
# can override them if you like.
LOGIN_REDIRECT_URL = '/dashboard/' #default: '/accounts/profile/'
#LOGIN_URL = '' #default: '/accounts/login/'
#LOGOUT_URL = '' #default: '/accounts/logout/'

#SMTP is the default backend so no need to specify
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587 #TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'supplelabs@gmail.com'
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'SERP app <do-not-reply@serpapp.com>'
#Defines email addresses that error/admin messages come from
SERVER_EMAIL = 'SERP app admin <root@serpapp.com>'

#Keep from getting 404 messages about favicon.ico
SEND_BROKEN_LINK_EMAILS = False

########################
# tracker settings:    #
########################

#How we will make searches. Takes: dummy, google, or scroogle. 'dummy' is good for
#testing and dev work.
SEARCH_METHOD = 'google'

#For if we use Google AJAX API to search:
GOOGLE_AJAX_API_KEY = ''
WHAT_IS_MY_IP_URL = 'http://whatismyip.heroku.com/'

#Used in celery task to slow down the checks.
CHECK_RATE_LIMIT = '3/m' #per minute

#We need to know so that our messages and reporting can be accurate.
MAX_SEARCH_RESULTS = 100
#MAX_SEARCH_RESULTS = 50

#The time required to pass before user can refresh link again.
#NOTE: This is currently not used. We are currently refreshing every 12
#      hours.
TIME_BETWEEN_REFRESH = datetime.timedelta(hours = 6)

#When we refresh the Track with a new Check, we check to see if there are existing
#Checks that haven't been completed. If so, we check their created date to make sure
#the task hasn't froze or something.
#NOTE: Currently not used.
FROZEN_CHECK_EXPIRE_TIME = datetime.timedelta(minutes = 10)

####################
# celery settings: #
####################

CELERY_RESULT_BACKEND = 'database' #default = database

BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_VHOST = 'serp'
BROKER_USER = 'guest'
BROKER_PASSWORD = 'guest'

#Typically equal to number of cores in CPU.
CELERYD_CONCURRENCY = 2

#If True, tasks are executed locally and never sent to queue.
#CELERY_ALWAYS_EAGER = True
CELERYD_LOG_LEVEL = 'INFO'
#If we enable this, logging data won't be print to console.
#CELERYD_LOG_FILE = 'celeryd.log'

#Additional queues
CELERY_QUEUES = {
    'high': {
        'binding_key': 'high',
    },
    'low': {
        'binding_key': 'low',
    },
}
CELERY_DEFAULT_QUEUE = 'high'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'high'

############################
#django_rpx_plus settings: #
############################
RPXNOW_API_KEY = ''

# The realm is the subdomain of rpxnow.com that you signed up under. It handles 
# your HTTP callback. (eg. http://mysite.rpxnow.com implies that RPXNOW_REALM  is
# 'mysite'.
RPXNOW_REALM = 'serp-app'

# (Optional)
#RPX_TRUSTED_PROVIDERS = ''

# (Optional)
# RPX requires a token_url to be passed to its APIs. The token_url is an
# absolute url that points back to the rpx_response view. By default, this
# token_url is constructed by using request.get_host(). However, there may
# be cases where rpx_response is hosted on another domain (eg. if the website
# is using subdomains). Therefore, we can force the base url to be fixed instead
# of auto-detected. 
# Note: This is the HOSTNAME without the beginning 'http://' or trailing slash
#       part. An example hostname would be: localhost:8000
# Protip: You can set RPX_BASE_SITE_HOST in middleware too.
#RPX_BASE_SITE_HOST = '' #Set in middleware

# If it is the first time a user logs into your site through RPX, we will send 
# them to a page so that they can register on your site. The purpose is to 
# let the user choose a username (the one that RPX returns isn't always suitable)
# and confirm their email address (RPX doesn't always return the user's email).
REGISTER_URL = '/accounts/register/'


#Import any local settings (ie. production environment) that will override
#these development environment settings.
try:
    from local_settings import *
except ImportError:
    pass 
