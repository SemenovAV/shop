from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser


class CustomRegistrationForm(UserCreationForm):
    model = CustomUser
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputEmail',
                'type': 'email',
                'placeholder': _('Email')

            }))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'id': 'inputPassword1',
                'class': 'form-control',
                'placeholder': 'Password',
                'name': 'password',
                'required': '',
                'data-cip-id': 'inputPassword'
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Retype Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'id': 'inputPassword2',
                'class': 'form-control',
                'placeholder': 'Retype Password',
                'name': 'password',
                'required': '',
                'data-cip-id': 'inputPassword'
            }
        ),
    )
    class Meta:
        model = CustomUser
        fields = ("username", )
        field_classes = {'username': UsernameField}


class CustomAuthForm(AuthenticationForm):
    model = CustomUser
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputEmail',
                'type': 'email',
                'placeholder': _('Email')

            }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'id': 'inputPassword',
                'class': 'form-control',
                'placeholder': 'Password',
                'name': 'password',
                'required': '',
                'data-cip-id': 'inputPassword'
            }
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
