from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LearningStyleDiagnostic(models.Model):
    """Model to store user learning style diagnostic results"""
    LEARNING_STYLES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading', 'Reading/Writing'),
        ('kinesthetic', 'Kinesthetic'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_styles')
    date_taken = models.DateTimeField(default=timezone.now)
    
    # Scores for each learning style (0-100)
    visual_score = models.IntegerField(default=0)
    auditory_score = models.IntegerField(default=0)
    reading_score = models.IntegerField(default=0)
    kinesthetic_score = models.IntegerField(default=0)
    
    # Primary and secondary learning styles
    primary_style = models.CharField(max_length=20, choices=LEARNING_STYLES)
    secondary_style = models.CharField(max_length=20, choices=LEARNING_STYLES, blank=True, null=True)
    
    # AI-generated recommendations
    recommendations = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Learning Style - {self.get_primary_style_display()}"
    
    def get_highest_score(self):
        """Returns the learning style with the highest score"""
        scores = {
            'visual': self.visual_score,
            'auditory': self.auditory_score,
            'reading': self.reading_score,
            'kinesthetic': self.kinesthetic_score
        }
        return max(scores, key=scores.get)
    
    def get_style_distribution(self):
        """Returns the percentage distribution of learning styles"""
        total = self.visual_score + self.auditory_score + self.reading_score + self.kinesthetic_score
        if total == 0:
            return {
                'visual': 0,
                'auditory': 0,
                'reading': 0,
                'kinesthetic': 0
            }
        
        return {
            'visual': round((self.visual_score / total) * 100),
            'auditory': round((self.auditory_score / total) * 100),
            'reading': round((self.reading_score / total) * 100),
            'kinesthetic': round((self.kinesthetic_score / total) * 100)
        }

class DiagnosticQuestion(models.Model):
    """Model for learning style diagnostic questions"""
    LEARNING_STYLE_CATEGORIES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading', 'Reading/Writing'),
        ('kinesthetic', 'Kinesthetic'),
    ]
    
    text = models.TextField()
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLE_CATEGORIES)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.get_learning_style_display()} Question: {self.text[:50]}..."

class DiagnosticResponse(models.Model):
    """Model to store user responses to diagnostic questions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnostic_responses')
    question = models.ForeignKey(DiagnosticQuestion, on_delete=models.CASCADE, related_name='responses')
    score = models.IntegerField(help_text="Score from 1-5 (strongly disagree to strongly agree)")
    diagnostic = models.ForeignKey(LearningStyleDiagnostic, on_delete=models.CASCADE, related_name='responses')
    
    class Meta:
        unique_together = ('user', 'question', 'diagnostic')
    
    def __str__(self):
        return f"{self.user.username}'s response to {self.question}"

class LearningResource(models.Model):
    """Model for learning resources tailored to different learning styles"""
    LEARNING_STYLE_CATEGORIES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading', 'Reading/Writing'),
        ('kinesthetic', 'Kinesthetic'),
        ('all', 'All Styles'),
    ]
    
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('interactive', 'Interactive'),
        ('exercise', 'Exercise'),
        ('tool', 'Tool'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLE_CATEGORIES)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    url = models.URLField(blank=True)
    file = models.FileField(upload_to='learning_resources/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_resources')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_learning_style_display()})"

class LearningStyleQuestion(models.Model):
    """Model for learning style assessment questions"""
    text = models.TextField()
    category = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.category} - {self.text[:50]}..."

class UserLearningStyle(models.Model):
    """Model to store user's learning style preferences"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_style_preferences')
    visual_preference = models.IntegerField(default=0)
    auditory_preference = models.IntegerField(default=0)
    reading_preference = models.IntegerField(default=0)
    kinesthetic_preference = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Learning Style Preferences"

class UserDiagnosticResponse(models.Model):
    """Model to store user responses to learning style questions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='style_responses')
    question = models.ForeignKey(LearningStyleQuestion, on_delete=models.CASCADE)
    response = models.IntegerField(help_text="Response value (1-5)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
    
    def __str__(self):
        return f"{self.user.username}'s response to {self.question}"
