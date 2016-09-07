from accounts.mixins.account import AccountBalance
from accounts.models import Transaction


class JoinEvent(AccountBalance):
    """ handles of joining to an event
    """
    def __init__(self, *args, **kwargs):
        return super(JoinEvent, self).__init__(*args, **kwargs)

    def _has_enough_credit(self, event, user):
        return True if user.credits >= event.fee else False

    def _has_joined(self, event, user):
        from events.models import Participant
        return Participant.objects.filter(event=event, user=user).exists()

    def join_event(self, event, user):
        from events.models import Participant
        # check if user's balance is enough to join
        if self._has_enough_credit(event, user) and not self._has_joined(event, user):
            # add participant
            Participant.objects.create(
                user=user, event=event, status=Participant.JOINED)
            # log user's transaction
            # user will be billed by the fee of the event
            self.create_trans(
                user=user,
                amount=event.fee,
                trans_type=Transaction.DEBIT,
                desc="Joined the {event_id} event".format(event_id=event.id),
            )
            return {}, True

        return {"error": "Not enough credit."}, False
