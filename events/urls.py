from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', EventListView.as_view(), name='events'),
    url(r'^create/$', EventCreateView.as_view(), name='event_create'),
    url(r'^join/(?P<event_id>[0-9]+)/$', EventJoinView.as_view(), name='event_join'),
    url(r'^(?P<event_id>[0-9]+)/$', EventDetailView.as_view(), name='event'),
]