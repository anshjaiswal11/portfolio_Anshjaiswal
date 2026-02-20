from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('projects/', views.projects_list_view, name='projects_list'),
    path('projects/new/', views.project_create_view, name='project_create'),
    path('projects/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('projects/<slug:slug>/edit/', views.project_edit_view, name='project_edit'),
    path('projects/<slug:slug>/delete/', views.project_delete_view, name='project_delete'),
]
