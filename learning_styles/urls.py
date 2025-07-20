from django.urls import path
from . import views

app_name = 'learning_styles'

urlpatterns = [
    path('', views.home, name='home'),
    path('diagnostic/', views.diagnostic_test, name='diagnostic'),
    path('results/', views.diagnostic_results, name='results'),
    path('resources/', views.learning_resources, name='resources'),
    # Add new AI dashboard page
    path('dashboard/', views.ai_dashboard, name='dashboard'),
]
