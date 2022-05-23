from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class' :'form-control',
        'placeholder': 'Username'
        }
    ),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' :'form-control',
        'placeholder': 'Password'
        }
    ),required=True)


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class' :'form-control',
        'placeholder': 'Username'
        }
    ),required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' :'form-control',
        'placeholder': 'Password'
        }
    ),required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' :'form-control',
        'placeholder': 'Confirm Password'
        }
    ),required=True)


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'autofocus': True,
        'class' :'form-control',
        'placeholder': 'New password'
        }
    ),required=True)

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' :'form-control',
        'placeholder': 'New password confirmation'
        }
    ),required=True)
