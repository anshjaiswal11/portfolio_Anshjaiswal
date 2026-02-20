from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm
from accounts_app.models import Profile
from django.contrib.auth.models import User


def home_view(request):
    featured_projects = Project.objects.filter(is_featured=True).order_by('order')[:3]
    all_projects = Project.objects.all().order_by('-created_at')[:6]
    profile = Profile.objects.filter(user__is_superuser=True).first()
    context = {
        'featured_projects': featured_projects,
        'recent_projects': all_projects,
        'profile': profile,
    }
    return render(request, 'home.html', context)


def about_view(request):
    profile = Profile.objects.filter(user__is_superuser=True).first()
    return render(request, 'about.html', {'profile': profile})


def projects_list_view(request):
    projects = Project.objects.all().order_by('-created_at')
    tech_filter = request.GET.get('tech', '')
    if tech_filter:
        projects = projects.filter(tech_stack__icontains=tech_filter)
    return render(request, 'projects/list.html', {
        'projects': projects,
        'tech_filter': tech_filter,
    })


def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(pk=project.pk).order_by('-created_at')[:3]
    return render(request, 'projects/detail.html', {
        'project': project,
        'related_projects': related_projects,
    })


@login_required
def project_create_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Only admin users can create projects.')
        return redirect('projects_list')
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.title}" created successfully!')
            return redirect('project_detail', slug=project.slug)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProjectForm()
    return render(request, 'projects/form.html', {'form': form, 'action': 'Create'})


@login_required
def project_edit_view(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Only admin users can edit projects.')
        return redirect('projects_list')
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.title}" updated successfully!')
            return redirect('project_detail', slug=project.slug)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/form.html', {'form': form, 'action': 'Edit', 'project': project})


@login_required
def project_delete_view(request, slug):
    if not request.user.is_staff:
        messages.error(request, 'Only admin users can delete projects.')
        return redirect('projects_list')
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted successfully!')
        return redirect('projects_list')
    return render(request, 'projects/confirm_delete.html', {'project': project})
