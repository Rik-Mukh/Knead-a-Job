"""
Job Tracker Serializers

This module contains Django REST Framework serializers for the job tracker models.
Serializers handle the conversion between model instances and JSON data for API responses.
"""

from rest_framework import serializers
from .models import JobApplication, ResumeTemplate, Experience, Project, Education


class JobApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for JobApplication model.
    
    Handles serialization and deserialization of job application data.
    Automatically sets the user field from the request context.
    """
    
    class Meta:
        model = JobApplication
        fields = '__all__'  # Include all model fields
        read_only_fields = ('user', 'created_at', 'updated_at')  # Fields that cannot be modified via API
    
    def create(self, validated_data):
        """
        Override create method to automatically set the user from the request context.
        
        Args:
            validated_data: The validated data from the serializer
            
        Returns:
            JobApplication: The created job application instance
        """
        # Set the user from the request context
        return super().create(validated_data)
    
    def validate_applied_date(self, value):
        """
        Validate that the applied date is not in the future.
        
        Args:
            value: The applied date value
            
        Returns:
            date: The validated applied date
            
        Raises:
            serializers.ValidationError: If the date is in the future
        """
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

        # Order check
        if start and attrs.get("end_date") and attrs["end_date"] < start:
            raise serializers.ValidationError({
                "end_date": "End date cannot be before start date."
            })
        return attrs

    # No resume_template logic needed - experiences are independent

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
        fields = ['name', 'city', 'email', 'phone', 'links', 'summary', 'skills']
    
    def create(self, validated_data):
        """Create or update the singleton template."""
        template = ResumeTemplate.get_or_create_template()
        for attr, value in validated_data.items():
            setattr(template, attr, value)
        template.save()
        return template



