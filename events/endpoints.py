from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^$', EventsAPI.as_view({
        'get': 'list',
    }), name="events_list")
]