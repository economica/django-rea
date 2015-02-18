#!/usr/bin/env python

import os

from django import setup


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    setup()

    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    from django.core.management.commands.makemigrations import Command

    options = {
        'verbosity': 1
    }

    out = StringIO()

    c = Command()
    c.stdout = out
    c.handle('rea', **options)

    print(out.getvalue())
