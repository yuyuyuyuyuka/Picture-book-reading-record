from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


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
        
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', max_length=225, widget=forms.PasswordInput())
    
    
class RequestPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput()
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError('このメールアドレスに対応するユーザーは存在しません')
        return email