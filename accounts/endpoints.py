from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .api import *


urlpatterns = [
    url(r'^signupapi/$', SignUpAPI.as_view(), name="signupapi"),
    url(r'^login/$', LoginView.as_view(), name='api_login'),
    url(r'^logout/$', LogoutView.as_view(), name='api_logout'),
    url(r'^messages/(?P<conversation_id>[0-9]+)/$', MessageAPI.as_view({
        'get': 'list',
        'post': 'create_message',
    }), name="message_list"),
]
urlpatterns = format_suffix_patterns(urlpatterns)