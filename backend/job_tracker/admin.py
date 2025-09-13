"""
Job Tracker Admin Configuration

This module configures the Django admin interface for job tracker models.
It defines how models are displayed and managed in the admin panel.
"""

from django.contrib import admin
from .models import JobApplication, ResumeTemplate, Experience, Project, Education


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


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    """
    Admin configuration for ResumeTemplate model.
    
    Defines how resume templates are displayed and managed in the admin interface.
    """
    
    # Fields to display in the list view
    list_display = ['name', 'email', 'city', 'user', 'updated_at']
    
    # Fields to filter by in the admin interface
    list_filter = ['created_at', 'updated_at', 'user']
    
    # Fields to search by
    search_fields = ['name', 'email', 'user__username']
    
    # Enable date-based filtering
    date_hierarchy = 'updated_at'
    
    # Make certain fields read-only
    readonly_fields = ['created_at', 'updated_at']
    
    # Group related fields together
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'email', 'phone', 'city')
        }),
        ('Professional Information', {
            'fields': ('summary', 'skills', 'links')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ExperienceInline(admin.TabularInline):
    """Inline admin for Experience model."""
    model = Experience
    extra = 1
    fields = ['company', 'position', 'start_date', 'end_date', 'is_current', 'order']


class ProjectInline(admin.TabularInline):
    """Inline admin for Project model."""
    model = Project
    extra = 1
    fields = ['name', 'technologies', 'start_date', 'end_date', 'is_ongoing', 'order']


class EducationInline(admin.TabularInline):
    """Inline admin for Education model."""
    model = Education
    extra = 1
    fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current', 'order']


# Update ResumeTemplateAdmin to include inlines
ResumeTemplateAdmin.inlines = [ExperienceInline, ProjectInline, EducationInline]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Experience model.
    """
    
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current', 'resume_template']
    list_filter = ['is_current', 'start_date', 'resume_template__user']
    search_fields = ['company', 'position', 'resume_template__user__username']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Experience Details', {
            'fields': ('resume_template', 'company', 'position', 'location', 'start_date', 'end_date', 'is_current')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Ordering', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for Project model.
    """
    
    list_display = ['name', 'technologies', 'start_date', 'end_date', 'is_ongoing', 'resume_template']
    list_filter = ['is_ongoing', 'start_date', 'resume_template__user']
    search_fields = ['name', 'technologies', 'resume_template__user__username']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Project Details', {
            'fields': ('resume_template', 'name', 'description', 'technologies', 'url', 'start_date', 'end_date', 'is_ongoing')
        }),
        ('Ordering', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Education model.
    """
    
    list_display = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_current', 'resume_template']
    list_filter = ['is_current', 'start_date', 'resume_template__user']
    search_fields = ['institution', 'degree', 'field_of_study', 'resume_template__user__username']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Education Details', {
            'fields': ('resume_template', 'institution', 'degree', 'field_of_study', 'location', 'start_date', 'end_date', 'is_current')
        }),
        ('Academic Information', {
            'fields': ('gpa',)
        }),
        ('Ordering', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
