from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^events/', include('events.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^api/events/', include('events.endpoints')),
    url(r'^api/accounts/', include('accounts.endpoints')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)