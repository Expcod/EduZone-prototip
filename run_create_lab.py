import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduzone.settings')
django.setup()

# Import the command
from django.core.management import call_command

if __name__ == "__main__":
    # Run the command to create the simple chemistry lab
    call_command('create_simple_lab')
    print("Simple chemistry lab created successfully!")
