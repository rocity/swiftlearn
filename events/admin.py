from django.contrib import admin
from .models import Event, Participant, Feedback, EventComment, Bookmark


class EventAdmin(admin.ModelAdmin):
    model = Event
    filter_horizontal = ('tags',)


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['user','event_title','feedback','rate_star']


class EventCommentAdmin(admin.ModelAdmin):
    model = EventComment
    list_display = ['user', 'event_title', 'comment', 'comment_date']

class BookmarkAdmin(admin.ModelAdmin):
    model = Bookmark
    list_display = ['event_title', 'user', 'active']

admin.site.register(Bookmark, BookmarkAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(Participant)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(EventComment, EventCommentAdmin)
