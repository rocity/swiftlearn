from django.db import models
from accounts.models import Account


class Event(models.Model):
    """ educator's session
    """
    educator = models.ForeignKey(Account)
    title = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)
    fee = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "{title}".format(title=self.title)


class Participant(models.Model):
    """ session participant
    """
    INVITED = 'invited'
    JOINED = 'joined'
    DECLINED = 'declined'

    PARTICIPANT_STATUS = (
        (INVITED, 'Invited'),
        (JOINED, 'Joined'),
        (DECLINED, 'Declined'),
    )

    user = models.ForeignKey(Account)
    event = models.ForeignKey(Event)
    status = models.CharField(max_length=50, choices=PARTICIPANT_STATUS, default=INVITED)

    def __str__(self):
        return "{user}: {session}".format(user=self.user, session=self.event)