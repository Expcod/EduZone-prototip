from django.contrib import admin
from .models import (
    LearningStyleDiagnostic, 
    DiagnosticQuestion, 
    DiagnosticResponse,
    LearningResource,
    LearningStyleQuestion,
    UserLearningStyle,
    UserDiagnosticResponse
)

@admin.register(LearningStyleDiagnostic)
class LearningStyleDiagnosticAdmin(admin.ModelAdmin):
    list_display = ('user', 'primary_style', 'date_taken')
    list_filter = ('primary_style', 'date_taken')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('date_taken',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'primary_style', 'secondary_style', 'date_taken')
        }),
        ('Scores', {
            'fields': ('visual_score', 'auditory_score', 'reading_score', 'kinesthetic_score')
        }),
        ('Analysis', {
            'fields': ('recommendations',)
        }),
    )

@admin.register(DiagnosticQuestion)
class DiagnosticQuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'learning_style', 'order')
    list_filter = ('learning_style',)
    search_fields = ('text',)
    
    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Question'

@admin.register(DiagnosticResponse)
class DiagnosticResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_short', 'score', 'diagnostic')
    list_filter = ('score', 'question__learning_style')
    search_fields = ('user__username', 'question__text')
    
    def question_short(self, obj):
        return obj.question.text[:30] + '...' if len(obj.question.text) > 30 else obj.question.text
    question_short.short_description = 'Question'

@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'learning_style', 'resource_type', 'created_at')
    list_filter = ('learning_style', 'resource_type')
    search_fields = ('title', 'description')

@admin.register(LearningStyleQuestion)
class LearningStyleQuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('text',)
    
    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Question'

@admin.register(UserLearningStyle)
class UserLearningStyleAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_updated')
    search_fields = ('user__username',)

@admin.register(UserDiagnosticResponse)
class UserDiagnosticResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_short', 'response', 'created_at')
    list_filter = ('response',)
    search_fields = ('user__username', 'question__text')
    
    def question_short(self, obj):
        return obj.question.text[:30] + '...' if len(obj.question.text) > 30 else obj.question.text
    question_short.short_description = 'Question'
