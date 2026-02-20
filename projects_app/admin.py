from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description', 'tech_stack']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'order']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'short_description', 'description', 'image')
        }),
        ('Technical Details', {
            'fields': ('tech_stack', 'github_link', 'live_demo_link')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
