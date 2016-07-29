from django.core.urlresolvers import reverse
from django.db import models
from accounts.models import Account, Skill
from userlogs.mixins import RecentActivityMixin


class Event(RecentActivityMixin, models.Model):
    """ educator's session
    """
    educator = models.ForeignKey(Account)
    title = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Skill, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    fee = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "{title}".format(title=self.title)

    def get_event_url(self):
        return reverse('event', args=[self.id])

    def save(self, *args, **kwargs):
        action_type = self.ra_model.CREATED if not self.id else self.ra_model.UPDATED
        instance = super(Event, self).save(*args, **kwargs)
        # log activity
        self.log_activity(self.educator,
            self.ra_model.EVENT, action_type, obj=self)

        return instance


class Participant(RecentActivityMixin, models.Model):
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

    def save(self, *args, **kwargs):
        instance = super(Participant, self).save(*args, **kwargs)
        if not self.id:
            # log activity
            self.log_activity(self.user,
                self.ra_model.EVENT, self.ra_model.JOINED, obj=self.event)
        
        return instance