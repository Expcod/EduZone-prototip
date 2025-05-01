from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from core.models import Subject, Grade, Experiment
from .models import SimulationType, Simulation, UserSimulationProgress

def simulation_home(request):
    """Home page for the simulation lab"""
    simulation_types = SimulationType.objects.all()
    subjects = Subject.objects.all()
    grades = Grade.objects.all().order_by('number')
    
    # Get featured simulations
    featured_simulations = Simulation.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    # Get user progress if logged in
    user_progress = {}
    if request.user.is_authenticated:
        progress_records = UserSimulationProgress.objects.filter(
            user=request.user,
            simulation__in=featured_simulations
        )
        for record in progress_records:
            user_progress[record.simulation.id] = {
                'started': record.started,
                'completed': record.completed
            }
    
    return render(request, 'simlab/home.html', {
        'simulation_types': simulation_types,
        'subjects': subjects,
        'grades': grades,
        'featured_simulations': featured_simulations,
        'user_progress': user_progress,
    })

def simulation_types(request):
    """Page showing all simulation types"""
    simulation_types = SimulationType.objects.all()
    
    return render(request, 'simlab/types.html', {
        'simulation_types': simulation_types,
    })

def subject_simulations(request, subject_slug):
    """Page showing simulations for a specific subject"""
    subject = get_object_or_404(Subject, slug=subject_slug)
    grades = Grade.objects.all().order_by('number')
    
    # Get simulations for this subject
    simulations = Simulation.objects.filter(
        experiment__subject=subject,
        is_active=True
    ).order_by('experiment__grade__number')
    
    # Group simulations by grade
    simulations_by_grade = {}
    for grade in grades:
        simulations_by_grade[grade] = simulations.filter(experiment__grade=grade)
    
    return render(request, 'simlab/subject_simulations.html', {
        'subject': subject,
        'grades': grades,
        'simulations_by_grade': simulations_by_grade,
    })

def grade_simulations(request, grade_number):
    """Page showing simulations for a specific grade"""
    grade = get_object_or_404(Grade, number=grade_number)
    subjects = Subject.objects.all()
    
    # Get simulations for this grade
    simulations = Simulation.objects.filter(
        experiment__grade=grade,
        is_active=True
    ).order_by('experiment__subject__name')
    
    # Group simulations by subject
    simulations_by_subject = {}
    for subject in subjects:
        simulations_by_subject[subject] = simulations.filter(experiment__subject=subject)
    
    return render(request, 'simlab/grade_simulations.html', {
        'grade': grade,
        'subjects': subjects,
        'simulations_by_subject': simulations_by_subject,
    })

def run_simulation(request, sim_slug):
    """Page to run a specific simulation"""
    simulation = get_object_or_404(Simulation, slug=sim_slug, is_active=True)
    
    # Get simulation assets
    assets = simulation.assets.all()
    
    # Record that the user started this simulation
    if request.user.is_authenticated:
        progress, created = UserSimulationProgress.objects.get_or_create(
            user=request.user,
            simulation=simulation,
            defaults={'started': True}
        )
        if not progress.started:
            progress.started = True
            progress.save()
    
    # Determine which template to use based on simulation type
    template_name = f"simlab/simulations/{simulation.simulation_type.slug}.html"
    
    # For simple chemistry lab, use the simple-chemistry template
    if simulation.simulation_type.slug == 'simple-chemistry':
        template_name = "simlab/simulations/simple-chemistry.html"
    
    return render(request, template_name, {
        'simulation': simulation,
        'assets': assets,
    })

@login_required
@csrf_exempt
def save_simulation_progress(request):
    """API endpoint to save simulation progress"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        simulation_id = data.get('simulation_id')
        completed = data.get('completed', False)
        simulation_data = data.get('data', {})
        
        simulation = get_object_or_404(Simulation, id=simulation_id, is_active=True)
        
        progress, created = UserSimulationProgress.objects.get_or_create(
            user=request.user,
            simulation=simulation,
            defaults={
                'started': True,
                'completed': completed,
                'completion_date': timezone.now() if completed else None,
                'data': simulation_data
            }
        )
        
        if not created:
            progress.started = True
            progress.data = simulation_data
            
            if completed and not progress.completed:
                progress.completed = True
                progress.completion_date = timezone.now()
            
            progress.save()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def load_simulation_progress(request, simulation_id):
    """API endpoint to load simulation progress"""
    try:
        simulation = get_object_or_404(Simulation, id=simulation_id, is_active=True)
        
        try:
            progress = UserSimulationProgress.objects.get(
                user=request.user,
                simulation=simulation
            )
            
            return JsonResponse({
                'success': True,
                'started': progress.started,
                'completed': progress.completed,
                'data': progress.data
            })
        
        except UserSimulationProgress.DoesNotExist:
            return JsonResponse({
                'success': True,
                'started': False,
                'completed': False,
                'data': {}
            })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
