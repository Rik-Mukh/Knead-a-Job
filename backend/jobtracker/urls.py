"""
URL configuration for jobtracker project.

This module defines the main URL patterns for the job tracker Django project.
It includes the admin interface and API endpoints.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.http import FileResponse
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints for job tracker
    path('api/', include('job_tracker.urls')),
    
]
