from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/login/', views.api_login, name='api_login'),
    path('auth/logout/', views.api_logout, name='api_logout'),
    path('auth/profile/', views.api_profile, name='api_user_profile'),

    # Projects
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='api_projects_list'),
    path('projects/featured/', views.FeaturedProjectsAPIView.as_view(), name='api_projects_featured'),
    path('projects/<slug:slug>/', views.ProjectDetailAPIView.as_view(), name='api_project_detail'),

    # Contact
    path('contact/', views.ContactMessageCreateAPIView.as_view(), name='api_contact'),

    # Profile
    path('profile/', views.ProfileAPIView.as_view(), name='api_portfolio_profile'),
]
