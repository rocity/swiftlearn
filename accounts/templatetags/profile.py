import os

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_image_url(image):
    if image:
        return os.path.join(settings.MEDIA_URL, image.url)
    return os.path.join(settings.STATIC_URL, settings.DEFAULT_PROFILE_IMAGE)

@register.filter
def get_cover_url(image):
    if image:
        return os.path.join(settings.MEDIA_URL, image.url)
    return os.path.join(settings.STATIC_URL, settings.DEFAULT_COVER_IMAGE)
