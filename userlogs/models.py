from django.db import models
from accounts.models import Account


class RecentActivity(models.Model):
    """ user activities
    """
    CREATED = 'created'
    UPDATED = 'updated'
    JOINED = 'joined'
    ACTION_TYPES = (
        (CREATED, 'Created'),
        (UPDATED, 'Updated'),
        (JOINED, 'Joined'),
    )

    PROFILE = 'profile'
    EVENT = 'event'
    ACTIONS = (
        (PROFILE, 'Profile'),
        (EVENT, 'Event'),
    )

    user = models.ForeignKey(Account)

    action = models.CharField(max_length=50, choices=ACTIONS, default=PROFILE)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES, default=CREATED)
    date_created = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{user}: {action}".format(
            user=self.user, action=self.action)