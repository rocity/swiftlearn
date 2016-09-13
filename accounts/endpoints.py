from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .api import *


urlpatterns = [
    url(r'^signupapi/$', SignUpAPI.as_view(), name="signupapi"),
    url(r'^login/$', LoginView.as_view(), name='api_login'),
    url(r'^logout/$', LogoutView.as_view(), name='api_logout'),

]
urlpatterns = format_suffix_patterns(urlpatterns)