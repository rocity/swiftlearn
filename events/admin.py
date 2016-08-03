from django.contrib import admin
from .models import Event, Participant, Feedback


class EventAdmin(admin.ModelAdmin):
    model = Event
    filter_horizontal = ('tags',)


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['user','event_title','feedback','rate_star']


admin.site.register(Event, EventAdmin)
admin.site.register(Participant)
admin.site.register(Feedback, FeedbackAdmin)
