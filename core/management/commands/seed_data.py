from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Subject, Grade, Experiment, Achievement
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Create subjects
        subjects_data = [
            {'name': 'Kimyo', 'icon': 'flask', 'color': 'text-success', 'bg_color': 'bg-success bg-opacity-10', 
             'description': 'Kimyo fani moddalarning tarkibi, tuzilishi, xossalari va o\'zgarishlarini o\'rganadi.'},
            {'name': 'Fizika', 'icon': 'atom', 'color': 'text-primary', 'bg_color': 'bg-primary bg-opacity-10',
             'description': 'Fizika fani materiya, energiya va ularning o\'zaro ta\'sirini o\'rganadi.'},
            {'name': 'Matematika', 'icon': 'calculator', 'color': 'text-warning', 'bg_color': 'bg-warning bg-opacity-10',
             'description': 'Matematika fani son, struktura, fazo va o\'zgarishlarni o\'rganadi.'},
            {'name': 'Biologiya', 'icon': 'microscope', 'color': 'text-secondary', 'bg_color': 'bg-secondary bg-opacity-10',
             'description': 'Biologiya fani tirik organizmlar va ularning o\'zaro ta\'sirini o\'rganadi.'},
        ]
        
        subjects = []
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults={
                    'slug': slugify(subject_data['name']),
                    'icon': subject_data['icon'],
                    'color': subject_data['color'],
                    'bg_color': subject_data['bg_color'],
                    'description': subject_data['description'],
                }
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'Created subject: {subject.name}')
        
        # Create grades
        grades = []
        for grade_number in range(8, 12):
            grade, created = Grade.objects.get_or_create(
                number=grade_number,
                defaults={'description': f'{grade_number}-sinf o\'quvchilari uchun'}
            )
            grades.append(grade)
            if created:
                self.stdout.write(f'Created grade: {grade.number}-sinf')
        
        # Create experiments
        difficulties = ['easy', 'medium', 'hard']
        durations = ['30 daqiqa', '45 daqiqa', '60 daqiqa']
        
        experiment_count = 0
        for subject in subjects:
            for grade in grades:
                for i in range(1, 6):  # 5 experiments per subject per grade
                    title = f"{subject.name} tajribasi {i} ({grade.number}-sinf)"
                    slug = slugify(title)
                    
                    experiment, created = Experiment.objects.get_or_create(
                        slug=slug,
                        defaults={
                            'title': title,
                            'subject': subject,
                            'grade': grade,
                            'description': f"{grade.number}-sinf uchun {subject.name.lower()} laboratoriya tajribasi",
                            'difficulty': random.choice(difficulties),
                            'duration': random.choice(durations),
                            'instructions': f"Bu tajriba uchun kerakli ko'rsatmalar...",
                            'is_vr': False,
                        }
                    )
                    
                    if created:
                        experiment_count += 1
        
        self.stdout.write(f'Created {experiment_count} experiments')
        
        # Create achievements
        achievements_data = [
            {'name': 'Kimyo bilimdon', 'description': '5 ta kimyo tajribasini muvaffaqiyatli yakunlash', 'icon': 'award'},
            {'name': 'Fizika mutaxassisi', 'description': '10 ta fizika tajribasini muvaffaqiyatli yakunlash', 'icon': 'award'},
            {'name': 'Matematika ustasi', 'description': 'Barcha matematika tajribalarini yakunlash', 'icon': 'award'},
            {'name': 'Biologiya izlanuvchisi', 'description': 'Barcha biologiya tajribalarini yakunlash', 'icon': 'award'},
            {'name': 'Ilmiy izlanuvchi', 'description': 'Har bir fandan kamida 3 ta tajribani yakunlash', 'icon': 'award'},
        ]
        
        achievement_count = 0
        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults={
                    'description': achievement_data['description'],
                    'icon': achievement_data['icon'],
                }
            )
            
            if created:
                achievement_count += 1
        
        self.stdout.write(f'Created {achievement_count} achievements')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Created superuser: admin (password: admin)')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))