from .models import RecentActivity


class RecentActivityMixin(object):

    ra_model = RecentActivity

    def __init__(self, *args, **kwargs):
        return super(RecentActivityMixin, self).__init__(*args, **kwargs)

    def log_activity(self, user, action, action_type, obj=None):
        """ create a activity
        """
        link = obj.get_event_url() if obj else user.get_profile_url()

        return self.ra_model.objects.create(user=user,
            action=action, action_type=action_type, link=link)