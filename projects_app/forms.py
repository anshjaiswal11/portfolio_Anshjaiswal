from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'short_description', 'description', 'tech_stack',
                  'github_link', 'live_demo_link', 'image', 'is_featured', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Project title'}),
            'short_description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief description (max 300 chars)'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 6, 'placeholder': 'Detailed project description...'}),
            'tech_stack': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, Django, PostgreSQL, React...'}),
            'github_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/...'}),
            'live_demo_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
