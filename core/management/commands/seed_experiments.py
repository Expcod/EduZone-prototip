from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Subject, Grade, Experiment

class Command(BaseCommand):
    help = 'Seeds the database with initial experiments'

    def handle(self, *args, **options):
        self.stdout.write('Seeding experiments...')
        
        # Get subjects and grades
        kimyo = Subject.objects.get(slug='kimyo')
        fizika = Subject.objects.get(slug='fizika')
        grade_8 = Grade.objects.get(number=8)
        
        # Create experiments
        experiments_data = [
            {
                'title': 'Kimyo tajribasi 1',
                'slug': 'kimyo-tajribasi-1',
                'subject': kimyo,
                'grade': grade_8,
                'description': 'Kimyo fanidan birinchi tajriba',
                'difficulty': 'easy',
                'duration': '30 daqiqa',
                'instructions': 'Tajriba uchun kerakli materiallar...',
                'is_vr': False
            },
            {
                'title': 'Kimyo tajribasi 2',
                'slug': 'kimyo-tajribasi-2',
                'subject': kimyo,
                'grade': grade_8,
                'description': 'Kimyo fanidan ikkinchi tajriba',
                'difficulty': 'medium',
                'duration': '45 daqiqa',
                'instructions': 'Tajriba uchun kerakli materiallar...',
                'is_vr': False
            },
            {
                'title': 'Fizika tajribasi 1',
                'slug': 'fizika-tajribasi-1',
                'subject': fizika,
                'grade': grade_8,
                'description': 'Fizika fanidan birinchi tajriba',
                'difficulty': 'easy',
                'duration': '30 daqiqa',
                'instructions': 'Tajriba uchun kerakli materiallar...',
                'is_vr': False
            },
            {
                'title': 'Fizika tajribasi 2',
                'slug': 'fizika-tajribasi-2',
                'subject': fizika,
                'grade': grade_8,
                'description': 'Fizika fanidan ikkinchi tajriba',
                'difficulty': 'medium',
                'duration': '45 daqiqa',
                'instructions': 'Tajriba uchun kerakli materiallar...',
                'is_vr': False
            }
        ]
        
        for exp_data in experiments_data:
            experiment, created = Experiment.objects.get_or_create(
                slug=exp_data['slug'],
                defaults=exp_data
            )
            if created:
                self.stdout.write(f"Created experiment: {experiment.title}")
        
        self.stdout.write('Successfully seeded experiments') 