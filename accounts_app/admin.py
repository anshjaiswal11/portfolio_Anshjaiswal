from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'title', 'location', 'created_at']
    search_fields = ['user__username', 'name', 'bio', 'skills']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
