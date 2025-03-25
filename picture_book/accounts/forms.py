from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class RegistForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
        widgets = {
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput()
        }
        labels = {
            'username':'名前／ニックネーム',
            'email':'メールアドレス',
            'password1':'パスワード',
            'password2':'パスワード(再入力)',
        }