from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class RegistForm(forms.ModelForm):
    
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password':forms.PasswordInput
        }