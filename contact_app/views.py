from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            # Send email to admin
            try:
                send_mail(
                    subject=f'[Portfolio Contact] {contact_msg.subject or "New Message"} from {contact_msg.name}',
                    message=f'''
New contact message received:

Name: {contact_msg.name}
Email: {contact_msg.email}
Subject: {contact_msg.subject or "N/A"}

Message:
{contact_msg.message}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
                # Send confirmation to user
                send_mail(
                    subject='Thank you for reaching out!',
                    message=f'''
Hi {contact_msg.name},

Thank you for your message! I've received it and will get back to you as soon as possible.

Here's a copy of your message:
---
{contact_msg.message}
---

Best regards,
Portfolio Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact_msg.email],
                    fail_silently=True,
                )
            except Exception as e:
                pass  # Email sending is non-critical

            messages.success(request, 'Your message has been sent! I\'ll get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})
