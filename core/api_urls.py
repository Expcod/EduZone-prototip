from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'profiles', api_views.UserProfileViewSet, basename='profile')
router.register(r'subjects', api_views.SubjectViewSet)
router.register(r'grades', api_views.GradeViewSet)
router.register(r'experiments', api_views.ExperimentViewSet)
router.register(r'user-experiments', api_views.UserExperimentViewSet, basename='user-experiment')
router.register(r'achievements', api_views.AchievementViewSet)
router.register(r'user-achievements', api_views.UserAchievementViewSet, basename='user-achievement')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', api_views.user_dashboard, name='api_dashboard'),
]