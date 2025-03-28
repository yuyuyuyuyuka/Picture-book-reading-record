from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

# 新規アカウント登録
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

# ログインフォーム
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', max_length=225, widget=forms.PasswordInput())
    
# パスワードリセット
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
    
# 新しいパスワードの入力画面でパスワードと再入力のパスワードが一致しない場合のエラー表示
class NewSetPasswordForm(forms.Form):
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（再入力）', widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('パスワードが一致しません')
        else:
            raise ValidationError('パスワードを設定してください')
        return password2