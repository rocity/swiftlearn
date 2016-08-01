from django import template
from userlogs.models import RecentActivity
from userlogs.context import RECENT_ACTIVITY_MESSAGES

register = template.Library()


@register.filter
def load_notifications(user):
    return RecentActivity.objects.filter(user=user).order_by('-date_created')[:5]

@register.filter
def shorten_timetag(strtime):
    strtime = strtime.split(",")[0]
    return strtime.replace("minutes ", "mins ").replace("minute ", "min ")

@register.filter
def single_timetag(strtime):
    return strtime.split(",")[0]

@register.filter
def notification_text(activity):
    return RECENT_ACTIVITY_MESSAGES[activity.action][activity.action_type]
