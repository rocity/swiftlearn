from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.management import call_command
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class AccountManager(BaseUserManager):
    """ Manager class which contains methods
        used by the account model.
    """
    def create_user(self, email, password=None, **kwargs):
        """ Create user object based on the inputted
            data.
        """
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not kwargs.get('username'):
            raise ValueError('Users mus have a valid username.')

        account = self.model(email=self.normalize_email(email), username=kwargs.get('username'))
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        """ Create superuser account.
            (can access admin panel)
        """
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True

        account.save()

        return account


class Account(AbstractBaseUser, PermissionsMixin):
    """ Model class which contains the user's
        account information
    """
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)

    # more info
    position = models.CharField(max_length=255, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activated = models.BooleanField(default=False)

    objects = AccountManager()

    is_admin   = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{email}".format(email=self.email)

    def get_full_name(self):
        """ Returns the first_name pluse the last_name, with a space
            in between.
        """
        full_name = "{first_name} {last_name}".format(
            first_name=self.first_name, last_name=self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def _extract_username(self):
        """ extract username from email
        """
        return "{username}".format(username=self.email.split('@')[0])

    def generate_confirm_key(self):
        """ Generate a new confirm key for this
            user.
        """
        from accounts.models import ConfirmationKey
        return ConfirmationKey.objects.create(user=self)


class ConfirmationKey(models.Model):
    """ learner's email confirmation key
    """
    user = models.ForeignKey(Account)
    key = models.CharField(max_length=32, null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return "{user}:{key}".format(user=self.user, key=self.key)

    def save(self, *args, **kwargs):
        if not self.id:
            self.key = self._generate_key()
        return super(ConfirmationKey, self).save(*args, **kwargs)

    def _generate_key(self):
        return uuid4().hex


# class Educator(models.Model):
#     """ educators model
#     """
#     user = models.OneToOneField(Account)


# class Session(models.Model):
#     """ educator's session
#     """
#     title = models.CharField(max_length=255)
#     info = models.TextField(null=True, blank=True)

#     start_date = models.DateTimeField(null=True, blank=True)
#     fee = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
#     is_finished = models.BooleanField(default=False)

#     def __str__(self):
#         return "{title}".format(title=self.title)