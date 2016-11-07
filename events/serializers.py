from rest_framework import serializers
from .models import Event, EventComment, Feedback


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
    full_name = serializers.CharField(source='get_user_full_name', read_only=True)
    avatar = serializers.CharField(source='get_user_avatar', read_only=True)
    class Meta:
        model = EventComment
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'