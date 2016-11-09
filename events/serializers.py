from rest_framework import serializers
from rest_framework.reverse import reverse
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
    status_link = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = '__all__'

    def get_status_link(self, obj):
        url = reverse('bookmark_list', args=[], kwargs={'event_id': obj.event_title.id})
        if obj.active:
            url = reverse('bookmark_remove', args=[], kwargs={'event_id': obj.event_title.id,
                                                              'bookmark_id': obj.id})
        return url