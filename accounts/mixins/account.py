from ..models import Account, Transaction


class AccountBalance(object):
    """ manage user's balance
    """
    def __init__(self, *args, **kwargs):
        return super(AccountBalance, self).__init__(*args, **kwargs)

    def get_running_balance(self, user, amount, trans_type):
        if trans_type == Transaction.CREDIT:
            return user.balance + amount
        return user.balance - amount

    def create_trans(self, user, amount, trans_type, desc=None):
        """ Create transaction
        """
        running_balance = self.get_running_balance(user, amount, trans_type)
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            trans_type=trans_type,
            running_balance=running_balance,
            description=desc
        )

        # update user's balance
        user.balance = running_balance
        user.save()

        return transaction