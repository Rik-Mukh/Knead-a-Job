"""
ASGI config for jobtracker project.

This module exposes the ASGI callable as a module-level variable named ``application``.
ASGI (Asynchronous Server Gateway Interface) is used for async Django applications.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobtracker.settings')

application = get_asgi_application()
