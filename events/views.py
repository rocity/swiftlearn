from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404

from braces.views import LoginRequiredMixin
from .forms import EventForm, FeedbackForm, EventCommentForm
from .models import Event, EventComment
from accounts.models import Account


class EventListView(LoginRequiredMixin, TemplateView):
    """ Events list view
    """
    template_name = 'events/list.html'

    def get(self, *args, **kwargs):
        # created upcoming events
        upcoming_events = Event.objects.filter(
            educator=self.request.user, is_finished=False)

        return render(self.request, self.template_name, {
            'upcoming_events': upcoming_events})


class EventDetailView(LoginRequiredMixin, TemplateView):
    """ Event detail view
    """
    template_name = 'events/detail.html'

    def get(self, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        comments = event.eventcomment_set.filter(parent=None).order_by('-comment_date')
        form = EventCommentForm()
        return render(self.request, self.template_name, {
            'event': event,
            'form': form,
            'comments': comments
            })


class EventCreateView(LoginRequiredMixin, TemplateView):
    """ Create a new event view
    """
    template_name = 'events/create.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'form': EventForm()})

    def post(self, *args, **kwargs):
        form = EventForm(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.educator = self.request.user
            instance.save()

            return HttpResponseRedirect(reverse('events'))
        return render(self.request, self.template_name, {'form': form})


class EventJoinView(LoginRequiredMixin, View):
    """ Join an upcoming event
    """
    def get(self, *args, **kwargs):
        # join an event
        # TODO: add a billing
        event_id = kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        resp, joined = event.join(user=self.request.user)
        print(resp)
        print(joined)

        return HttpResponseRedirect(reverse('event', args=[event.id]))


class FeedbackView(LoginRequiredMixin, TemplateView):
    """ Create new feedback for Event 
    """
    template_name = "events/feedback.html"

    def get(self, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        form = FeedbackForm()
        return render(self.request, self.template_name,{'form':form, 'event':event})

class BookmarkView(LoginRequiredMixin, View):
    """ Bookmark an event
    """
    pass