from datetime import date, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from events.models import Event, Participant


class Command(BaseCommand):
    """send email notification to users who joined the specific event
    """
    def send_notification(self):
        events = Event.objects.all()
        for event in events:
            three_days = date.today() + timedelta(days=3)
            tomorrow = date.today() + timedelta(days=1)

            #send email notification 3 days before the event
            if three_days == event.start_date:
                participants = Participant.objects.filter(event=event)
                for participant in participants:
                    subject =   "Swiftlearn event reminder"
                    message =   "The event (" + str(event) + ") that you joined will be 3 days from now."
                    msg = EmailMessage(subject, message, to=[participant.user.email])
                    msg.send(fail_silently=False)

            #send email notification 1 day before the event
            elif tomorrow == event.start_date:
                participants = Participant.objects.filter(event=event)
                for participant in participants:
                    subject =   "Swiftlearn event reminder"
                    message =   "The event (" + str(event) + ") that you joined will be tomorrow."
                    msg = EmailMessage(subject, message, to=[participant.user.email])
                    msg.send(fail_silently=False)

    def handle(self, *args, **options):
        return self.send_notification()
