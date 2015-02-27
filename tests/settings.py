INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'rea',
    'tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

MIDDLEWARE_CLASSES = ()

SECRET_KEY = 'rea-fake-key'
