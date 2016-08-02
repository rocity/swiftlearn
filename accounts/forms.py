from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import Account
from events.models import Event


class SignupForm(forms.ModelForm):
    """ form for new learners
    """
    email = forms.EmailField(widget=forms.EmailInput({
        'class': 'form-control', 'placeholder': 'E-mail address'
    }))
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control', 'placeholder': 'Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control', 'placeholder': 'Confirm password'
    }))

    class Meta:
        model = Account
        fields = ('email', 'password', 'confirm_password')

    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Password didn't match. Try again.")

        return password

    def save(self, commit=True, **kwargs):
        instance = super(SignupForm, self).save(commit=False)
        instance.username = instance._extract_username()

        if commit:
            instance.set_password(self.cleaned_data['password'])
            instance.save()

        return instance


class LoginForm(AuthenticationForm):
    """ form for user login
    """
    error_msg = "Email/Password is incorrect."

    def clean(self):
        """ validate user's credentials
        """
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not (email or password):
            raise forms.ValidationError(self.error_msg, code='invalid_login')

        # check if user's credentials are valid
        self.user_cache = authenticate(email=email, password=password)
        if self.user_cache is None or \
            not self.user_cache.is_active:
            raise forms.ValidationError(self.error_msg, code='invalid_login')

        return self.cleaned_data


class ResetPasswordForm(forms.Form):
    """ form for password reset
    """
    email = forms.EmailField(widget=forms.EmailInput({
        'class': 'form-control', 'placeholder': 'E-mail address'
    }))


class ChangePasswordForm(forms.ModelForm):
    """ form for user to change password
    """
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control', 'placeholder': 'New Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control', 'placeholder': 'Confirm password'
    }))

    class Meta:
        model = Account
        fields = ('password', 'confirm_password')

    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Password didn't match. Try again.")

        return password
