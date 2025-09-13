"""
Job Tracker Serializers

This module contains Django REST Framework serializers for the job tracker models.
Serializers handle the conversion between model instances and JSON data for API responses.
"""

from rest_framework import serializers
from .models import JobApplication, Resume, MeetingNote

# two serializers for the job application model so that meeting mins doesn't show on the dashboard appear on dashbaord
    # For Dashboard/List views – hides meeting_minutes
class JobApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        exclude = ['meeting_minutes']
        read_only_fields = ('user', 'created_at', 'updated_at')


# For Detail/Edit views – shows full fields including meeting_minutes
class JobApplicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    
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


class MeetingNoteSerializer(serializers.ModelSerializer):
    """
    Serializer for MeetingNote model.
    
    Handles serialization and deserialization of meeting note data.
    """
    
    class Meta:
        model = MeetingNote
        fields = ['id', 'job_application', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Override create method to handle job_application assignment.
        """
        print(f"DEBUG: MeetingNoteSerializer.create called with: {validated_data}")
        return super().create(validated_data)
    
    def validate_content(self, value):
        """
        Validate the meeting note content.
        
        Args:
            value: The content value
            
        Returns:
            str: The validated content
            
        Raises:
            serializers.ValidationError: If the content is invalid
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Meeting note content cannot be empty.")
        return value.strip()

