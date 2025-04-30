from django import template
from django.db.models import QuerySet

register = template.Library()

@register.filter
def filter_by_subject(experiments, subject):
    """Filter experiments by subject"""
    if isinstance(experiments, QuerySet):
        return experiments.filter(subject=subject)
    return [exp for exp in experiments if exp.subject == subject]

@register.filter
def completed_count(user_experiments, experiments):
    """Count completed experiments"""
    if not user_experiments:
        return 0
    
    count = 0
    for exp in experiments:
        if exp.id in user_experiments and user_experiments[exp.id]:
            count += 1
    return count

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    if not dictionary:
        return None
    return dictionary.get(key)