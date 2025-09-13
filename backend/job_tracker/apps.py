"""
Job Tracker App Configuration

This module configures the job_tracker Django application.
It defines the app name and any app-specific settings.
"""

from django.apps import AppConfig


class JobTrackerConfig(AppConfig):
    """
    Configuration class for the job_tracker Django application.
    
    This class defines the default auto field and app name for the job tracker.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_tracker'
