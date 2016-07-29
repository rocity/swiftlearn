from django.conf import settings
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView, View
from django.shortcuts import render, get_object_or_404

from braces.views import LoginRequiredMixin
from events.models import Event

from .forms import SignupForm, LoginForm
from .models import ConfirmationKey, Account


class SignupView(TemplateView):
    """ Registration view for new learners
    """
    template_name = 'accounts/signup.html'

    def get(self, *args, **kwargs):
        form = SignupForm()
        return render(self.request, self.template_name, {'form': form, 'has_error': False})

    def post(self, *args, **kwargs):
        form = SignupForm(self.request.POST)
        if form.is_valid():
            instance = form.save()           
            instance._send_confirmation_email() # activate account
            # login user
            instance.backend = settings.AUTH_BACKEND
            login(self.request, instance)

            return HttpResponseRedirect(reverse('dashboard'))
        return render(self.request, self.template_name, {'form': form, 'has_error': True})


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
