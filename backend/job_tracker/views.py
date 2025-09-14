"""
Job Tracker Views

This module contains Django REST Framework views for the job tracker API.
Views handle HTTP requests and return appropriate responses for job applications and resumes.
"""


from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, status, views, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import JobApplication, ResumeTemplate, Experience, Project, Education, MeetingNote, Notification
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .serializers import (
    ResumeTemplateSerializer, JobApplicationListSerializer, JobApplicationDetailSerializer, UserSerializer,
    ResumeTemplateCreateSerializer, ExperienceSerializer, ProjectSerializer, EducationSerializer, MeetingNoteSerializer, NotificationSerializer
)


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
        print(f"Update request data: {request.data}")
        print(f"Request method: {request.method}")
        
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
                skills=request.data.get('skills', ''),
                custom_markdown=request.data.get('custom_markdown', '')
            )
        else:
            # Update existing template
            for field in ['name', 'city', 'email', 'phone', 'links', 'summary', 'skills', 'custom_markdown']:
                if field in request.data:
                    print(f"Updating field {field} with value: {request.data[field]}")
                    setattr(template, field, request.data[field])
            template.save()
            print(f"Template saved successfully")
        
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
    
    @action(detail=False, methods=['get'])
    def generate(self, request):
        """Generate resume Markdown from all data."""
        try:
            # Get template data
            template = ResumeTemplate.get_or_create_template()
            
            # Check if custom markdown exists
            if template.custom_markdown:
                return Response({'markdown': template.custom_markdown})
            
            # Get all related data
            experiences = Experience.objects.all().order_by('-start_date')
            projects = Project.objects.all().order_by('-start_date')
            educations = Education.objects.all().order_by('-start_date')
            
            # Generate Markdown
            markdown = self._generate_resume_markdown(template, experiences, projects, educations)
            
            return Response({'markdown': markdown})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_resume_markdown(self, template, experiences, projects, educations):
        """Generate Markdown from resume data."""
        # Format experiences
        exp_text = ""
        for exp in experiences:
            exp_text += f"### {exp.position} | {exp.company}\n"
            if exp.is_current:
                exp_text += f"**{exp.start_date.strftime('%B %Y')} - Present**\n"
            else:
                exp_text += f"**{exp.start_date.strftime('%B %Y')} - {exp.end_date.strftime('%B %Y') if exp.end_date else 'Present'}**\n"
            if exp.location:
                exp_text += f"*{exp.location}*\n"
            exp_text += f"{exp.description}\n\n"
        
        # Format education
        edu_text = ""
        for edu in educations:
            edu_text += f"### {edu.degree} | {edu.institution}\n"
            if edu.is_current:
                edu_text += f"**{edu.start_date.strftime('%B %Y')} - Present**\n"
            else:
                edu_text += f"**{edu.start_date.strftime('%B %Y')} - {edu.end_date.strftime('%B %Y') if edu.end_date else 'Present'}**\n"
            if edu.field_of_study:
                edu_text += f"*{edu.field_of_study}*\n"
            if edu.gpa:
                edu_text += f"GPA: {edu.gpa}\n"
            edu_text += "\n"
        
        # Format projects
        proj_text = ""
        for proj in projects:
            proj_text += f"### {proj.name}\n"
            if proj.is_ongoing:
                proj_text += f"**{proj.start_date.strftime('%B %Y')} - Present**\n"
            else:
                proj_text += f"**{proj.start_date.strftime('%B %Y')} - {proj.end_date.strftime('%B %Y') if proj.end_date else 'Present'}**\n"
            proj_text += f"{proj.description}\n"
            if proj.technologies:
                proj_text += f"*Technologies: {proj.technologies}*\n"
            if proj.url:
                proj_text += f"[View Project]({proj.url})\n"
            proj_text += "\n"
        
        # Generate full Markdown
        markdown = f"""# {template.name}
{template.email} | {template.phone} | {template.city}

## Work Experience
{exp_text if exp_text else "No work experience added yet."}

## Education
{edu_text if edu_text else "No education added yet."}

## Projects
{proj_text if proj_text else "No projects added yet."}

## Skills
{template.skills if template.skills else "No skills added yet."}

## Professional Summary
{template.summary if template.summary else "No summary added yet."}
"""
        
        return markdown
    
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

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User model.
    
    Provides read-only access to user information.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only the current authenticated user.
        """
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get the current authenticated user.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

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
    
    def create(self, request, *args, **kwargs):
        """Create a new project with debug logging."""
        print(f"DEBUG: ProjectViewSet.create called")
        print(f"DEBUG: Request data: {request.data}")
        print(f"DEBUG: Request method: {request.method}")
        print(f"DEBUG: Content type: {request.content_type}")
        
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"DEBUG: Exception in create: {e}")
            print(f"DEBUG: Exception type: {type(e)}")
            raise
    
    def perform_create(self, serializer):
        """Create a new project entry - no template linking needed."""
        print(f"DEBUG: perform_create called with serializer data: {serializer.validated_data}")
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

