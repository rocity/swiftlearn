from rest_framework import serializers
from .models import Event, EventComment, Feedback, Bookmark


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
                  'id',
                  'title',
                  'info',
                  'fee',
                  'start_date',
                  'start_time',
                  'end_time',
                  'educator',
                  )


class EventCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'