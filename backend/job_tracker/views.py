"""
Job Tracker Views

This module contains Django REST Framework views for the job tracker API.
Views handle HTTP requests and return appropriate responses for job applications and resumes.
"""

from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import JobApplication, Resume, ResumeTemplate, Experience, Project, Education
from .serializers import (
    JobApplicationSerializer, ResumeSerializer, ResumeTemplateSerializer, 
    ResumeTemplateCreateSerializer, ExperienceSerializer, ProjectSerializer, EducationSerializer
)


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for JobApplication model.
    
    Provides CRUD operations for job applications.
    Users can only access their own applications.
    """
    
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """
        Return only job applications belonging to the current user.
        
        Returns:
            QuerySet: Filtered queryset of job applications
        """
        return JobApplication.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Custom action to get application statistics for the current user.
        
        Returns:
            Response: JSON response with application statistics
        """
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'applied': queryset.filter(status='applied').count(),
            'interview': queryset.filter(status='interview').count(),
            'rejected': queryset.filter(status='rejected').count(),
            'accepted': queryset.filter(status='accepted').count(),
            'withdrawn': queryset.filter(status='withdrawn').count(),
        }
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom action to get recent applications for the current user.
        
        Returns:
            Response: JSON response with recent applications
        """
        limit = request.query_params.get('limit', 5)
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = 5
        
        recent_applications = self.get_queryset()[:limit]
        serializer = self.get_serializer(recent_applications, many=True)
        return Response(serializer.data)



class ResumeTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ResumeTemplate model.
    
    Provides CRUD operations for resume templates.
    Each user can have only one resume template.
    """
    
    serializer_class = ResumeTemplateSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """
        Return only resume templates belonging to the current user.
        
        Returns:
            QuerySet: Filtered queryset of resume templates
        """
        return ResumeTemplate.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        
        Returns:
            Serializer: Appropriate serializer class
        """
        if self.action == 'create':
            return ResumeTemplateCreateSerializer
        return ResumeTemplateSerializer
    
    def perform_create(self, serializer):
        """
        Create a new resume template for the current user.
        
        Args:
            serializer: The serializer instance
        """
        # Check if user already has a resume template
        if ResumeTemplate.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("User already has a resume template.")
        
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """
        Override list to return the user's single resume template.
        Since each user can only have one template, this acts like a 'get my template' endpoint.
        
        Returns:
            Response: JSON response with resume template data or 404 if none exists
        """
        try:
            template = ResumeTemplate.objects.get(user=request.user)
            serializer = self.get_serializer(template)
            return Response([serializer.data])  # Return as list for consistency
        except ResumeTemplate.DoesNotExist:
            return Response(
                {'detail': 'No resume template found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Experience model.
    
    Provides CRUD operations for work experience entries.
    """
    
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """
        Return only experiences belonging to the current user's resume template.
        
        Returns:
            QuerySet: Filtered queryset of experiences
        """
        try:
            template = ResumeTemplate.objects.get(user=self.request.user)
            return Experience.objects.filter(resume_template=template)
        except ResumeTemplate.DoesNotExist:
            return Experience.objects.none()
    
    def perform_create(self, serializer):
        """
        Create a new experience entry for the current user's resume template.
        
        Args:
            serializer: The serializer instance
        """
        try:
            template = ResumeTemplate.objects.get(user=self.request.user)
            serializer.save(resume_template=template)
        except ResumeTemplate.DoesNotExist:
            raise serializers.ValidationError("Resume template not found. Please create a resume template first.")


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Project model.
    
    Provides CRUD operations for project entries.
    """
    
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """
        Return only projects belonging to the current user's resume template.
        
        Returns:
            QuerySet: Filtered queryset of projects
        """
        try:
            template = ResumeTemplate.objects.get(user=self.request.user)
            return Project.objects.filter(resume_template=template)
        except ResumeTemplate.DoesNotExist:
            return Project.objects.none()
    
    def perform_create(self, serializer):
        """
        Create a new project entry for the current user's resume template.
        
        Args:
            serializer: The serializer instance
        """
        try:
            template = ResumeTemplate.objects.get(user=self.request.user)
            serializer.save(resume_template=template)
        except ResumeTemplate.DoesNotExist:
            raise serializers.ValidationError("Resume template not found. Please create a resume template first.")


class EducationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Education model.
    
    Provides CRUD operations for education entries.
    """
    
    serializer_class = EducationSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """
        Return only education entries belonging to the current user's resume template.
        
        Returns:
            QuerySet: Filtered queryset of education entries
        """
        try:
            template = ResumeTemplate.objects.get(user=self.request.user)
            return Education.objects.filter(resume_template=template)
        except ResumeTemplate.DoesNotExist:
            return Education.objects.none()
    
    def perform_create(self, serializer):
        """
        Create a new education entry for the current user's resume template.
        
        Args:
            serializer: The serializer instance
        """
        try:
            template = ResumeTemplate.objects.get(user=self.request.user)
            serializer.save(resume_template=template)
        except ResumeTemplate.DoesNotExist:
            raise serializers.ValidationError("Resume template not found. Please create a resume template first.")


class IsAuthenticated(permissions.IsAuthenticated):
    pass

