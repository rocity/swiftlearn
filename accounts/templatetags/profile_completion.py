from django import template
from accounts.models import AccountCompletionTask

register = template.Library()


@register.filter
def get_profile_tasks(value):
    return AccountCompletionTask.objects.all()