from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', EventListView.as_view(), name='events'),
    url(r'^create/$', EventCreateView.as_view(), name='event_create'),
    url(r'^(?P<event_id>[0-9]+)/join/$', EventJoinView.as_view(), name='event_join'),
    url(r'^(?P<event_id>[0-9]+)/$', EventDetailView.as_view(), name='event'),
    url(r'^(?P<event_id>[0-9]+)/feedback/$', FeedbackView.as_view(), name='feedback'),
    url(r'^(?P<event_id>[0-9]+)/bookmark/$', BookmarkView.as_view(), name='bookmark'),
]