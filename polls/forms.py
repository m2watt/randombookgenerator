from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.core import validators


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = {
            'email',

        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()


class Loginform(forms.Form):
    email = forms.CharField(max_length=30, label="Enter email", widget=forms.EmailInput)
    password = forms.CharField(max_length=30, label='Password',
                               widget=forms.PasswordInput)


