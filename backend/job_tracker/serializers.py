from rest_framework import serializers

from django.contrib.auth.models import User
from .models import JobApplication, ResumeTemplate, Experience, Project, Education, MeetingNote, Notification


class MeetingNoteSerializer(serializers.ModelSerializer):
    """
    Serializer for MeetingNote model.
    """

    class Meta:
        model = MeetingNote
        fields = ['id', 'job_application', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        print(f"DEBUG: MeetingNoteSerializer.create called with: {validated_data}")
        return super().create(validated_data)

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Meeting note content cannot be empty.")
        return value.strip()


# -------------------------------
# Job Application Serializers
# -------------------------------

class JobApplicationListSerializer(serializers.ModelSerializer):
    # Reverse relation without related_name – use default meetingnote_set
    meetingnote_set = MeetingNoteSerializer(many=True, read_only=True)

    class Meta:
        model = JobApplication
        exclude = ['meeting_minutes']  # assuming this is a field you added
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Automatically assign the user from the request context
        # For development, create a default user if none exists
        user = self.context['request'].user
        if not user.is_authenticated:
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='halalkingxi',
                defaults={'email': 'rik@ualberta.ca', 'first_name': 'Rik', 'last_name': 'Mukherji'}
            )
        validated_data['user'] = user
        return super().create(validated_data)


class JobApplicationDetailSerializer(serializers.ModelSerializer):
    meetingnote_set = MeetingNoteSerializer(many=True, read_only=True)

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Automatically assign the user from the request context
        # For development, create a default user if none exists
        user = self.context['request'].user
        if not user.is_authenticated:
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='halalkingxi',
                defaults={'email': 'rik@ualberta.ca', 'first_name': 'Rik', 'last_name': 'Mukherji'}
            )
        validated_data['user'] = user
        return super().create(validated_data)

    def validate_applied_date(self, value):
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Applied date cannot be in the future.")
        return value

class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for Experience model.

    - Converts empty-string end_date ("") to None.
    - Validates end_date rules based on is_current.
    """

    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {
            "location": {"required": False, "allow_blank": True},
            "end_date": {"required": False, "allow_null": True},
            "description": {"required": True},
        }

    # 1) Normalize payload before field parsing:
    #    Convert "" -> None for end_date so DateField doesn't error.
    def to_internal_value(self, data):
        data = dict(data) if data is not None else {}
        if data.get("end_date", "") == "":
            data["end_date"] = None
        return super().to_internal_value(data)

    # 2) Cross-field validation for dates and current flag.
    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        current = attrs.get("is_current")

        # If current position, force end_date to None
        if current:
            attrs["end_date"] = None
        else:
            # If not current, require an end_date
            if end is None:
                raise serializers.ValidationError({
                    "end_date": "End date is required unless this is your current position."
                })
                
            if start and attrs.get("end_date") and attrs["end_date"] < start:
                raise serializers.ValidationError({
                    "end_date": "End date cannot be before start date."
                })
        return attrs





class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    
    Provides basic user information for the frontend.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']# -------------------------------
# Notification Serializer
# -------------------------------

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    should_show = serializers.ReadOnlyField()
    job_application_title = serializers.CharField(source='job_application.position', read_only=True)
    job_application_company = serializers.CharField(source='job_application.company_name', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'job_application', 'job_application_title', 'job_application_company',
            'title', 'message', 'show_date', 'is_read', 'is_active',
            'created_at', 'updated_at', 'should_show'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'should_show']

    def create(self, validated_data):
        # Automatically assign the user from the request context
        user = self.context['request'].user
        if not user.is_authenticated:
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='halalkingxi',
                defaults={'email': 'rik@ualberta.ca', 'first_name': 'Rik', 'last_name': 'Mukherji'}
            )
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """Override to add debugging information."""
        data = super().to_representation(instance)
        print(f"DEBUG: Serializing notification {instance.id}: {data}")
        return data



class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    
    Handles serialization and deserialization of project data.
    Projects are stored independently without template association.
    """
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def to_internal_value(self, data):
        """Convert empty strings to None for optional fields."""
        print(f"DEBUG: ProjectSerializer.to_internal_value called with data: {data}")
        data = dict(data) if data is not None else {}
        
        # Convert empty strings to None for optional fields
        if data.get('technologies', '') == '':
            data['technologies'] = None
        if data.get('url', '') == '':
            data['url'] = None
        if data.get('end_date', '') == '':
            data['end_date'] = None
            
        print(f"DEBUG: ProjectSerializer.to_internal_value processed data: {data}")
        result = super().to_internal_value(data)
        print(f"DEBUG: ProjectSerializer.to_internal_value result: {result}")
        return result
    
    def validate(self, attrs):
        """Validate project data."""
        print(f"DEBUG: ProjectSerializer.validate called with attrs: {attrs}")
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        is_ongoing = attrs.get('is_ongoing', False)
        
        print(f"DEBUG: start_date: {start_date}, end_date: {end_date}, is_ongoing: {is_ongoing}")
        
        # If project is ongoing, force end_date to None
        if is_ongoing:
            attrs['end_date'] = None
        else:
            # If not ongoing and end_date is provided, validate it's after start_date
            if start_date and end_date and end_date < start_date:
                print(f"DEBUG: Validation error - end_date before start_date")
                raise serializers.ValidationError({
                    'end_date': 'End date cannot be before start date.'
                })
                
        print(f"DEBUG: ProjectSerializer.validate final attrs: {attrs}")
        return attrs


class EducationSerializer(serializers.ModelSerializer):
    """
    Serializer for Education model.
    
    Handles serialization and deserialization of education data.
    Education entries are stored independently without template association.
    """
    
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ResumeTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for ResumeTemplate model.
    
    Handles serialization and deserialization of resume template data.
    Includes nested serializers for related experiences, projects, and education.
    """
    
    experiences = ExperienceSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    
    class Meta:
        model = ResumeTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        """Create or update the singleton template."""
        return ResumeTemplate.get_or_create_template()
    
    def update(self, instance, validated_data):
        """Update the singleton template."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def validate_email(self, value):
        """Validate email format."""
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value
    
    def validate_phone(self, value):
        """Validate phone number format."""
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        return value


class ResumeTemplateCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating resume templates.
    
    Used when creating a new resume template without nested data.
    """
    
    class Meta:
        model = ResumeTemplate
        fields = ['name', 'city', 'email', 'phone', 'links', 'summary', 'skills', 'custom_markdown']
    
    def create(self, validated_data):
        """Create or update the singleton template."""
        template = ResumeTemplate.get_or_create_template()
        for attr, value in validated_data.items():
            setattr(template, attr, value)
        template.save()
        return template




