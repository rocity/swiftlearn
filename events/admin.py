from django.contrib import admin
from .models import Event, Participant, Feedback, EventMessage


class EventAdmin(admin.ModelAdmin):
    model = Event
    filter_horizontal = ('tags',)


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['user','event_title','feedback','rate_star']


class EventMessageAdmin(admin.ModelAdmin):
    model = EventMessage
    list_display = ['user', 'event_title', 'message', 'message_date']


admin.site.register(Event, EventAdmin)
admin.site.register(Participant)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(EventMessage, EventMessageAdmin)
