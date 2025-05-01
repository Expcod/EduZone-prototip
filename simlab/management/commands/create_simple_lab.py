from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone

from core.models import Subject, Grade, Experiment
from simlab.models import SimulationType, Simulation

class Command(BaseCommand):
    help = 'Creates a simple chemistry lab for 8th grade'

    def handle(self, *args, **options):
        # Get or create simulation type
        sim_type, created = SimulationType.objects.get_or_create(
            name="Oddiy laboratoriya",
            slug="simple-chemistry",
            defaults={
                "description": "Oddiy kimyoviy tajribalar uchun laboratoriya",
                "icon": "flask"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created simulation type: {sim_type.name}'))
        
        # Get chemistry subject
        try:
            chemistry = Subject.objects.get(name="Kimyo")
        except Subject.DoesNotExist:
            chemistry = Subject.objects.create(
                name="Kimyo",
                slug="kimyo",
                description="Kimyo fani",
                icon="flask"
            )
            self.stdout.write(self.style.SUCCESS(f'Created subject: {chemistry.name}'))
        
        # Get 8th grade
        try:
            grade_8 = Grade.objects.get(number=8)
        except Grade.DoesNotExist:
            grade_8 = Grade.objects.create(
                number=8,
                name="8-sinf"
            )
            self.stdout.write(self.style.SUCCESS(f'Created grade: {grade_8.name}'))
        
        # Create experiment if it doesn't exist
        experiment_title = "Kislota-ishqor reaksiyasi"
        experiment, exp_created = Experiment.objects.get_or_create(
            title=experiment_title,
            subject=chemistry,
            grade=grade_8,
            defaults={
                "description": "Kislota va ishqor o'rtasidagi reaksiyani o'rganish",
                "duration_minutes": 30
            }
        )
        if exp_created:
            self.stdout.write(self.style.SUCCESS(f'Created experiment: {experiment.title}'))
        
        # Create simulations
        for i in range(1, 6):
            title = f"Kimyo tajribasi {i} (8-sinf)"
            slug = slugify(title)
            
            # Check if simulation already exists
            if Simulation.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.WARNING(f'Simulation already exists: {title}'))
                continue
            
            # Create simulation
            simulation = Simulation.objects.create(
                title=title,
                slug=slug,
                description=f"8-sinf uchun kimyo laboratoriya tajribasi {i}",
                experiment=experiment,
                simulation_type=sim_type,
                is_active=True,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                instructions="1. Boshlash tugmasini bosing\n2. Kislota va ishqor konsentratsiyalarini o'zgartiring\n3. Reaksiyani kuzating",
                code_js="// This is a placeholder for simulation code"
            )
            self.stdout.write(self.style.SUCCESS(f'Created simulation: {simulation.title}'))
        
        self.stdout.write(self.style.SUCCESS('Simple chemistry lab created successfully!'))
