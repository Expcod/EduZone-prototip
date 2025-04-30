from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    
    # Main URLs
    path('', views.home, name='home'),
    path('sinf/<int:grade_number>/', views.grade_dashboard, name='grade_dashboard'),
    path('<slug:subject_slug>/laboratoriya/<int:grade_number>/', views.laboratory_view, name='laboratory_view'),
    path('<slug:subject_slug>/vr-lab/', views.vr_lab_view, name='vr_lab_view'),
    path('<slug:subject_slug>/', views.subject_view, name='subject_view'),
]