from django.core.urlresolvers import reverse
from django.db import models
from accounts.models import Account, Skill
from userlogs.mixins import RecentActivityMixin
from .mixins.join import JoinEvent


class Event(RecentActivityMixin, JoinEvent, models.Model):
    """ educator's session
    """
    educator = models.ForeignKey(Account)
    title = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Skill, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
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

    def join(self, user):
        return self.join_event(self, user)

    def get_participants(self):
        from events.models import Participant
        return Participant.objects.filter(event=self.id)


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


class Feedback(models.Model):
    """ Create new Feedback on Tutorials
    """
    user = models.ForeignKey(Account)
    event_title = models.ForeignKey(Event)
    feedback = models.TextField()
    rate_star =  models.IntegerField(default=1)
    feed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{user}{title}".format(user=self.user, title=self.event_title)


class EventComment(models.Model):
    """ Post comment at event
    """
    user = models.ForeignKey(Account)
    event_title = models.ForeignKey(Event)
    comment = models.TextField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="replies")
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{user} {comment}".format(user=self.user, comment=self.comment)

class Bookmark(models.Model):
    """ User's saved bookmarks
    """
    user = models.ForeignKey(Account)
    event_title = models.ForeignKey(Event)
    bookmark_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{user} {event_title}".format(user=self.user, event_title=self.event_title)
