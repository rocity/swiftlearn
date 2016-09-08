from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import EmailMessage
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from .mixins.timezone import TimezoneMixin

import os
from django.conf import settings

from .utils import get_directory, get_directory_cover_photo
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.conf import settings

class AccountCompletionTask(models.Model):
    """ learner's account completion
    """
    desc = models.CharField(max_length=255)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "{desc}".format(desc=self.desc)


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


class Account(TimezoneMixin, AbstractBaseUser, PermissionsMixin):
    """ Model class which contains the user's
        account information
    """

    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    middle_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    timezone = models.CharField(max_length=50, null=True, blank=True)

    cover_photo = models.ImageField(upload_to=get_directory_cover_photo, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=get_directory, null=True, blank=True)
    quote = models.TextField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    badges = models.ManyToManyField('Badge', blank=True)
    subscribers = models.ManyToManyField('Account', blank=True)

    # cover photo position
    cover_photo_position = models.CharField(max_length=225, null=True, blank=True)

    # more info
    position = models.CharField(max_length=255, null=True, blank=True)
    primary_expertise = models.ForeignKey('Skill', related_name='primary_expertise', null=True, blank=True)
    expertise = models.ManyToManyField('Skill', related_name='expertise', blank=True)

    completion = models.ManyToManyField('AccountCompletionTask', blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activated = models.BooleanField(default=False)

    # billing info
    credits = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    objects = AccountManager()

    # type of user tutor or student
    user_type = models.CharField(max_length=225, null=True, blank=True)

    # optional user profile
    company = models.CharField(max_length=225, null=True, blank=True)
    personal_website = models.CharField(max_length=255, null=True, blank=True)
    social_accounts = models.CharField(max_length=255, null=True, blank=True)

    # edit account 
    language = models.CharField(max_length=225, null=True, blank=True)
    secondary_email = models.EmailField(max_length=225, null=True, blank=True)
    activation_account = models.BooleanField(default=True)

    is_admin   = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    _profile_picture = None
    _cover_photo = None

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args,**kwargs)
        self._profile_picture = self.profile_picture
        self._cover_photo = self.cover_photo

    def __str__(self):
        return "{email}".format(email=self.email)

    def save(self, *args, **kwargs):
        if not self.timezone:
            self.timezone = self.get_gmt()

        if self.profile_picture != self._profile_picture and self._profile_picture !='':
            self.delete_profile_picture()

        if self.cover_photo != self._cover_photo and self._cover_photo !='':
            self.delete_cover_photo()

        return super(Account, self).save(*args, **kwargs)
        self._profile_picture = self.profile_picture
        self._cover_photo = self.cover_photo

    def delete_profile_picture(self, empty_image=False):
        image_path = os.path.join(settings.MEDIA_ROOT, str(self._profile_picture))

        try:
            os.remove(image_path)
        except Exception as e:
            pass

        if empty_image:
            self.profile_picture =''

    def delete_cover_photo(self, empty_image=False):
        image_path = os.path.join(settings.MEDIA_ROOT, str(self._cover_photo))

        try:
            os.remove(image_path)
        except Exception as e:
            pass

        if empty_image:
            self.cover_photo =''

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
        return "{username}".format(username=self.email)

    def generate_confirm_key(self):
        """ Generate a new confirm key for this
            user.
        """
        from accounts.models import ConfirmationKey
        return ConfirmationKey.objects.create(user=self)

    def completion_percent(self):
        """ number of the completion percentage
        """
        percent = self.completion.all().aggregate(Sum('points'))
        return "{percent}".format(percent=percent['points__sum'] or 0)

    def get_profile_url(self):
        return reverse('profile', args=[self.id])

    def get_gmt(self):
        return "GMT {}".format(self.get_gmtzone(self.city))

    def _send_confirmation_email(self):
        """ Send confirmation key to user.
        """
        confirm_key = self.generate_confirm_key()

        subject =   "Swift Tutorial Confirmation Key"
        message =   "Click link to activate\n\n" + settings.SITE_URL + "/activate/" + confirm_key.key
        email_to = confirm_key.user.email
        msg = EmailMessage(subject, message, to=[email_to])
        msg.send()


class Transaction(models.Model):
    """ transaction model
    """
    CREDIT = "credit"
    DEBIT = "debit"
    TRANS_TYPE = (
        (CREDIT, "Credit"),
        (DEBIT, "Debit"),
    )
    user = models.ForeignKey(Account)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    trans_type = models.CharField(max_length=10, choices=TRANS_TYPE, default=CREDIT)
    running_balance = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[{amount}] {type}".format(
            amount=self.amount, type=self.trans_type)


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


class Education(models.Model):
    """ education background
    """
    user = models.ForeignKey(Account)
    school = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    date_attended_fr = models.DateField(null=True, blank=True)
    date_attended_to = models.DateField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    def __str__(self):
        # if self.school or self.degree:
        return "{degree}".format(degree=self.degree)
        # else:
        #     return "No education"


class Skill(models.Model):
    """ Global tags
    """
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='skills/logo/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{name}".format(name=self.name)


class Badge(models.Model):
    """ User's achievement badges
    """
    title = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='badges/', null=True, blank=True)

    criteria = models.ManyToManyField('BadgeCriteria', blank=True)

    def __str__(self):
        return "{title}".format(title=self.title)


class BadgeCriteria(models.Model):
    """ Badge tutorials
    """
    desc = models.CharField(max_length=255)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{desc}".format(desc=self.desc)


def payment_notify(sender, **kwargs):
    """PayPal payment notification
    """
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        from accounts.models import Account, Transaction
        user = Account.objects.get(email = ipn_obj.payer_email)
        user.credits += ipn_obj.mc_gross
        user.save()
        Transaction.objects.create( user = user,
                                    amount = ipn_obj.mc_gross,
                                    description = ipn_obj.item_name
                                    )
valid_ipn_received.connect(payment_notify)
