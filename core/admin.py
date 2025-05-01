from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Subject, 
    Grade, 
    Experiment, 
    UserExperiment, 
    Achievement, 
    UserAchievement, 
    UserProfile
)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_icon', 'slug', 'display_color')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    def display_icon(self, obj):
        return format_html('<i class="bi bi-{}" style="font-size: 1.2rem;"></i> {}', obj.icon, obj.icon)
    display_icon.short_description = 'Icon'
    
    def display_color(self, obj):
        return format_html('<span style="color: {}; padding: 5px; border-radius: 3px;">{}</span>', 
                          obj.color.replace('text-', ''), obj.color)
    display_color.short_description = 'Color'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('number', 'description')
    search_fields = ('number', 'description')

class UserExperimentInline(admin.TabularInline):
    model = UserExperiment
    extra = 0
    fields = ('user', 'completed', 'completion_date')
    readonly_fields = ('user',)

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade', 'difficulty', 'duration', 'is_vr', 'created_at')
    list_filter = ('subject', 'grade', 'difficulty', 'is_vr')
    search_fields = ('title', 'description', 'instructions')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [UserExperimentInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'subject', 'grade')
        }),
        ('Details', {
            'fields': ('description', 'difficulty', 'duration', 'instructions')
        }),
        ('Options', {
            'fields': ('is_vr',)
        }),
    )

@admin.register(UserExperiment)
class UserExperimentAdmin(admin.ModelAdmin):
    list_display = ('user', 'experiment', 'completed', 'completion_date')
    list_filter = ('completed', 'completion_date', 'experiment__subject', 'experiment__grade')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'experiment__title')
    date_hierarchy = 'completion_date'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'experiment')
        }),
        ('Progress', {
            'fields': ('completed', 'completion_date', 'notes')
        }),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_icon', 'description')
    search_fields = ('name', 'description')
    
    def display_icon(self, obj):
        return format_html('<i class="bi bi-{}" style="font-size: 1.2rem;"></i> {}', obj.icon, obj.icon)
    display_icon.short_description = 'Icon'

class UserAchievementInline(admin.TabularInline):
    model = UserAchievement
    extra = 0
    fields = ('achievement', 'progress', 'completed', 'completion_date')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'progress', 'completed', 'completion_date')
    list_filter = ('completed', 'completion_date', 'achievement')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'achievement__name')
    date_hierarchy = 'completion_date'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'grade', 'class_group', 'phone')
    list_filter = ('grade', 'school')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'school', 'phone', 'address')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'avatar')
        }),
        ('School Information', {
            'fields': ('grade', 'school', 'class_group')
        }),
        ('Contact Information', {
            'fields': ('phone', 'address', 'bio')
        }),
        ('Social Media', {
            'fields': ('website', 'github', 'twitter', 'instagram'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('user',)
        return ()

# Customize admin site header and title
admin.site.site_header = 'EduZone Administration'
admin.site.site_title = 'EduZone Admin Portal'
admin.site.index_title = 'Welcome to EduZone Admin Portal'
