from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_path'),
    path('register/', views.register_view, name='register_path'),
    path('logout/', views.logout_view, name='logout_path'),
    path('profile/<int:user_id>/', views.show_profile_view, name='show_profile_path'),
    path('profile/edit/<int:pk>/', views.EditProfileView.as_view(), name='edit_profile_activate'),
]
