from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^activate/(?P<key>.+)/$', ActivationView.as_view(), name="activate"),
]