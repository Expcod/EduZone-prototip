from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.utils import timezone

from .models import (
    LearningStyleDiagnostic, 
    DiagnosticQuestion, 
    DiagnosticResponse,
    LearningResource,
    LearningStyleQuestion,
    UserLearningStyle,
    UserDiagnosticResponse
)
from .forms import DiagnosticResponseForm

import json
import numpy as np
from sklearn.cluster import KMeans

def home(request):
    """Home page for the learning styles app"""
    # Get user learning style if authenticated
    user_learning_style = None
    if request.user.is_authenticated:
        user_learning_style = UserLearningStyle.objects.filter(user=request.user).first()
    
    return render(request, 'learning_styles/home.html', {
        'user_learning_style': user_learning_style
    })

@login_required
def diagnostic_test(request):
    """Diagnostic test to determine learning style"""
    # Check if user has already taken the test
    existing_style = UserLearningStyle.objects.filter(user=request.user).first()
    
    # Get all questions for the diagnostic test
    questions = LearningStyleQuestion.objects.all().order_by('?')  # Randomize question order
    
    if request.method == 'POST':
        # Process form submission
        responses = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                try:
                    response_value = int(value)
                    responses[question_id] = response_value
                except ValueError:
                    pass
        
        if len(responses) < 5:  # Require at least 5 responses
            messages.error(request, "Iltimos, kamida 5 ta savolga javob bering.")
            return render(request, 'learning_styles/diagnostic_test.html', {
                'questions': questions
            })
        
        # Calculate scores for each learning style category
        visual_score = 0
        auditory_score = 0
        kinesthetic_score = 0
        reading_writing_score = 0
        total_responses = 0
        
        # Process each response
        for question_id, response_value in responses.items():
            try:
                question = LearningStyleQuestion.objects.get(id=question_id)
                
                # Save or update user response
                UserDiagnosticResponse.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'response_value': response_value}
                )
                
                # Add to appropriate score based on question category
                if question.category == 'visual':
                    visual_score += response_value
                elif question.category == 'auditory':
                    auditory_score += response_value
                elif question.category == 'kinesthetic':
                    kinesthetic_score += response_value
                elif question.category == 'reading_writing':
                    reading_writing_score += response_value
                
                total_responses += 1
            except LearningStyleQuestion.DoesNotExist:
                continue
        
        # Normalize scores to percentages
        total_points = visual_score + auditory_score + kinesthetic_score + reading_writing_score
        if total_points > 0:
            visual_percent = int((visual_score / total_points) * 100)
            auditory_percent = int((auditory_score / total_points) * 100)
            kinesthetic_percent = int((kinesthetic_score / total_points) * 100)
            reading_writing_percent = int((reading_writing_score / total_points) * 100)
            
            # Determine primary learning style
            scores = {
                'visual': visual_percent,
                'auditory': auditory_percent,
                'kinesthetic': kinesthetic_percent,
                'reading_writing': reading_writing_percent
            }
            
            primary_style = max(scores, key=scores.get)
            
            # Check if multimodal (two or more styles with similar scores)
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            if len(sorted_scores) >= 2 and sorted_scores[0][1] - sorted_scores[1][1] < 10:
                primary_style = 'multimodal'
            
            # Save or update user learning style
            UserLearningStyle.objects.update_or_create(
                user=request.user,
                defaults={
                    'primary_style': primary_style,
                    'visual_score': visual_percent,
                    'auditory_score': auditory_percent,
                    'kinesthetic_score': kinesthetic_percent,
                    'reading_writing_score': reading_writing_percent
                }
            )
            
            messages.success(request, "Diagnostika muvaffaqiyatli yakunlandi!")
            return redirect('learning_styles:results')
        else:
            messages.error(request, "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    return render(request, 'learning_styles/diagnostic_test.html', {
        'questions': questions,
        'existing_style': existing_style
    })

@login_required
def diagnostic_results(request):
    """Show diagnostic results and recommendations"""
    user_learning_style = UserLearningStyle.objects.filter(user=request.user).first()
    
    if not user_learning_style:
        messages.warning(request, "Siz hali diagnostikadan o'tmagansiz.")
        return redirect('learning_styles:diagnostic_test')
    
    # Get recommended resources based on learning style
    recommended_resources = LearningResource.objects.filter(
        learning_style__in=[user_learning_style.primary_style, 'all']
    ).order_by('-created_at')[:5]
    
    return render(request, 'learning_styles/diagnostic_results.html', {
        'user_learning_style': user_learning_style,
        'recommended_resources': recommended_resources
    })

