from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Record

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'mobile']
