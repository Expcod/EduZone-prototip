from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Subject, Grade, Experiment, UserExperiment, Achievement, UserAchievement, UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, SubjectSerializer, GradeSerializer,
    ExperimentSerializer, UserExperimentSerializer, AchievementSerializer, UserAchievementSerializer
)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Regular users can only see their own profile
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grade.objects.all().order_by('number')
    serializer_class = GradeSerializer
    permission_classes = [permissions.AllowAny]

class ExperimentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Experiment.objects.all()
        
        # Filter by subject
        subject_slug = self.request.query_params.get('subject', None)
        if subject_slug:
            queryset = queryset.filter(subject__slug=subject_slug)
        
        # Filter by grade
        grade_number = self.request.query_params.get('grade', None)
        if grade_number:
            queryset = queryset.filter(grade__number=grade_number)
        
        # Filter by VR status
        is_vr = self.request.query_params.get('is_vr', None)
        if is_vr is not None:
            is_vr_bool = is_vr.lower() == 'true'
            queryset = queryset.filter(is_vr=is_vr_bool)
        
        return queryset

class UserExperimentViewSet(viewsets.ModelViewSet):
    serializer_class = UserExperimentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Regular users can only see their own experiments
        if self.request.user.is_staff:
            return UserExperiment.objects.all()
        return UserExperiment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.AllowAny]

class UserAchievementViewSet(viewsets.ModelViewSet):
    serializer_class = UserAchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Regular users can only see their own achievements
        if self.request.user.is_staff:
            return UserAchievement.objects.all()
        return UserAchievement.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard(request):
    """API endpoint to get user dashboard data"""
    user = request.user
    
    # Get user experiments
    user_experiments = UserExperiment.objects.filter(user=user)
    completed_experiments = user_experiments.filter(completed=True).count()
    total_experiments = Experiment.objects.count()
    
    # Get user achievements
    user_achievements = UserAchievement.objects.filter(user=user)
    achievements_data = UserAchievementSerializer(user_achievements, many=True).data
    
    # Get grade-specific data if user has a grade
    grade_data = None
    if hasattr(user, 'profile') and user.profile.grade:
        grade = user.profile.grade
        grade_experiments = Experiment.objects.filter(grade=grade)
        grade_completed = UserExperiment.objects.filter(
            user=user, 
            experiment__grade=grade,
            completed=True
        ).count()
        
        grade_data = {
            'grade_number': grade.number,
            'total_experiments': grade_experiments.count(),
            'completed_experiments': grade_completed,
            'completion_percentage': int(grade_completed / max(grade_experiments.count(), 1) * 100)
        }
    
    # Get subject-specific data
    subjects_data = []
    for subject in Subject.objects.all():
        subject_experiments = Experiment.objects.filter(subject=subject)
        subject_completed = UserExperiment.objects.filter(
            user=user, 
            experiment__subject=subject,
            completed=True
        ).count()
        
        subjects_data.append({
            'id': subject.id,
            'name': subject.name,
            'slug': subject.slug,
            'icon': subject.icon,
            'color': subject.color,
            'total_experiments': subject_experiments.count(),
            'completed_experiments': subject_completed,
            'completion_percentage': int(subject_completed / max(subject_experiments.count(), 1) * 100)
        })
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'full_name': f"{user.first_name} {user.last_name}",
            'email': user.email,
        },
        'experiments': {
            'total': total_experiments,
            'completed': completed_experiments,
            'completion_percentage': int(completed_experiments / max(total_experiments, 1) * 100)
        },
        'grade': grade_data,
        'subjects': subjects_data,
        'achievements': achievements_data
    })