from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^$', EventsAPI.as_view({
        'get': 'list',
        'post': 'create_event',
    }), name="events_list"),
    url(r'^(?P<event_id>[0-9]+)/$', EventsAPI.as_view({
        'get': 'get_event',
        'put': 'update_event',
        'delete': 'delete_event',
    }), name="events_update"),
    url(r'^(?P<event_id>[0-9]+)/feedbacks/$', FeedbackAPI.as_view({
        'get': 'list',
        'post': 'create_feedback',
    }), name="feedback_list"),
    url(r'^(?P<event_id>[0-9]+)/comments/$', EventCommentsAPI.as_view({
        'get': 'list',
        'post': 'create_comment',
    }), name="comments_list"),
    url(r'^(?P<event_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$', EventCommentsAPI.as_view({
        'get': 'get_comment',
        'put': 'update_comment',
        'delete': 'delete_comment',
    }), name="comments_update"),
    url(r'^(?P<event_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/reply/$', EventCommentReplyAPI.as_view({
        'get': 'list',
        'post': 'create_reply',
    }), name="reply_list"),
    url(r'^(?P<event_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/reply/(?P<reply_id>[0-9]+)/$', EventCommentReplyAPI.as_view({
        'get': 'get_reply',
        'update': 'update_reply',
        'delete': 'delete_reply',
    }), name="reply_update"),
    url(r'^(?P<event_id>[0-9]+)/bookmarks/$', BookmarkAPI.as_view({
        'get': 'create_bookmark',
    }), name="bookmark_list"),
    url(r'^(?P<event_id>[0-9]+)/bookmarks/(?P<bookmark_id>[0-9]+)/$', BookmarkAPI.as_view({
        'get': 'remove_bookmark',
    }), name="bookmark_remove"),
]