"""
WSGI config for herokuprova project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise.django import DjangoWhiteNoise

settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainapp.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)


from wsil.script import github_crawler
github_crawler.start()