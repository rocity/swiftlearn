from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import Account, Skill, Education
from events.models import Event

import datetime

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
    first_name = forms.CharField(widget=forms.TextInput({
        'class':'input form-control',
        'placeholder': 'First Name'
         }))
    last_name = forms.CharField(widget=forms.TextInput({
        'class':'input form-control',
        'placeholder': 'Last Name'
         }))

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')
   

class LoginForm(AuthenticationForm):
    """ form for user login
    """
    username = forms.CharField(max_length=30, 
                               widget=forms.TextInput(attrs={
                                'type': 'email',
                                'class': 'form-control',
                                'name': 'username',
                                'placeholder': 'Email address'
                                }))
    password = forms.CharField(max_length=30, 
                               widget=forms.PasswordInput(attrs={
                                'class': 'form-control',
                                'name': 'password',
                                'placeholder': 'Password'
                                }))
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
        confirm_password = self.data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Password didn't match. Try again.")

        return password


class EditProfileForm(forms.ModelForm):
    """ form for user profile 
    """
    overview = forms.CharField(widget=forms.Textarea({
        'class':'input form-control',
         'rows':'2'
         }))
    first_name = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }))
    middle_name = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }),required=False)
    last_name = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }))
    primary_expertise = forms.ModelChoiceField(
        queryset=Skill.objects.all(), 
        widget=forms.Select({
        'class':'input form-control'
        }))
    expertise = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(), 
        widget=forms.SelectMultiple({
        'class':'input form-control'
        }))
    country = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }))
    phone = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }))
    city = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }))
    timezone = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }))
    school = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }), required=False)
    date_attended_fr = forms.CharField(widget=forms.TextInput({
        'type':'date',
        'class':'input form-control'
        }), required=False)
    date_attended_to = forms.CharField(widget=forms.TextInput({
        'type':'date',
        'class':'input form-control'
        }), required=False)
    company = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }),required=False)
    personal_website = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }),required=False)


    class Meta:
        model = Account
        fields = (
            'overview',
            'first_name',
            'middle_name',
            'last_name',
            'primary_expertise',
            'expertise',
            'country',
            'phone',
            'city',
            'timezone',
            'school',
            'date_attended_fr',
            'date_attended_to',
            'company',
            'personal_website'
            )

    def save(self, commit=True):
        instance = super(EditProfileForm, self).save(commit=False)
        if commit:
            date_fr = datetime.datetime.strptime( self.cleaned_data.get('date_attended_fr'),"%Y-%m-%d").date()
            date_to = datetime.datetime.strptime(self.cleaned_data.get('date_attended_to'), "%Y-%m-%d").date()
            edu = Education.objects.get(user = instance)
            edu.school = self.cleaned_data.get('school')
            edu.date_attended_to =date_to
            edu.date_attended_fr =date_fr
            edu.save()
            instance.save()
        return instance


class EditAccountForm(forms.ModelForm):
    """ form for editing user account
    """
    email = forms.EmailField(widget=forms.EmailInput({
        'class':'input form-control'
        }))
    secondary_email = forms.EmailField(widget=forms.EmailInput({
        'class':'input form-control'
        }), required=False)
    language = forms.CharField(widget=forms.TextInput({
        'class':'input form-control'
        }))

    class Meta:
        model = Account 
        fields = (
            'email',
            'secondary_email',
            'language'
            )


class ChangePasswordForm(forms.ModelForm):
    """ form for changing password
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('user',None)
        return super(ChangePasswordForm, self).__init__(*args,**kwargs)

    password = forms.CharField(widget=forms.PasswordInput({
        'class':'input form-control',
        'placeholder': 'Enter current password'
        }))
    new_password = forms.CharField(widget=forms.PasswordInput({
        'class':'input form-control',
        'placeholder': 'Enter new password'
        }))
    password_confirmation = forms.CharField(widget=forms.PasswordInput({
        'class':'input form-control',
        'placeholder': 'Enter corfirm password'
        }))
    
    class Meta:
        model = Account
        fields = (
            'password', 
            'new_password', 
            'password_confirmation'
            )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        email = self.request
        print(email)
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Incorrect Password!")
        return password

    def clean_new_password(self):
        new_password = self.data['new_password']
        password_confirmation = self.data['password_confirmation']
        if new_password != password_confirmation:
            raise forms.ValidationError("Password did'nt match!")
        return new_password

    def save(self, commit=True):
        instance = super(ChangePasswordForm, self).save(commit=False)
        if commit:
            instance.set_password(self.data['new_password'])
            user = instance.save()
        return instance


class EditProfilePicForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('profile_picture',)


class RemoveProfilePicForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('profile_picture',)


class CoverPhotoForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('cover_photo','cover_photo_position')


class RemoveCoverPhotoForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('cover_photo',)
