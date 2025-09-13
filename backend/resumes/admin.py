from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at', 'user']
    search_fields = ['title', 'user__username']
    date_hierarchy = 'created_at'
