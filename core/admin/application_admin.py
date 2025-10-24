from django.contrib import admin
from core.models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface for Application model
    """
    list_display = ('name', 'parent', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('parent', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    autocomplete_fields = ('parent',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'description', 'parent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
        ('Additional Properties', {
            'fields': ('properties',),
            'classes': ('collapse',),
        }),
    )