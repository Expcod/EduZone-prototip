from django.urls import path
from . import views

app_name = 'simlab'  # Add namespace

urlpatterns = [
    path('', views.simulation_home, name='home'),
    path('types/', views.simulation_types, name='types'),
    path('subject/<slug:subject_slug>/', views.subject_simulations, name='subject_simulations'),
    path('grade/<int:grade_number>/', views.grade_simulations, name='grade_simulations'),
    path('run/<slug:sim_slug>/', views.run_simulation, name='run_simulation'),
    path('api/save-progress/', views.save_simulation_progress, name='save_progress'),
    path('api/load-progress/<int:simulation_id>/', views.load_simulation_progress, name='load_progress'),
]
