from django import forms
from django.core import validators
from django.forms import widgets

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =("avatar",)
