from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Event, EventComment, Feedback
from .serializers import EventSerializer, EventCommentSerializer, FeedbackSerializer

from braces.views import LoginRequiredMixin


class EventsAPI(LoginRequiredMixin, ViewSet):
    """ API endpoint for the list of events
    """
    def list(self, *args, **kwargs):
        events = Event.objects.filter(is_finished=False, educator=self.request.user)
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=204)


class EventCommentsAPI(LoginRequiredMixin, ViewSet):
    """API endpoint for the list of comments for specific event
    """
    serializer_class = EventCommentSerializer

    def list(self, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        comments = event.eventcomment_set.filter(parent=None).order_by('-comment_date')
        serializer = EventCommentSerializer(comments, many=True)

        return Response(serializer.data, status=204)

    #create comment for the event
    def create_comment(self, request, **kwargs):
        event_id = kwargs.get('event_id')
        serializer = EventCommentSerializer(data=dict(
                                            comment=request.data['comment'], 
                                            event_title=event_id,
                                            user=self.request.user.id))
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EventCommentReplyAPI(LoginRequiredMixin, ViewSet):
    """API endpoint for the list of replies for a specific comment
    """
    serializer_class = EventCommentSerializer
    
    def list(self, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        comment_id = kwargs.get('comment_id')
        comment = get_object_or_404(EventComment, id=comment_id)
        comments = event.eventcomment_set.filter(parent=comment).order_by('-comment_date')
        serializer = EventCommentSerializer(comments, many=True)
        return Response(serializer.data, status=204)

    #create reply for the comment
    def create_reply(self, request, **kwargs):
        event_id = kwargs.get('event_id')
        comment_id = kwargs.get('comment_id')
        serializer = EventCommentSerializer(data=dict(
                                            comment=request.data['comment'], 
                                            event_title=event_id,
                                            user=self.request.user.id,
                                            parent=comment_id))
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class FeedbackAPI(LoginRequiredMixin, ViewSet):
    """API endpoint for the list of feedbacks for a specific event
    """
    serializer_class = FeedbackSerializer

    def list(self, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        feedbacks = Feedback.objects.filter(event_title=event)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=204)

    #create feedback for the event
    def create_feedback(self, request, **kwargs):
        event_id = kwargs.get('event_id')
        serializer = FeedbackSerializer(data=dict(
                                        user=self.request.user.id,
                                        event_title=event_id,
                                        feedback=request.data['feedback'],
                                        rate_star=request.data['rate_star']))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)