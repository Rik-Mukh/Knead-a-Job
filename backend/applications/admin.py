from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['position', 'company_name', 'status', 'applied_date', 'user']
    list_filter = ['status', 'applied_date', 'user']
    search_fields = ['position', 'company_name', 'notes']
    date_hierarchy = 'applied_date'
