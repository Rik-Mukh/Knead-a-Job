"""
Job Tracker Admin Configuration

This module configures the Django admin interface for job tracker models.
It defines how models are displayed and managed in the admin panel.
"""

from django.contrib import admin
from .models import JobApplication, ResumeTemplate, Experience, Project, Education, MeetingNote, Notification


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
            'fields': ('notes', 'meeting_minutes')
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
    list_display = ['name', 'email', 'city', 'phone', 'updated_at']
    
    # Fields to filter by in the admin interface
    list_filter = ['created_at', 'updated_at']
    
    # Fields to search by
    search_fields = ['name', 'email', 'city', 'phone']
    
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


# Inline classes removed - models no longer have foreign key to ResumeTemplate


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Experience model.
    """
    
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['company', 'position']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Experience Details', {
            'fields': ('company', 'position', 'location', 'start_date', 'end_date', 'is_current')
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
    
    list_display = ['name', 'technologies', 'start_date', 'end_date', 'is_ongoing']
    list_filter = ['is_ongoing', 'start_date']
    search_fields = ['name', 'technologies']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Project Details', {
            'fields': ('name', 'description', 'technologies', 'url', 'start_date', 'end_date', 'is_ongoing')
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
    
    list_display = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['institution', 'degree', 'field_of_study']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Education Details', {
            'fields': ('institution', 'degree', 'field_of_study', 'location', 'start_date', 'end_date', 'is_current')
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


@admin.register(MeetingNote)
class MeetingNoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for MeetingNote model.
    
    Defines how meeting notes are displayed and managed in the admin interface.
    """
    
    # Fields to display in the list view
    list_display = ['job_application', 'content_preview', 'created_at']
    
    # Fields to filter by in the admin interface
    list_filter = ['created_at', 'job_application__status', 'job_application__user']
    
    # Fields to search by
    search_fields = ['content', 'job_application__position', 'job_application__company_name']
    
    # Enable date-based filtering
    date_hierarchy = 'created_at'
    
    # Make certain fields read-only
    readonly_fields = ['created_at', 'updated_at']
    
    # Group related fields together
    fieldsets = (
        ('Meeting Note Information', {
            'fields': ('job_application', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        """Return a preview of the content (first 50 characters)."""
        if not obj.content:
            return "No content"
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification model.
    
    Defines how notifications are displayed and managed in the admin interface.
    """
    
    # Fields to display in the list view
    list_display = ['title', 'user', 'job_application', 'show_date', 'is_read', 'is_active', 'created_at']
    
    # Fields to filter by in the admin interface
    list_filter = ['is_read', 'is_active', 'show_date', 'created_at', 'user']
    
    # Fields to search by
    search_fields = ['title', 'message', 'user__username', 'job_application__position', 'job_application__company_name']
    
    # Enable date-based filtering
    date_hierarchy = 'show_date'  # Changed from 'created_at' to 'show_date'
    
    # Make certain fields read-only
    readonly_fields = ['created_at', 'updated_at', 'should_show']
    
    # Group related fields together
    fieldsets = (
        ('Notification Information', {
            'fields': ('user', 'job_application', 'title', 'message')
        }),
        ('Display Settings', {
            'fields': ('show_date', 'is_read', 'is_active')  # Changed from 'Notification Settings'
        }),
        ('System Information', {
            'fields': ('should_show', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Add custom actions
    actions = ['mark_as_read', 'mark_as_unread', 'activate_notifications', 'deactivate_notifications']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = 'Mark selected notifications as unread'
    
    def activate_notifications(self, request, queryset):
        """Activate selected notifications."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} notifications activated.')
    activate_notifications.short_description = 'Activate selected notifications'
    
    def deactivate_notifications(self, request, queryset):
        """Deactivate selected notifications."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} notifications deactivated.')
    deactivate_notifications.short_description = 'Deactivate selected notifications'
