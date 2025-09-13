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


class ResumeTemplate(models.Model):
    """
    Model representing a resume template.
    
    Only one template can exist in the system (singleton pattern).
    Contains personal information and serves as the base for generating resumes.
    """
    
    # Personal Information
    name = models.CharField(max_length=200, help_text="Full name")
    city = models.CharField(max_length=100, help_text="City of residence")
    email = models.EmailField(help_text="Email address")
    phone = models.CharField(max_length=20, help_text="Phone number")
    links = models.TextField(
        blank=True, 
        null=True, 
        help_text="Links (GitHub, LinkedIn, portfolio, etc.) - one per line"
    )
    
    # Professional Information
    summary = models.TextField(
        blank=True, 
        null=True, 
        help_text="Professional summary or objective"
    )
    skills = models.TextField(
        blank=True, 
        null=True, 
        help_text="Skills - one per line or comma-separated"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this template was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this template was last updated")
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        """String representation of the resume template."""
        return f"Resume Template - {self.name or 'Untitled'}"
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure only one template exists.
        If a template already exists, update it instead of creating a new one.
        """
        if not self.pk and ResumeTemplate.objects.exists():
            # If this is a new template and one already exists, update the existing one
            existing = ResumeTemplate.objects.first()
            existing.name = self.name
            existing.city = self.city
            existing.email = self.email
            existing.phone = self.phone
            existing.links = self.links
            existing.summary = self.summary
            existing.skills = self.skills
            existing.save()
            return existing
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_or_create_template(cls):
        """
        Get the existing template or create a new one if none exists.
        Returns the single template instance.
        """
        template, created = cls.objects.get_or_create(
            pk=1,  # Use a fixed primary key to ensure singleton
            defaults={
                'name': '',
                'city': '',
                'email': '',
                'phone': '',
                'links': '',
                'summary': '',
                'skills': ''
            }
        )
        return template


class Experience(models.Model):
    """
    Model representing work experience entries.
    
    Experience entries are stored independently without template association.
    """
    
    # Experience details
    company = models.CharField(max_length=200, help_text="Company name")
    position = models.CharField(max_length=200, help_text="Job title or position")
    location = models.CharField(max_length=200, blank=True, null=True, help_text="Work location")
    start_date = models.DateField(help_text="Start date of employment")
    end_date = models.DateField(blank=True, null=True, help_text="End date (leave blank if current)")
    is_current = models.BooleanField(default=False, help_text="Is this current position?")
    description = models.TextField(help_text="Job description and responsibilities")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, help_text="Order of display (higher numbers first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this experience was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this experience was last updated")
    
    class Meta:
        ordering = ['-order', '-start_date']
        unique_together = ['company', 'position', 'start_date']
    
    def __str__(self):
        """String representation of the experience."""
        return f"{self.position} at {self.company}"


class Project(models.Model):
    """
    Model representing project entries.
    
    Project entries are stored independently without template association.
    """
    
    # Project details
    name = models.CharField(max_length=200, help_text="Project name")
    description = models.TextField(help_text="Project description")
    technologies = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        help_text="Technologies used (comma-separated)"
    )
    url = models.URLField(blank=True, null=True, help_text="Project URL or repository")
    start_date = models.DateField(help_text="Project start date")
    end_date = models.DateField(blank=True, null=True, help_text="Project end date")
    is_ongoing = models.BooleanField(default=False, help_text="Is this project ongoing?")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, help_text="Order of display (higher numbers first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this project was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this project was last updated")
    
    class Meta:
        ordering = ['-order', '-start_date']
        unique_together = ['name', 'start_date']
    
    def __str__(self):
        """String representation of the project."""
        return f"{self.name}"


class Education(models.Model):
    """
    Model representing education entries.
    
    Education entries are stored independently without template association.
    """
    
    # Education details
    institution = models.CharField(max_length=200, help_text="School or university name")
    degree = models.CharField(max_length=200, help_text="Degree or certification")
    field_of_study = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text="Field of study or major"
    )
    location = models.CharField(max_length=200, blank=True, null=True, help_text="Institution location")
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(blank=True, null=True, help_text="End date or graduation date")
    gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="GPA (if applicable)"
    )
    is_current = models.BooleanField(default=False, help_text="Is this current education?")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, help_text="Order of display (higher numbers first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this education was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this education was last updated")
    
    class Meta:
        ordering = ['-order', '-start_date']
        unique_together = ['institution', 'degree', 'start_date']
    
    def __str__(self):
        """String representation of the education."""
        return f"{self.degree} from {self.institution}"



