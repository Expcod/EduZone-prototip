from django.db import models
from django.contrib.auth.models import User
from core.models import Subject, Grade, Experiment

class SimulationType(models.Model):
    """Model for simulation types (2D Canvas, WebGL, Three.js, VPython)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="code")
    
    def __str__(self):
        return self.name

class Simulation(models.Model):
    """Model for laboratory simulations"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='simulations')
    simulation_type = models.ForeignKey(SimulationType, on_delete=models.CASCADE, related_name='simulations')
    description = models.TextField()
    instructions = models.TextField()
    code_js = models.TextField(blank=True, help_text="JavaScript code for the simulation")
    code_python = models.TextField(blank=True, help_text="Python code for the simulation")
    config = models.JSONField(default=dict, blank=True, help_text="Configuration parameters for the simulation")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def subject(self):
        return self.experiment.subject
    
    @property
    def grade(self):
        return self.experiment.grade

class SimulationAsset(models.Model):
    """Model for simulation assets (textures, 3D models, sounds, etc.)"""
    ASSET_TYPES = [
        ('texture', 'Texture'),
        ('model', '3D Model'),
        ('sound', 'Sound'),
        ('data', 'Data File'),
    ]
    
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    file = models.FileField(upload_to='simulation_assets/')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"

class UserSimulationProgress(models.Model):
    """Model to track user progress on simulations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulation_progress')
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='user_progress')
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    last_interaction = models.DateTimeField(auto_now=True)
    data = models.JSONField(default=dict, blank=True, help_text="User's saved simulation data")
    
    class Meta:
        unique_together = ('user', 'simulation')
    
    def __str__(self):
        return f"{self.user.username} - {self.simulation.title}"
