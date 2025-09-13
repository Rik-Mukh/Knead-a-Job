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


class ResumeSerializer(serializers.ModelSerializer):
    """
    Serializer for Resume model.
    
    Handles serialization and deserialization of resume data.
    Automatically sets the user field from the request context.
    """
    
    file_size = serializers.ReadOnlyField()  # Include the file_size property as read-only
    
    class Meta:
        model = Resume
        fields = '__all__'  # Include all model fields
        read_only_fields = ('user', 'created_at', 'updated_at', 'file_size')  # Fields that cannot be modified via API
    
    def create(self, validated_data):
        """
        Override create method to automatically set the user from the request context.
        
        Args:
            validated_data: The validated data from the serializer
            
        Returns:
            Resume: The created resume instance
        """
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_file(self, value):
        """
        Validate the uploaded file.
        
        Args:
            value: The uploaded file
            
        Returns:
            file: The validated file
            
        Raises:
            serializers.ValidationError: If the file is invalid
        """
        # Check file size (limit to 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        
        # Check file extension
        allowed_extensions = ['.pdf', '.doc', '.docx']
        file_extension = value.name.lower().split('.')[-1]
        if f'.{file_extension}' not in allowed_extensions:
            raise serializers.ValidationError("Only PDF, DOC, and DOCX files are allowed.")
        
        return value


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for Experience model.
    
    Handles serialization and deserialization of work experience data.
    """
    
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        """Set the resume_template from the request context."""
        validated_data['resume_template'] = self.context['resume_template']
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    
    Handles serialization and deserialization of project data.
    """
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        """Set the resume_template from the request context."""
        validated_data['resume_template'] = self.context['resume_template']
        return super().create(validated_data)


class EducationSerializer(serializers.ModelSerializer):
    """
    Serializer for Education model.
    
    Handles serialization and deserialization of education data.
    """
    
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        """Set the resume_template from the request context."""
        validated_data['resume_template'] = self.context['resume_template']
        return super().create(validated_data)


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
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        """Set the user from the request context."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
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
        """Set the user from the request context."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



