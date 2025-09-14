"""
WSGI config for jobtracker project.

This module exposes the WSGI callable as a module-level variable named ``application``.
WSGI (Web Server Gateway Interface) is used for deploying Django applications.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobtracker.settings')

application = get_wsgi_application()
