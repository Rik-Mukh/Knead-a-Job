"""
Job Tracker Models

This module contains Django models for job applications and resume management.
It defines the database schema for storing job application data and resume files.
"""

from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):
    """
    Model representing a job application.
    
    This model stores information about job applications including company details,
    position information, application status, and tracking data.
    """
    
    # Status choices for job applications
    STATUS_CHOICES = [
        ('applied', 'Applied'),           # Initial application submitted
        ('interview', 'Interview'),       # Interview scheduled or completed
        ('rejected', 'Rejected'),         # Application rejected
        ('accepted', 'Accepted'),         # Job offer received
        ('withdrawn', 'Withdrawn'),       # Application withdrawn by candidate
    ]
    
    # Core application fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who submitted this application")
    company_name = models.CharField(max_length=200, help_text="Name of the company")
    position = models.CharField(max_length=200, help_text="Job title or position name")
    job_url = models.URLField(blank=True, null=True, help_text="URL to the job posting")
    
    # Application tracking
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='applied',
        help_text="Current status of the application"
    )
    applied_date = models.DateField(help_text="Date when the application was submitted")
    
    # Additional information
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the application")
    # Follow-up response tracking
    meeting_minutes = models.TextField(blank=True, null=True, help_text="Meeting notes or interview minutes related to this job")

    salary_range = models.CharField(max_length=100, blank=True, null=True, help_text="Salary range if available")
    location = models.CharField(max_length=200, blank=True, null=True, help_text="Job location")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this record was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this record was last updated")
    
    class Meta:
        # Order applications by applied date (most recent first)
        ordering = ['-applied_date']
        # Ensure user cannot have duplicate applications for same company/position
        unique_together = ['user', 'company_name', 'position']
    
    def __str__(self):
        """String representation of the job application."""
        return f"{self.position} at {self.company_name}"
    
    @property
    def days_since_applied(self):
        """Calculate days since application was submitted."""
        from django.utils import timezone
        return (timezone.now().date() - self.applied_date).days


class Resume(models.Model):
    """
    Model representing a resume file.
    
    This model stores information about uploaded resume files,
    allowing users to manage multiple resume versions.
    """
    
    # Core resume fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who owns this resume")
    title = models.CharField(max_length=200, help_text="Descriptive title for the resume")
    file = models.FileField(upload_to='resumes/', help_text="The resume file")
    is_default = models.BooleanField(default=False, help_text="Whether this is the default resume for the user")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this resume was uploaded")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this resume was last updated")
    
    class Meta:
        # Order resumes by creation date (most recent first)
        ordering = ['-created_at']
        # Ensure user cannot have duplicate resume titles
        unique_together = ['user', 'title']
    
    def __str__(self):
        """String representation of the resume."""
        return f"{self.title} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure only one default resume per user.
        
        When a resume is set as default, all other resumes for the same user
        are automatically set to non-default.
        """
        # If this resume is set as default, unset all other default resumes for this user
        if self.is_default:
            Resume.objects.filter(user=self.user, is_default=True).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)
    
    @property
    def file_size(self):
        """Get the file size in a human-readable format."""
        if self.file:
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        return "Unknown"


class MeetingNote(models.Model):
    """
    Model representing a meeting note.
    
    This model stores information about meeting notes related to a job application.
    """
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, help_text="Job application related to this meeting note")
    content = models.TextField(help_text="Content of the meeting note")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this meeting note was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this meeting note was last updated")
    
    class Meta:
        # Order meeting notes by creation date (most recent first)
        ordering = ['-created_at']
