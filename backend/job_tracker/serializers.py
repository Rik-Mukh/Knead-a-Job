from rest_framework import serializers
from .models import JobApplication, Resume, MeetingNote
from django.contrib.auth.models import User

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


# -------------------------------
# Resume Serializer
# -------------------------------

class ResumeSerializer(serializers.ModelSerializer):
    file_size = serializers.ReadOnlyField()

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'file_size')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB.")

        allowed_extensions = ['.pdf', '.doc', '.docx']
        file_extension = value.name.lower().split('.')[-1]
        if f'.{file_extension}' not in allowed_extensions:
            raise serializers.ValidationError("Only PDF, DOC, and DOCX files are allowed.")

        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    
    Provides basic user information for the frontend.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']