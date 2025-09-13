"""
Job Tracker Views

This module contains Django REST Framework views for the job tracker API.
Views handle HTTP requests and return appropriate responses for job applications and resumes.
"""

from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import JobApplication, Resume, MeetingNote, Notification
from .serializers import JobApplicationListSerializer, JobApplicationDetailSerializer, ResumeSerializer, MeetingNoteSerializer, NotificationSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for JobApplication model.
    
    Provides CRUD operations for job applications.
    Users can only access their own applications.
    """
    # Replace with IsAuthenticated later
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return JobApplicationDetailSerializer  # Show full fields
        return JobApplicationListSerializer  # List view hides meeting_minutes
    
    def get_queryset(self):
        """
        Return only job applications belonging to the current user.
        
        Returns:
            QuerySet: Filtered queryset of job applications
        """
        # TODO: Change this to return only the applications for the current user
        # return JobApplication.objects.filter(user=self.request.user)
        return JobApplication.objects.all()

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
        
        # recent_applications = self.get_queryset()[:limit]
        recent_applications = self.get_queryset().order_by('-created_at')[:limit]
        serializer = self.get_serializer(recent_applications, many=True)
        return Response(serializer.data)

    def create_notification(self, job_application, title, message, show_date):
        """
        Create a notification for a job application.
        
        Args:
            job_application: JobApplication instance
            title: Notification title
            message: Notification message
            show_date: DateTime when to show this notification
        """
        print(f"DEBUG: Creating notification - Title: {title}, Show Date: {show_date}")
        
        # Get or create a default user for development
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(
            username='halalkingxi',
            defaults={'email': 'rik@ualberta.ca', 'first_name': 'Rik', 'last_name': 'Mukherji'}
        )
        print(f"DEBUG: Using user: {user.username}")
        
        # Check if notification already exists to avoid duplicates
        existing_notification = Notification.objects.filter(
            user=user,
            job_application=job_application,
            title=title
        ).first()
        
        if existing_notification:
            print(f"DEBUG: Notification already exists, skipping creation")
        else:
            try:
                notification = Notification.objects.create(
                    user=user,
                    job_application=job_application,
                    title=title,
                    message=message,
                    show_date=show_date
                )
                print(f"DEBUG: Successfully created notification with ID: {notification.id}")
            except Exception as e:
                print(f"DEBUG: Error creating notification: {e}")

    def update(self, request, *args, **kwargs):
        """
        Override update method to trigger notifications when status changes.
        """
        instance = self.get_object()
        old_status = instance.status
        
        print(f"DEBUG: Updating job application {instance.id} from status '{old_status}' to '{request.data.get('status', 'unknown')}'")
        
        # Call the parent update method
        response = super().update(request, *args, **kwargs)
        
        # Refresh the instance to get the updated status
        instance.refresh_from_db()
        new_status = instance.status
        
        print(f"DEBUG: Status changed from '{old_status}' to '{new_status}'")
        
        # Check if status changed from 'applied' to 'interview'
        if old_status == 'applied' and new_status == 'interview':
            print("DEBUG: Creating notifications for status change to interview")
            
            # Create immediate notification (show now)
            self.create_notification(
                job_application=instance,
                title="Follow-up Reminder",
                message=f"Don't forget to send a thank you email for your interview at {instance.company_name} for the {instance.position} position!",
                show_date=timezone.now()  # Show immediately
            )
            print("DEBUG: Created immediate notification")
            
            # Create future notification (show in 1 week)
            future_date = timezone.now() + timedelta(weeks=1)
            self.create_notification(
                job_application=instance,
                title="Status Update Reminder",
                message=f"Time to check in on your application at {instance.company_name} for the {instance.position} position. Have you heard back or been ghosted?",
                show_date=future_date  # Show in 1 week
            )
            print("DEBUG: Created future notification")
        else:
            print(f"DEBUG: No notification needed - status change from '{old_status}' to '{new_status}'")
        
        return response


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
        return Resume.objects.all()
        
    
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
    
class MeetingNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MeetingNote model.
    
    Provides CRUD operations for meeting notes.
    Users can only access their own meeting notes.
    """
    serializer_class = MeetingNoteSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development

    def get_queryset(self):
        """
        Return meeting notes filtered by job application if specified.
        
        Returns:
            QuerySet: Filtered queryset of meeting notes
        """
        # For now, return all meeting notes since we're using AllowAny permissions
        # TODO: Filter by user when authentication is implemented
        queryset = MeetingNote.objects.all()
        application_id = self.kwargs.get('application_id')
        if application_id:
            queryset = queryset.filter(job_application_id=application_id)
        return queryset

    def perform_create(self, serializer):
        """
        Override create to validate the job application exists.
        """
        # Get the job_application from the validated data
        job_application = serializer.validated_data.get('job_application')
        if job_application:
            # job_application is already a JobApplication instance from the serializer
            serializer.save()
        else:
            raise serializers.ValidationError("Job application is required")


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Notification model.
    
    Provides CRUD operations for notifications.
    Users can only access their own notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for development

    def get_queryset(self):
        """
        Return notifications for the current user, filtering out future notifications.
        
        Returns:
            QuerySet: Filtered queryset of notifications
        """
        from django.utils import timezone
        
        # For now, return all notifications since we're using AllowAny permissions
        # TODO: Filter by user when authentication is implemented
        queryset = Notification.objects.all()
        
        # Filter out future notifications (only show current and past notifications)
        now = timezone.now()
        queryset = queryset.filter(
            show_date__lte=now,  # Only show notifications where show_date is now or in the past
            is_active=True       # Only show active notifications
        )
        
        print(f"DEBUG: Notification queryset count: {queryset.count()}")
        print(f"DEBUG: Current time: {now}")
        print(f"DEBUG: Filtered notifications:")
        for notification in queryset:
            print(f"  - ID: {notification.id}, Title: {notification.title}, Show Date: {notification.show_date}")
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        Mark a notification as read.
        
        Args:
            pk: Primary key of the notification to mark as read
            
        Returns:
            Response: JSON response confirming the action
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'Notification marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of unread notifications for the current user.
        
        Returns:
            Response: JSON response with unread count
        """
        queryset = self.get_queryset()
        unread_count = queryset.filter(is_read=False).count()
        return Response({'unread_count': unread_count})