def analyze_diagnostic_results(diagnostic):
    """Analyze diagnostic responses and update the diagnostic record"""
    # Get all responses for this diagnostic session
    responses = DiagnosticResponse.objects.filter(diagnostic_session=diagnostic)
    
    # Initialize scores
    scores = {
        'visual': 0,
        'auditory': 0,
        'kinesthetic': 0,
        'reading_writing': 0,
    }
    
    # Calculate scores for each learning style
    for response in responses:
        category = response.question.category
        if category in scores:
            scores[category] += response.response_value * response.question.weight
    
    # Normalize scores to 0-100 scale
    max_possible = {
        'visual': DiagnosticQuestion.objects.filter(category='visual', is_active=True).aggregate(
            total=sum('weight'))['total'] * 5 or 1,
        'auditory': DiagnosticQuestion.objects.filter(category='auditory', is_active=True).aggregate(
            total=sum('weight'))['total'] * 5 or 1,
        'kinesthetic': DiagnosticQuestion.objects.filter(category='kinesthetic', is_active=True).aggregate(
            total=sum('weight'))['total'] * 5 or 1,
        'reading_writing': DiagnosticQuestion.objects.filter(category='reading_writing', is_active=True).aggregate(
            total=sum('weight'))['total'] * 5 or 1,
    }
    
    for style in scores:
        if max_possible[style] > 0:
            scores[style] = min(100, int((scores[style] / max_possible[style]) * 100))
    
    # Determine primary learning style
    primary_style = max(scores, key=scores.get)
    
    # Generate strengths and recommendations
    strengths = generate_strengths(primary_style, scores)
    recommendations = generate_recommendations(primary_style, scores)
    
    # Update diagnostic record
    diagnostic.primary_style = primary_style
    diagnostic.visual_score = scores['visual']
    diagnostic.auditory_score = scores['auditory']
    diagnostic.kinesthetic_score = scores['kinesthetic']
    diagnostic.reading_writing_score = scores['reading_writing']
    diagnostic.strengths = strengths
    diagnostic.recommendations = recommendations
    diagnostic.analysis_details = {
        'scores': scores,
        'normalized_scores': {k: v for k, v in scores.items()},
        'response_count': responses.count(),
    }
    diagnostic.save()

def generate_strengths(primary_style, scores):
    """Generate strengths based on learning style"""
    strengths = {
        'visual': [
            "Vizual ma'lumotlarni yaxshi eslab qolasiz.",
            "Diagrammalar, grafiklar va rasmlar orqali o'rganishda kuchli.",
            "Fazoviy munosabatlarni yaxshi tushunasiz.",
            "Ranglar va vizual elementlarni yaxshi eslab qolasiz.",
        ],
        'auditory': [
            "Og'zaki tushuntirishlarni yaxshi qabul qilasiz.",
            "Tinglash orqali o'rganishda kuchli.",
            "Muhokama va suhbatlar orqali bilim olishda samarali.",
            "Og'zaki ko'rsatmalarni yaxshi eslab qolasiz.",
        ],
        'kinesthetic': [
            "Amaliy tajribalar orqali o'rganishda kuchli.",
            "Harakat va jismoniy faoliyat orqali o'rganishni afzal ko'rasiz.",
            "Qo'l bilan ishlaganda yaxshi o'zlashtirasiz.",
            "Real hayotiy misollar orqali o'rganishda samarali.",
        ],
        'reading_writing': [
            "Matnlarni o'qish va yozish orqali o'rganishda kuchli.",
            "Ro'yxatlar va yozma ko'rsatmalarni yaxshi tushunasiz.",
            "O'qib chiqilgan ma'lumotlarni yaxshi eslab qolasiz.",
            "Konspekt olish va yozma mashqlar orqali samarali o'rganasiz.",
        ],
    }
    
    # Get strengths for primary style
    result = strengths.get(primary_style, [])
    
    # Add strengths from secondary styles if score is high
    secondary_styles = sorted(
        [(style, score) for style, score in scores.items() if style != primary_style],
        key=lambda x: x[1],
        reverse=True
    )
    
    if secondary_styles and secondary_styles[0][1] >= 70:
        result.append(f"Siz {get_style_name(secondary_styles[0][0])} uslubida ham kuchli.")
        result.append(strengths[secondary_styles[0][0]][0])
    
    return "\n".join(result)

