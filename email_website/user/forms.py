from django import forms
# from django.contrib.auth.models import Group
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
#
from .models import User

from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

from .models import *


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'country',
                  'password1', 'password2']


class ValidationForm(forms.Form):
    validate_number = forms.CharField(max_length=50)
