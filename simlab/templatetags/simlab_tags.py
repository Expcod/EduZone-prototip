from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    return dictionary.get(key)

@register.filter
def to_json(value):
    """Convert a value to JSON string"""
    return mark_safe(json.dumps(value))

@register.filter
def get_subject_color(subject_name):
    """Get color class based on subject name"""
    colors = {
        'Kimyo': 'success',
        'Fizika': 'primary',
        'Matematika': 'warning',
        'Biologiya': 'info'
    }
    return colors.get(subject_name, 'secondary')
