from django.contrib import admin
from django.utils.html import format_html
from .models import SimulationType, Simulation, SimulationAsset, UserSimulationProgress

@admin.register(SimulationType)
class SimulationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_icon', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def display_icon(self, obj):
        return format_html('<i class="bi bi-{}" style="font-size: 1.2rem;"></i> {}', obj.icon, obj.icon)
    display_icon.short_description = 'Icon'

class SimulationAssetInline(admin.TabularInline):
    model = SimulationAsset
    extra = 1

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'experiment', 'simulation_type', 'is_active', 'created_at')
    list_filter = ('simulation_type', 'is_active', 'experiment__subject', 'experiment__grade')
    search_fields = ('title', 'description', 'instructions')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SimulationAssetInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'experiment', 'simulation_type', 'is_active')
        }),
        ('Content', {
            'fields': ('description', 'instructions')
        }),
        ('Code', {
            'fields': ('code_js', 'code_python'),
            'classes': ('collapse',)
        }),
        ('Configuration', {
            'fields': ('config',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SimulationAsset)
class SimulationAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'simulation', 'asset_type', 'description')
    list_filter = ('asset_type', 'simulation__simulation_type')
    search_fields = ('name', 'description', 'simulation__title')

@admin.register(UserSimulationProgress)
class UserSimulationProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'simulation', 'started', 'completed', 'completion_date', 'last_interaction')
    list_filter = ('started', 'completed', 'simulation__simulation_type')
    search_fields = ('user__username', 'simulation__title')
    readonly_fields = ('last_interaction',)
