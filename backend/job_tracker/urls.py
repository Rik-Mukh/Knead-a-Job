"""
Job Tracker URL Configuration

This module defines URL patterns for the job tracker API endpoints.
It uses Django REST Framework routers to automatically generate URLs for the ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobApplicationViewSet, ResumeViewSet, ResumeTemplateViewSet, 
    ExperienceViewSet, ProjectViewSet, EducationViewSet
)

# Create a router instance
router = DefaultRouter()

# Register ViewSets with the router
# This automatically creates URL patterns for CRUD operations
router.register(r'applications', JobApplicationViewSet, basename='application')
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'resume-templates', ResumeTemplateViewSet, basename='resume-template')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'educations', EducationViewSet, basename='education')

# URL patterns for the job tracker app
urlpatterns = [
    # Include all router-generated URLs
    path('', include(router.urls)),
]
