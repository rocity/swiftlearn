from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^$', EventsAPI.as_view({
        'get': 'list',
    }), name="events_list"),
    url(r'^(?P<event_id>[0-9]+)/comments/$', EventCommentsAPI.as_view({
        'get': 'list',
        'post': 'create_comment',
    }), name="comments_list"),
    url(r'^(?P<event_id>[0-9]+)/comment/(?P<comment_id>[0-9]+)/reply/$', EventCommentReplyAPI.as_view({
        'get': 'list',
        'post': 'create_reply',
    }), name="reply_list")
]