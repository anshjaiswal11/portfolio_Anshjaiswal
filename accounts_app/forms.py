from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
        'placeholder': 'Email address'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
        'placeholder': 'Last name'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['password1', 'password2']:
            self.fields[field_name].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
                'placeholder': 'Password' if field_name == 'password1' else 'Confirm password'
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500',
            'placeholder': 'Password'
        })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'profile_image', 'skills', 'title', 'location',
                  'github_url', 'linkedin_url', 'twitter_url', 'website_url',
                  'resume', 'education', 'experience']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your full name'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Short bio...'}),
            'skills': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, Django, React, ...'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Stack Developer'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City, Country'}),
            'github_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/username'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://linkedin.com/in/username'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://twitter.com/username'}),
            'website_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://yourwebsite.com'}),
            'education': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Education background...'}),
            'experience': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Work experience...'}),
        }
