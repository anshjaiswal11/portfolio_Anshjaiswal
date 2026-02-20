from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 6,
                'placeholder': 'Write your message here...',
                'required': True
            }),
        }
