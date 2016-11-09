import json
import os
import uuid

from django.conf import settings
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest

from django.db.models import Q

from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404

from braces.views import LoginRequiredMixin
from events.models import Event, Feedback, Bookmark

from paypal.standard.forms import PayPalPaymentsForm

from .forms import ( 
    SignupForm, 
    LoginForm, 
    ResetPasswordForm, 
    ChangePasswordForm, 
    EditProfileForm, 
    EditAccountForm,
    EditProfilePicForm,
    RemoveProfilePicForm,
    CoverPhotoForm,
    RemoveCoverPhotoForm
    )
from .models import ConfirmationKey, Account, Skill, Education, Transaction

from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.mail import send_mail

import base64
from django.core.files.base import ContentFile


class IndexView(TemplateView):
    """ Main page of the site
    """
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))
        return render(self.request, self.template_name, {})


class SignupView(TemplateView):
    """ Registration view for new learners
    """
    template_name = 'accounts/signup.html'

    def get(self, *args, **kwargs):
        user_type = self.request.GET.get('t')
        if not user_type == 'tutor' and not user_type == 'student':
            raise Http404()
        form = SignupForm()
        return render(self.request, self.template_name, {'form': form,'user_type':user_type})


class LoginView(TemplateView):
    """ Login view for users
    """
    template_name = 'accounts/login.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))
        form = LoginForm()
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = LoginForm(data=self.request.POST)
        if form.is_valid():
            user = Account.objects.get(email=form.user_cache)
            if user.expertise.exists():
                login(self.request, form.user_cache)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                login(self.request, form.user_cache)
                return HttpResponseRedirect(reverse('user_category'))
        return render(self.request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """ Logout View
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('login'))


class DashboardView(LoginRequiredMixin, TemplateView):
    """ Dashboard View
    """
    template_name = 'accounts/dashboard.html'
    
    def get(self, *args, **kwargs):
        user = Account.objects.get(email=self.request.user)
        if user.expertise.count() == 0:
            return HttpResponseRedirect(reverse('user_category'))      
        return render(self.request, self.template_name, {})


class ProfileView(LoginRequiredMixin, TemplateView):
    """ user's profile
    """
    template_name = 'accounts/profile.html'

    def get(self, *args, **kwargs):
        user_id = kwargs.get('user_id')
        profile = get_object_or_404(Account, id=user_id) if user_id else self.request.user
        events = Event.objects.filter(educator=profile)
        feeds = Feedback.objects.all().order_by('-feed_date')

        return render(self.request, self.template_name, {'profile': profile,
                                                        'feeds':feeds,
                                                        'events':events
                                                        })


class EditProfileView(LoginRequiredMixin, TemplateView):
    """ User can edit his/her profile information
    """
    template_name = 'accounts/edit_profile.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        user = get_object_or_404(Account, email=self.request.user)
        transactions = Transaction.objects.filter(user=user).order_by('-date_created')
        paypal_dict = {
            "business" : settings.PAYPAL_RECEIVER_EMAIL,
            "item_name" : "Tutorial Payment",
            "invoice" : str(uuid.uuid4())[:8].upper(),
            "notify_url" : settings.SITE_URL + reverse('paypal-ipn'),
            "return_url" : settings.SITE_URL + "/profile/edit/",
            "cancel_return" : settings.SITE_URL + "/profile/edit/",
            "custom" : "Upgrade all users!",
        }

        account = Account.objects.get(email=self.request.user)
        education, create = Education.objects.get_or_create(user=account) 
        form = EditProfileForm(
            instance = account,
            initial = {
                'primary_expertise' : self.request.user.primary_expertise,
                'school' : education.school,
                'date_attended_fr' : education.date_attended_fr,
                'date_attended_to' : education.date_attended_to,
            })
        form2 = EditAccountForm(instance=account)
        form3 = ChangePasswordForm()
        form_paypal = PayPalPaymentsForm(initial=paypal_dict)
        return render(self.request, self.template_name, {'form':form, 
                                                        'form2':form2, 
                                                        'form3':form3,
                                                        'form_paypal':form_paypal,
                                                        'transactions':transactions
                                                        })

        
    def post(self, *args, **kwargs):
        form_identity = self.request.POST.get('form_identity', False)
        account = Account.objects.get(email=self.request.user)
        education, create = Education.objects.get_or_create(user=account) 
        form2 = EditAccountForm(instance=account)
        form3 = ChangePasswordForm()
        form = EditProfileForm(
            instance = account,
            initial = {
                'primary_expertise' : self.request.user.primary_expertise,
                'school' : education.school,
                'date_attended_fr' : education.date_attended_fr,
                'date_attended_to' : education.date_attended_to,
            })
        if form_identity == 'edit_profile':
            form = EditProfileForm(self.request.POST,instance=account)
            if form.is_valid():
                form_m = form.save(commit=False)
                form.save()
                form.save_m2m()
                return HttpResponseRedirect(reverse('dashboard'))
        elif form_identity == 'edit_account':
            form2 =  EditAccountForm(self.request.POST,instance=account)
            if form2.is_valid():
                form2.save()
        elif form_identity == 'edit_password':
            form3 = ChangePasswordForm(self.request.POST, instance=account, user=self.request.user)
            if form3.is_valid():
                instance = form3.save()
                instance.backend = settings.AUTHENTICATION_BACKENDS[0]
                login(self.request,instance)
                return HttpResponse(status=201)
            else:
                errors_dict = {}
                for error in form3.errors:
                    e = form3.errors[error]
                    errors_dict[error] = str(e)
                return HttpResponseBadRequest(json.dumps(errors_dict))
        elif form_identity == 'upload':
            form4 = EditProfilePicForm(self.request.POST, instance=account)
            data = self.request.POST.get('profile_picture')
            image_data = base64.b64decode(data.split(',')[1])
            image_name = self.request.POST.get('image_name')
            if form4.is_valid():
                form_m = form4.save(commit=False)
                form_m.profile_picture = ContentFile(image_data, image_name)
                form_m.save()

        elif form_identity =='remove':
            form5 = RemoveProfilePicForm(self.request.POST, instance=account)
            if form5.is_valid():
                instance = form5.save(commit=False)
                instance.profile_picture = ""
                instance.save()
                instance.delete_profile_picture()
                return HttpResponseRedirect(reverse('edit_profile'))
        elif form_identity == 'cover_photo':
            form6 = CoverPhotoForm(self.request.POST,self.request.FILES, instance=account)
            if form6.is_valid:
                form6.save()
                return HttpResponseRedirect(reverse('profileme'))

        elif form_identity == 'removecover':
            form7 = RemoveCoverPhotoForm(self.request.POST, instance=account)
            if form7.is_valid():
                instance = form7.save(commit=False)
                instance.cover_photo = ""
                instance.save()
                instance.delete_cover_photo()
                return HttpResponseRedirect(reverse('profileme'))

        return render(self.request, self.template_name,  {
            'form':form, 
            'form2':form2,
            'form3':form3, 
            'form_script': form_identity 
            })


class ActivationView(TemplateView):
    """ User Activation View
    """
    def get(self, *args, **kwargs):
        activate = get_object_or_404(ConfirmationKey, key=kwargs['key'])
        user = Account.objects.get(email=activate.user)
        
        if user.is_active == True:
            user.is_activated = True 
            user.save()
            activate.is_used = True
            activate.save()
            ConfirmationKey.objects.filter(user=activate.user, is_used=False).delete()
            return HttpResponseRedirect(reverse('dashboard'))


class ResendActivationView(TemplateView):
    """ Resend Activation Key to user
    """
    def get(self, *args, **kwargs):
        user = Account.objects.get(email=self.request.user)
        user._send_confirmation_email()

        return HttpResponseRedirect(reverse('dashboard'))


class SearchView(View):
    """Search for Preffered Tutorial
    """
    template_name = 'accounts/search.html'

    def get(self, *args, **kwargs):
        feed = Event.objects.all().order_by('-date_created')
        search = self.request.GET.get('q')
        if search:
            feed = feed.filter(
                Q(title__icontains=search)|
                Q(educator__last_name__icontains=search)|
                Q(educator__first_name__icontains=search)|
                Q(info__icontains=search)|
                Q(tags__name__icontains=search)
                )
        return render(self.request, self.template_name,{'feed':feed})


class ResetPasswordRequestView(TemplateView):
    """ User reset password request view
    """
    template_name = 'accounts/password_reset.html'

    def get(self, *args, **kwargs):
        form = ResetPasswordForm()
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = ResetPasswordForm(self.request.POST)
        if form.is_valid():
            data  = form.cleaned_data['email']
            users = Account.objects.filter(email=data)
            if users.exists():
                for user in users:
                    c = {
                        'email': user,
                        'domain': settings.SITE_URL,
                        'site_name': 'Swiftkind Tutorials',
                        'uid': urlsafe_base64_encode(force_bytes(user)),
                        'token': default_token_generator.make_token(user),
                        }
                    #send reset pass link to user
                    email_template_name = 'accounts/password_reset_email.html'
                    subject = "Swiftkind Password Reset"
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                messages.success(self.request, "Check your inbox to continue reseting password.")
                return render(self.request, self.template_name, {'form': form})
            else:
                messages.error(self.request, 'The email does not exist.')
                return render(self.request, self.template_name, {'form': form})

        return render(self.request, self.template_name, {'form': form})


class ResetPasswordConfirmView(TemplateView):
    """ User change password view
    """
    template_name = 'accounts/password_change.html'

    def get(self, *args, **kwargs):
        form = ChangePasswordForm()
        return render(self.request, self.template_name, {'form': form})

    def post(self, request, uidb64=None, token=None):
        form = ChangePasswordForm(self.request.POST)

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = Account.objects.get(email=uid)
        except Account.DoesNotExist:
            user=None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request, 'Password reset has been unsuccessful.')
                return render(self.request, self.template_name, {'form': form})
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return render(self.request, self.template_name, {'form': form})


class FeedView(View):
    template_name = 'accounts/pagination.html'

    def get(self, *args, **kwargs):
        feed = Event.objects.all().order_by('-date_created')

        # check for bookmark status of logged user and the event
        for item in feed:
            try:
                bookmark_object = item.bookmark_set.get(event_title=item.id,
                                                        user=self.request.user.id,
                                                        active=True)

                item.bookmarked = True
                item.bookmark = bookmark_object
            except Bookmark.DoesNotExist:
                item.bookmarked = False

        return render(self.request, self.template_name, {'feed': feed})


class SubscribeView(TemplateView):
    """ Subscribe to other user
    """
    def get(self, *args, **kwargs):
        subscriber = Account.objects.get(email=self.request.user)
        user_id = kwargs.get('user_id')
        user = Account.objects.get(id=user_id)
        user.subscribers.add(subscriber)
        
        return HttpResponseRedirect(reverse('profile', kwargs={'user_id':user_id}))


class UnsubscribeView(TemplateView):
    """ Unsubscribe from other user
    """
    def get(self, *args, **kwargs):
        subscriber = Account.objects.get(email=self.request.user)
        user_id = kwargs.get('user_id')
        user = Account.objects.get(id=user_id)
        user.subscribers.remove(subscriber)
        
        return HttpResponseRedirect(reverse('profile', kwargs={'user_id':user_id}))


class UserCategoryView(LoginRequiredMixin, TemplateView):
    """ Category Selection View that can proceed to the Dashboard view
    """
    template_name = 'accounts/user_select_category.html'

    def get(self, *args, **kwargs):
        images = Skill.objects.all()
        return render(self.request, self.template_name, {'images':images})
 
    def post(self, *args, **kwargs):
        images = Skill.objects.all()

        user = Account.objects.get(email=self.request.user)
        categories = self.request.POST.getlist('category')
        if not categories:
            message = "Required to select categories!"
        else:
            user.expertise = categories
            user.save()
            return HttpResponseRedirect(reverse('dashboard'))
        return render(self.request, self.template_name, {'images':images,'message':message})

class BookmarksView(LoginRequiredMixin, TemplateView):
    """ Display events that the user bookmarked
    """
    template_name = 'accounts/bookmarks.html'

    def get(self, *args, **kwargs):
        bookmarks = Bookmark.objects.filter(user=self.request.user.id, active=True)
        return render(self.request, self.template_name, {'bookmarks': bookmarks})