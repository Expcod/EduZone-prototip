from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Subject, Grade, Experiment, UserExperiment, Achievement, UserAchievement
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm

def home(request):
    subjects = Subject.objects.all()
    grades = Grade.objects.all().order_by('number')
    
    # Get statistics for dashboard
    stats = {
        'total_experiments': Experiment.objects.count(),
        'subjects_count': subjects.count(),
        'subjects': []
    }
    
    for subject in subjects:
        subject_stats = {
            'name': subject.name,
            'icon': subject.icon,
            'color': subject.color,
            'bg_color': subject.bg_color,
            'experiments_count': subject.experiments.count(),
        }
        stats['subjects'].append(subject_stats)
    
    return render(request, 'dashboard.html', {
        'subjects': subjects,
        'grades': grades,
        'stats': stats,
    })

def grade_dashboard(request, grade_number):
    grade = get_object_or_404(Grade, number=grade_number)
    subjects = Subject.objects.all()
    
    # Get experiments for this grade
    experiments = Experiment.objects.filter(grade=grade)
    
    # Get user progress if logged in
    user_progress = None
    achievements = []
    
    if request.user.is_authenticated:
        completed_experiments = UserExperiment.objects.filter(
            user=request.user, 
            experiment__grade=grade,
            completed=True
        ).count()
        
        user_progress = {
            'total_experiments': experiments.count(),
            'completed_experiments': completed_experiments,
            'completion_percentage': int(completed_experiments / max(experiments.count(), 1) * 100)
        }
        
        # Get achievements
        user_achievements = UserAchievement.objects.filter(user=request.user)
        for ua in user_achievements:
            achievements.append({
                'name': ua.achievement.name,
                'description': ua.achievement.description,
                'icon': ua.achievement.icon,
                'progress': ua.progress,
                'completed': ua.completed
            })
    
    # Get recent and upcoming experiments
    recent_experiments = experiments.order_by('-created_at')[:3]
    
    return render(request, 'grade_dashboard.html', {
        'grade': grade,
        'subjects': subjects,
        'experiments': experiments,
        'user_progress': user_progress,
        'recent_experiments': recent_experiments,
        'achievements': achievements,
    })

def subject_view(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)
    grades = Grade.objects.all().order_by('number')
    
    return render(request, 'subject.html', {
        'subject': subject,
        'grades': grades,
    })

def laboratory_view(request, subject_slug, grade_number):
    subject = get_object_or_404(Subject, slug=subject_slug)
    grade = get_object_or_404(Grade, number=grade_number)
    
    # Get experiments for this subject and grade
    experiments = Experiment.objects.filter(subject=subject, grade=grade, is_vr=False)
    
    # Get user progress if logged in
    user_experiments = {}
    if request.user.is_authenticated:
        user_exps = UserExperiment.objects.filter(
            user=request.user,
            experiment__in=experiments
        )
        for ue in user_exps:
            user_experiments[ue.experiment.id] = ue.completed
    
    return render(request, 'laboratory.html', {
        'subject': subject,
        'grade': grade,
        'experiments': experiments,
        'user_experiments': user_experiments,
    })

def vr_lab_view(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)
    
    return render(request, 'vr_lab.html', {
        'subject': subject,
    })

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Ro'yxatdan o'tishda xatolik yuz berdi: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    
    # Get user experiments
    user_experiments = UserExperiment.objects.filter(user=user)
    completed_experiments = user_experiments.filter(completed=True).count()
    total_experiments = Experiment.objects.count()
    
    # Get user achievements
    user_achievements = UserAchievement.objects.filter(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user.profile)
    
    return render(request, 'profile.html', {
        'user': user,
        'form': form,
        'completed_experiments': completed_experiments,
        'total_experiments': total_experiments,
        'completion_percentage': int(completed_experiments / max(total_experiments, 1) * 100),
        'user_achievements': user_achievements,
    })
