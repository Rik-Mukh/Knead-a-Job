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
import openai
import os
import json


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
    
    @action(detail=False, methods=['get'])
    def generate_fresh(self, request):
        """Generate resume Markdown from database data, ignoring custom markdown."""
        try:
            # Get template data
            template = ResumeTemplate.get_or_create_template()
            
            # Get all related data
            experiences = Experience.objects.all().order_by('-start_date')
            projects = Project.objects.all().order_by('-start_date')
            educations = Education.objects.all().order_by('-start_date')
            
            # Generate Markdown from database data only
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


# AI Content Generation Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Allow unauthenticated for development
def generate_project_description(request):
    """
    Generate a project description using AI based on project name, technologies, and existing description.
    """
    print(f"Project description request received: {request.data}")
    try:
        data = request.data
        project_name = data.get('project_name', '')
        technologies = data.get('technologies', '')
        existing_description = data.get('existing_description', '')
        
        if not project_name:
            return Response(
                {'error': 'Project name is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set up OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError('OPENAI_API_KEY environment variable is not set')
        
        print(f"Initializing OpenAI client with API key: {api_key[:10]}...")
        try:
            # Initialize client with minimal configuration to avoid conflicts
            client = openai.OpenAI(
                api_key=api_key,
                timeout=30.0
            )
            print("OpenAI client initialized successfully")
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {str(e)}")
            raise ValueError(f'Failed to initialize OpenAI client: {str(e)}')
        
        # Build context for the prompt
        context_parts = []
        if project_name:
            context_parts.append(f"Project name: {project_name}")
        if technologies:
            context_parts.append(f"Technologies used: {technologies}")
        if existing_description:
            context_parts.append(f"Current description: {existing_description}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""Generate a professional project description for a resume based on the following information:

{context}

Please write a compelling project description that:
1. Clearly explains what the project does
2. Highlights the technologies used
3. Emphasizes the developer's role and contributions
4. Uses action-oriented language
5. Is concise but informative (2-3 sentences)
6. Start with a strong action verb or phrase
7. Use bullet points for the description

If there's an existing description, use it as a base and enhance it. If not, create a new description from scratch.

Return only the description text, no additional formatting or explanations."""

        print(f"Sending request to OpenAI with model: gpt-4o-mini")
        print(f"Prompt length: {len(prompt)} characters")
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer specializing in software development projects."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=200
            )
            print(f"OpenAI API response received: {response.choices[0].message.content[:100]}...")
        except Exception as e:
            print(f"OpenAI API call failed: {str(e)}")
            raise e
        
        generated_description = response.choices[0].message.content.strip()
        
        print(f"Returning generated description: {generated_description[:100]}...")
        return Response({
            'generated_description': generated_description
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate project description: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Allow unauthenticated for development
def generate_experience_summary(request):
    """
    Generate an experience summary using AI based on form data and existing description.
    Requires at least 500 characters of existing content.
    """
    try:
        data = request.data
        company = data.get('company', '')
        position = data.get('position', '')
        existing_description = data.get('existing_description', '')
        
        # Validate minimum character requirement
        if len(existing_description) < 500:
            return Response(
                {'error': 'Please provide at least 500 characters of existing experience description before generating AI content'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not company or not position:
            return Response(
                {'error': 'Company and position are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set up OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError('OPENAI_API_KEY environment variable is not set')
        
        try:
            # Initialize client with minimal configuration to avoid conflicts
            client = openai.OpenAI(
                api_key=api_key,
                timeout=30.0
            )
        except Exception as e:
            raise ValueError(f'Failed to initialize OpenAI client: {str(e)}')
        
        prompt = f"""Generate an enhanced professional experience description for a resume based on the following information:

Company: {company}
Position: {position}
Current description: {existing_description}

Please enhance the existing description by:
1. Improving clarity and professional tone
2. Adding quantifiable achievements where possible
3. Using strong action verbs
4. Making it more compelling for employers
5. Maintaining the original content but making it more polished
6. Start with a strong action verb or phrase
7. Use bullet points for the description

Return only the enhanced description text, no additional formatting or explanations."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume writer specializing in enhancing work experience descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=300
        )
        
        generated_description = response.choices[0].message.content.strip()
        
        return Response({
            'generated_description': generated_description
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate experience summary: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Allow unauthenticated for development
def generate_personal_summary(request):
    """
    Generate a personal summary using AI based on existing summary and user data.
    """
    try:
        data = request.data
        existing_summary = data.get('existing_summary', '')
        name = data.get('name', '')
        skills = data.get('skills', '')
        
        # Set up OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError('OPENAI_API_KEY environment variable is not set')
        
        try:
            # Initialize client with minimal configuration to avoid conflicts
            client = openai.OpenAI(
                api_key=api_key,
                timeout=30.0
            )
        except Exception as e:
            raise ValueError(f'Failed to initialize OpenAI client: {str(e)}')
        
        # Build context for the prompt
        context_parts = []
        if name:
            context_parts.append(f"Name: {name}")
        if skills:
            context_parts.append(f"Skills: {skills}")
        if existing_summary:
            context_parts.append(f"Current summary: {existing_summary}")
        
        context = "\n".join(context_parts) if context_parts else "No existing information provided"
        
        prompt = f"""Generate a professional summary for a resume based on the following information:

{context}

Please create or enhance a professional summary that:
1. Highlights key skills and expertise
2. Shows career focus and objectives
3. Is concise (2-4 sentences)
4. Uses professional language
5. Appeals to potential employers

If there's an existing summary, enhance it. If not, create a new one based on the provided information.

Return only the summary text, no additional formatting or explanations."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume writer specializing in creating compelling professional summaries."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=150
        )
        
        generated_summary = response.choices[0].message.content.strip()
        
        return Response({
            'generated_summary': generated_summary
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate personal summary: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

