from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth URLs[cite: 3]
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_kwarg('registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    
    # Dashboard & Logic
    path('', views.dashboard, name='dashboard'),
    
    # Admin Teacher Management[cite: 1, 2]
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
    
    # Teacher Student Management[cite: 2]
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
]