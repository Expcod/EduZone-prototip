from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    """Model for academic subjects like Physics, Chemistry, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Icon name (e.g., 'beaker', 'atom')")
    color = models.CharField(max_length=50, default="text-blue-500")
    bg_color = models.CharField(max_length=50, default="bg-blue-100")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Grade(models.Model):
    """Model for grade levels (8, 9, 10, 11)"""
    number = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.number}-sinf"

class Experiment(models.Model):
    """Model for laboratory experiments"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Oson'),
        ('medium', 'O\'rta'),
        ('hard', 'Qiyin'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='experiments')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='experiments')
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    duration = models.CharField(max_length=50, help_text="e.g., '30 daqiqa'")
    instructions = models.TextField(blank=True)
    is_vr = models.BooleanField(default=False, help_text="Is this a VR experiment?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class UserExperiment(models.Model):
    """Model to track user progress on experiments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiments')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='user_experiments')
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'experiment')
    
    def __str__(self):
        return f"{self.user.username} - {self.experiment.title}"

class Achievement(models.Model):
    """Model for user achievements"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="award")
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    """Model to track user achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    progress = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.CharField(max_length=100, blank=True)
    class_group = models.CharField(max_length=10, blank=True, help_text="e.g., 'A', 'B', etc.")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Social media links
    website = models.URLField(blank=True)
    github = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username