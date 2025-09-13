"""
Job Tracker Admin Configuration

This module configures the Django admin interface for job tracker models.
It defines how models are displayed and managed in the admin panel.
"""

from django.contrib import admin
from .models import JobApplication, Resume


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """
    Admin configuration for JobApplication model.
    
    Defines how job applications are displayed and managed in the admin interface.
    """
    
    # Fields to display in the list view
    list_display = ['position', 'company_name', 'status', 'applied_date', 'user']
    
    # Fields to filter by in the admin interface
    list_filter = ['status', 'applied_date', 'user', 'created_at']
    
    # Fields to search by
    search_fields = ['position', 'company_name', 'notes', 'user__username']
    
    # Enable date-based filtering
    date_hierarchy = 'applied_date'
    
    # Make certain fields read-only
    readonly_fields = ['created_at', 'updated_at']
    
    # Group related fields together
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'position', 'job_url')
        }),
        ('Application Details', {
            'fields': ('status', 'applied_date', 'location', 'salary_range')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Resume model.
    
    Defines how resumes are displayed and managed in the admin interface.
    """
    
    # Fields to display in the list view
    list_display = ['title', 'user', 'is_default', 'created_at']
    
    # Fields to filter by in the admin interface
    list_filter = ['is_default', 'created_at', 'user']
    
    # Fields to search by
    search_fields = ['title', 'user__username']
    
    # Enable date-based filtering
    date_hierarchy = 'created_at'
    
    # Make certain fields read-only
    readonly_fields = ['created_at', 'updated_at']
    
    # Group related fields together
    fieldsets = (
        ('Resume Information', {
            'fields': ('user', 'title', 'file', 'is_default')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
