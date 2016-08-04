from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer

from braces.views import LoginRequiredMixin


class EventsAPI(LoginRequiredMixin, ViewSet):
    """ API endpoint for the list of events
    """
    def list(self, *args, **kwargs):
        events = Event.objects.filter(is_finished=False, educator=self.request.user)
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=204)