from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Subject, Grade, Experiment, UserExperiment, Achievement, UserAchievement, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class ExperimentSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    grade_number = serializers.ReadOnlyField(source='grade.number')
    
    class Meta:
        model = Experiment
        fields = '__all__'

class UserExperimentSerializer(serializers.ModelSerializer):
    experiment_title = serializers.ReadOnlyField(source='experiment.title')
    
    class Meta:
        model = UserExperiment
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.ReadOnlyField(source='achievement.name')
    
    class Meta:
        model = UserAchievement
        fields = '__all__'