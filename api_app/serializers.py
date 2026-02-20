from rest_framework import serializers
from projects_app.models import Project
from contact_app.models import ContactMessage
from accounts_app.models import Profile


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'tech_stack', 'tech_list', 'github_link', 'live_demo_link',
            'image', 'is_featured', 'order', 'created_at', 'updated_at', 'url'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_tech_list(self, obj):
        return obj.get_tech_list()

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Title must be at least 3 characters long.')
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Description must be at least 10 characters long.')
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        if not '@' in value:
            raise serializers.ValidationError('Enter a valid email address.')
        return value

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Message must be at least 10 characters long.')
        return value


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'email', 'name', 'bio', 'title', 'location',
            'skills', 'skills_list', 'github_url', 'linkedin_url', 'twitter_url',
            'website_url', 'profile_image', 'education', 'experience'
        ]

    def get_skills_list(self, obj):
        return obj.get_skills_list()
