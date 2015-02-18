#!/usr/bin/env python

import sys

import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == "__main__":
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
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

    SECRET_KEY = 'fake-key'

    # Our settings for test execution
    settings.configure(
        DATABASES=DATABASES,
        DEBUG=True,
        INSTALLED_APPS=INSTALLED_APPS + ('rea', ),
        MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES,
        SECRET_KEY=SECRET_KEY
    )

    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['rea'])
    sys.exit(bool(failures))
