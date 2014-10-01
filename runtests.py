import os, sys
from django import setup
from django.conf import settings, global_settings

# Default settings for Django 1.7 applications
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rea.urls'


# Our settings for test execution
settings.configure(
    DEBUG=True,
    DATABASES=DATABASES,
    MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES,
    INSTALLED_APPS=INSTALLED_APPS + ('rea',)
)

setup()

from django.test.runner import DiscoverRunner
from django.db import connection

test_runner = DiscoverRunner(verbosity=1)
failures = test_runner.run_tests(['rea', ])

if failures:
    sys.exit(failures)