def generate_recommendations(primary_style, scores):
    """Generate recommendations based on learning style"""
    recommendations = {
        'visual': [
            "Diagrammalar, grafiklar va rasmlardan foydalaning.",
            "Ranglar bilan belgilash va ajratib ko'rsatish usullarini qo'llang.",
            "Vizual xaritalar va sxemalar yarating.",
            "Video darslar va animatsiyalardan foydalaning.",
            "Konspektlaringizni vizual elementlar bilan boyiting.",
        ],
        'auditory': [
            "Audio darslar va podkastlardan foydalaning.",
            "Materialni ovoz chiqarib o'qing yoki tinglang.",
            "Guruhlarda muhokama qiling va savol-javob usulidan foydalaning.",
            "O'rganilayotgan materialni o'z so'zlaringiz bilan tushuntiring.",
            "Musiqiy fon bilan o'rganishni sinab ko'ring.",
        ],
        'kinesthetic': [
            "Amaliy mashg'ulotlar va laboratoriya ishlarida faol qatnashing.",
            "O'rganish jarayonida harakat qiling - yuring, qo'l harakatlarini qo'llang.",
            "Rolli o'yinlar va simulyatsiyalardan foydalaning.",
            "Qisqa intervallarda o'rganing va tanaffuslar qiling.",
            "Real hayotiy misollar va tajribalar orqali o'rganing.",
        ],
        'reading_writing': [
            "Konspekt oling va o'z so'zlaringiz bilan qayta yozing.",
            "Ro'yxatlar, jadvallar va matnli ma'lumotlardan foydalaning.",
            "O'qilgan materialni yozma ravishda qayta ishlang.",
            "Lug'atlar, qo'llanmalar va yozma manbalardan foydalaning.",
            "O'z bilimlaringizni yozma ravishda tekshiring.",
        ],
    }
    
    # Get recommendations for primary style
    result = recommendations.get(primary_style, [])
    
    # Add recommendations for balanced learning if scores are close
    scores_list = list(scores.values())
    if max(scores_list) - min(scores_list) < 20:
        result.append("\nSizning o'rganish uslubingiz muvozanatlashgan. Quyidagi umumiy tavsiyalar:")
        result.append("- Turli xil o'rganish usullarini birlashtiring.")
        result.append("- O'zingiz uchun eng samarali usullarni aniqlash uchun turli yondashuvlarni sinab ko'ring.")
        result.append("- Murakkab mavzularni o'rganishda bir nechta uslublardan foydalaning.")
    
    return "\n".join(result)

def get_style_name(style_code):
    """Get human-readable style name in Uzbek"""
    style_names = {
        'visual': 'vizual',
        'auditory': 'eshitish',
        'kinesthetic': 'amaliy',
        'reading_writing': 'o\'qish-yozish',
        'multimodal': 'aralash',
    }
    return style_names.get(style_code, style_code)

@login_required
def learning_resources(request):
    """Show all learning resources"""
    resources = LearningResource.objects.all().order_by('-created_at')
    
    # Get user learning style if available
    user_learning_style = UserLearningStyle.objects.filter(user=request.user).first()
    
    return render(request, 'learning_styles/resources.html', {
        'resources': resources,
        'user_learning_style': user_learning_style
    })

@login_required
def learning_resources_by_style(request, style):
    """Show learning resources filtered by learning style"""
    if style not in [choice[0] for choice in LearningResource.STYLE_CHOICES]:
        return redirect('learning_styles:resources')
    
    resources = LearningResource.objects.filter(
        learning_style__in=[style, 'all']
    ).order_by('-created_at')
    
    # Get user learning style if available
    user_learning_style = UserLearningStyle.objects.filter(user=request.user).first()
    
    return render(request, 'learning_styles/resources.html', {
        'resources': resources,
        'user_learning_style': user_learning_style,
        'current_style': style
    })

@login_required
def ai_dashboard(request):
    """AI Diagnostics Dashboard"""
    # Get user's learning style
    user_diagnostic = LearningStyleDiagnostic.objects.filter(
        user=request.user
    ).order_by('-date_taken').first()
    
    # Get overall statistics
    total_diagnostics = LearningStyleDiagnostic.objects.count()
    
    # Get distribution of primary learning styles
    learning_style_distribution = LearningStyleDiagnostic.objects.values(
        'primary_style'
    ).annotate(
        count=Count('id')
    ).order_by('primary_style')
    
    # Convert to percentages
    style_distribution = []
    for style in learning_style_distribution:
        percentage = (style['count'] / max(total_diagnostics, 1)) * 100
        style_name = dict(LearningStyleDiagnostic.LEARNING_STYLE_CHOICES).get(
            style['primary_style'], 'Unknown'
        )
        style_distribution.append({
            'style': style_name,
            'percentage': round(percentage, 1)
        })
    
    # Get recommended resources based on user's learning style
    recommended_resources = []
    if user_diagnostic:
        recommended_resources = LearningResource.objects.filter(
            learning_style=user_diagnostic.primary_style
        )[:5]
    
    context = {
        'user_diagnostic': user_diagnostic,
        'total_diagnostics': total_diagnostics,
        'style_distribution': style_distribution,
        'recommended_resources': recommended_resources,
    }
    
    return render(request, 'learning_styles/ai_dashboard.html', context)
