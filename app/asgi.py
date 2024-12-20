"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

This application is using BlackNoise to serve static files
https://github.com/matthiask/blacknoise

For deployement, Uvicorn and Gunicorn are used

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from blacknoise import BlackNoise
from django.core.asgi import get_asgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = BlackNoise(get_asgi_application())
application.add(settings.STATIC_ROOT, settings.STATIC_URL)
