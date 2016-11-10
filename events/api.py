from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Event, EventComment, Feedback, Bookmark
from .serializers import EventSerializer, EventCommentSerializer, FeedbackSerializer, BookmarkSerializer


from braces.views import LoginRequiredMixin


class EventsAPI(LoginRequiredMixin, ViewSet):
    """ API endpoint for the list of events
    """
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

    def list(self, *args, **kwargs):
        events = Event.objects.filter(is_finished=False, educator=self.request.user)
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=204)

    def create_event(self, request, **kwargs):
        serializer = EventSerializer(data=dict(
                                     educator=self.request.user.id,
                                     title=request.data['title'],
                                     info=request.data['info'],
                                     fee=request.data['fee'],
                                     start_date=request.data['start_date'],
                                     start_time=request.data['start_time'],
                                     end_time=request.data['end_time']
            ))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get_event(self, request, **kwargs):
        event_id = kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
    
        return Response(serializer.data)

    def update_event(self, request, **kwargs):
        event = get_object_or_404(Event, pk=kwargs.get('event_id'))
        serializer = EventSerializer(event, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete_event(self, request, **kwargs):
        event = get_object_or_404(Event, pk=kwargs.get('event_id'))
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def get_comment(self, request, **kwargs):
        comment = get_object_or_404(EventComment, pk=kwargs.get('comment_id'))
        serializer = EventCommentSerializer(comment)
        return Response(serializer.data)

    def update_comment(self, request, **kwargs):
        comment = get_object_or_404(EventComment, pk=kwargs.get('comment_id'))
        serializer = EventCommentSerializer(comment, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete_comment(self, request, **kwargs):
        comment = get_object_or_404(EventComment, pk=kwargs.get('comment_id'))
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def get_reply(self, request, **kwargs):
        reply = get_object_or_404(EventComment, pk=kwargs.get('reply_id'))
        serializer = EventCommentSerializer(reply)
        return Response(serializer.data)

    def update_reply(self, request, **kwargs):
        reply = get_object_or_404(EventComment, pk=kwargs.get('reply_id'))
        serializer = EventCommentSerializer(reply, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete_reply(self, request, **kwargs):
        reply = get_object_or_404(EventComment, pk=kwargs.get('reply_id'))
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

class BookmarkAPI(LoginRequiredMixin, ViewSet):
    """ API endpoint for user bookmarks on specific events
    """
    serializer_class = BookmarkSerializer

    def create_bookmark(self, request, **kwargs):
        event_id = kwargs.get('event_id')

        try:
            # Check if bookmark already exists. if so, just change active status
            bookmark = Bookmark.objects.get(user=self.request.user.id, event_title=event_id)
            serializer = BookmarkSerializer(bookmark, data=dict(active=True), partial=True)
        except Bookmark.DoesNotExist:
            # Bookmark object is not yet created. Generate a new one
            serializer = BookmarkSerializer(data=dict(
                                            user=self.request.user.id,
                                            event_title=event_id))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def remove_bookmark(self, request, **kwargs):
        bookmark = get_object_or_404(Bookmark, pk=kwargs.get('bookmark_id'))

        serializer = BookmarkSerializer(bookmark, data=dict(active=False), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)