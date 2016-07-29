from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    model = Event
    filter_horizontal = ('tags',)

admin.site.register(Event, EventAdmin)