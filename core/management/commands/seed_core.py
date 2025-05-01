from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Subject, Grade, Experiment

class Command(BaseCommand):
    help = 'Seeds the database with initial core data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding core data...')
        
        # Create subjects
        subjects_data = [
            {
                'name': 'Kimyo',
                'slug': 'kimyo',
                'icon': 'beaker',
                'color': 'text-green-500',
                'bg_color': 'bg-green-100',
                'description': 'Kimyo fanidan virtual tajribalar'
            },
            {
                'name': 'Fizika',
                'slug': 'fizika',
                'icon': 'atom',
                'color': 'text-blue-500',
                'bg_color': 'bg-blue-100',
                'description': 'Fizika fanidan virtual tajribalar'
            },
            {
                'name': 'Matematika',
                'slug': 'matematika',
                'icon': 'calculator',
                'color': 'text-purple-500',
                'bg_color': 'bg-purple-100',
                'description': 'Matematika fanidan virtual tajribalar'
            },
            {
                'name': 'Biologiya',
                'slug': 'biologiya',
                'icon': 'dna',
                'color': 'text-red-500',
                'bg_color': 'bg-red-100',
                'description': 'Biologiya fanidan virtual tajribalar'
            }
        ]
        
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                slug=subject_data['slug'],
                defaults=subject_data
            )
            if created:
                self.stdout.write(f"Created subject: {subject.name}")
        
        # Create grades
        for grade_number in range(8, 12):
            grade, created = Grade.objects.get_or_create(
                number=grade_number,
                defaults={
                    'description': f'{grade_number}-sinf uchun virtual tajribalar'
                }
            )
            if created:
                self.stdout.write(f"Created grade: {grade_number}")
        
        self.stdout.write('Successfully seeded core data') 