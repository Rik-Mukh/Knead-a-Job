"""
Job Tracker Views

This module contains Django REST Framework views for the job tracker API.
Views handle HTTP requests and return appropriate responses for job applications and resumes.
"""

from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import JobApplication, ResumeTemplate, Experience, Project, Education
from .serializers import (
    JobApplicationSerializer, ResumeTemplateSerializer, 
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
        if self.request.user.is_authenticated:
            return JobApplication.objects.filter(user=self.request.user)
        return JobApplication.objects.none()
    
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
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  # Explicitly allow PUT
    
    def get_queryset(self):
        """
        Return the singleton resume template.
        
        Returns:
            QuerySet: QuerySet containing the single template
        """
        return ResumeTemplate.objects.all()
    
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
        Create or update the singleton resume template.
        
        Args:
            serializer: The serializer instance
        """
        serializer.save()
    
    def list(self, request, *args, **kwargs):
        """
        Get the resume template.
        Since only one template exists, this returns the single template.
        
        Returns:
            Response: JSON response with resume template data or 404 if none exists
        """
        try:
            template = ResumeTemplate.objects.first()
            if template:
                serializer = self.get_serializer(template)
                return Response(serializer.data)  # Return single object, not array
            else:
                # Create a new template if none exists
                template = ResumeTemplate.get_or_create_template()
                serializer = self.get_serializer(template)
                return Response(serializer.data)
        except Exception as e:
            return Response(
                {'detail': f'Error retrieving template: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get the resume template by ID (always returns the single template).
        
        Returns:
            Response: JSON response with resume template data
        """
        return self.list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Update the resume template.
        Since it's a singleton, we update the existing template.
        
        Returns:
            Response: JSON response with updated template data
        """
        template = ResumeTemplate.objects.first()
        if not template:
            # Create new template if none exists
            template = ResumeTemplate.objects.create(
                name=request.data.get('name', ''),
                city=request.data.get('city', ''),
                email=request.data.get('email', ''),
                phone=request.data.get('phone', ''),
                links=request.data.get('links', ''),
                summary=request.data.get('summary', ''),
                skills=request.data.get('skills', '')
            )
        else:
            # Update existing template
            for field in ['name', 'city', 'email', 'phone', 'links', 'summary', 'skills']:
                if field in request.data:
                    setattr(template, field, request.data[field])
            template.save()
        
        serializer = self.get_serializer(template)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete the resume template.
        
        Returns:
            Response: 204 No Content on successful deletion
        """
        template = ResumeTemplate.objects.first()
        if template:
            template.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'Resume template not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Return all experiences - no template filtering needed."""
        return Experience.objects.all()

    def perform_create(self, serializer):
        """Create a new experience entry - no template linking needed."""
        serializer.save()


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Project model.
    
    Provides CRUD operations for project entries.
    """
    
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """Return all projects - no template filtering needed."""
        return Project.objects.all()
    
    def perform_create(self, serializer):
        """Create a new project entry - no template linking needed."""
        serializer.save()


class EducationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Education model.
    
    Provides CRUD operations for education entries.
    """
    
    serializer_class = EducationSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """Return all education entries - no template filtering needed."""
        return Education.objects.all()
    
    def perform_create(self, serializer):
        """Create a new education entry - no template linking needed."""
        serializer.save()


class IsAuthenticated(permissions.IsAuthenticated):
    pass

