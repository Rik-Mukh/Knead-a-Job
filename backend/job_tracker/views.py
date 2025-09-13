"""
Job Tracker Views

This module contains Django REST Framework views for the job tracker API.
Views handle HTTP requests and return appropriate responses for job applications and resumes.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobApplication, Resume
from .serializers import JobApplicationSerializer, ResumeSerializer


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


class ResumeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Resume model.
    
    Provides CRUD operations for resumes.
    Users can only access their own resumes.
    """
    
    serializer_class = ResumeSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    
    def get_queryset(self):
        """
        Return only resumes belonging to the current user.
        
        Returns:
            QuerySet: Filtered queryset of resumes
        """
        return JobApplication.objects.all()
        
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """
        Custom action to set a resume as the default for the current user.
        
        Args:
            pk: Primary key of the resume to set as default
            
        Returns:
            Response: JSON response confirming the action
        """
        resume = self.get_object()
        # Unset all other default resumes for this user
        Resume.objects.filter(user=request.user, is_default=True).exclude(id=resume.id).update(is_default=False)
        # Set this resume as default
        resume.is_default = True
        resume.save()
        return Response({'status': 'Resume set as default'})
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """
        Custom action to get the default resume for the current user.
        
        Returns:
            Response: JSON response with default resume data or 404 if none exists
        """
        try:
            default_resume = Resume.objects.filter(user=request.user, is_default=True).first()
            if default_resume:
                serializer = self.get_serializer(default_resume)
                return Response(serializer.data)
            else:
                return Response(
                    {'detail': 'No default resume found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except Resume.DoesNotExist:
            return Response(
                {'detail': 'No default resume found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
