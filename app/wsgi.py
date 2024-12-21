"""
WSGI config for app project.

This project isn't made with WSGI in mind. Check the ASGI config instead!
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
