from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.TextField(blank=True, help_text='Comma-separated list of skills')
    title = models.CharField(max_length=200, blank=True, default='Full Stack Developer')
    location = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
