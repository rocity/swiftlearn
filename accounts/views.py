from django.conf import settings
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse

from django.db.models import Q

from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404

from braces.views import LoginRequiredMixin
from events.models import Event

from .forms import SignupForm, LoginForm, ResetPasswordForm, ChangePasswordForm
from .models import ConfirmationKey, Account

from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.mail import send_mail
from swiftlearn.settings import DEFAULT_FROM_EMAIL

import json

class SignupView(TemplateView):
    """ Registration view for new learners
    """
    template_name = 'accounts/signup.html'

    def get(self, *args, **kwargs):
        form = SignupForm()
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = SignupForm(self.request.POST)
        if form.is_valid():
            instance = form.save()           
            instance._send_confirmation_email() # activate account
            # login user
            instance.backend = settings.AUTH_BACKEND
            login(self.request, instance)
            success = "success"
            return HttpResponse(json.dumps(success))
        else:
            if self.request.is_ajax():
                errors_dict = { }
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = str(e)
                return HttpResponseBadRequest(json.dumps(errors_dict))
        return render(self.request, self.template_name, {'form': form})


class LoginView(TemplateView):
    """ Login view for users
    """
    template_name = 'accounts/login.html'

    def get(self, *args, **kwargs):
        form = LoginForm()
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = LoginForm(data=self.request.POST)
        if form.is_valid():
            login(self.request, form.user_cache)
            return HttpResponseRedirect(reverse('dashboard'))
        return render(self.request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """ Logout View
    """
    def get(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('login'))


class DashboardView(LoginRequiredMixin, TemplateView):
    """ Dashboard View
    """
    template_name = 'accounts/dashboard.html'
    
    def get(self, *args, **kwargs):
        feed = Event.objects.all().order_by('-date_created')
        return render(self.request, self.template_name, {'feed': feed})


class ProfileView(LoginRequiredMixin, TemplateView):
    """ user's profile
    """
    template_name = 'accounts/profile.html'

    def get(self, *args, **kwargs):
        user_id = kwargs.get('user_id')
        profile = get_object_or_404(Account, id=user_id) if user_id else self.request.user
        return render(self.request, self.template_name, {'profile': profile})


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
                        'domain': self.request.META['HTTP_HOST'],
                        'site_name': 'Swiftkind Tutorials',
                        'uid': urlsafe_base64_encode(force_bytes(user)),
                        'token': default_token_generator.make_token(user),
                        }
                    #send reset pass link to user
                    email_template_name = 'accounts/password_reset_email.html'
                    subject = "Swiftkind Password Reset"
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
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