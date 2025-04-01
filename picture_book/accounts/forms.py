from django import forms
from .models import User, Invitation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
import re

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
'''
# views.pyで↓のようになっているのにこのコードではuserを渡せない
# form = NewSetPasswordForm(request.POST or None, user=user)
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
        return password2 # ⇦ちなみにDjangoのフォームはclean()メソッドでcleaned_dataを返す必要があります
    
'''
class NewSetPasswordForm(forms.Form):
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（再入力）', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # userを受け取れるように__init__を追加
        super().__init__(*args, **kwargs)

    # バリデーション
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('パスワードは最低8文字以上必要です。')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('パスワードには英大文字・小文字を含めてください。')
        if not re.search(r'[0-9]', password):
            raise ValidationError('パスワードには数字を含めてください。')
        if self.user:
            if self.user.username in password or self.user.email.split('@')[0] in password:
                raise ValidationError('あなたの名前やメールアドレスを含むパスワードは使用できません。')
        if not re.match(r'^[A-Za-z0-9]+$', password):
            raise ValidationError('使える文字は半角英数字のみです。')

        return password


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError('パスワードが一致しません')
        else:
            raise ValidationError('パスワードを設定してください')
        return cleaned_data
    

# 家族招待URL作成画面
class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['family_id', 'user_id']
        

# 家族アカウント登録フォーム
class FamilyRegistForm(forms.ModelForm):
    password1 = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(),
        validators=[
            MinLengthValidator(8, 'パスワードは最低 8 文字以上必要です。'),
            RegexValidator(r'^[A-Za-z0-9]+$', '使える文字は半角英数になります。'),
            RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', '英大文字・小文字・数字を必ず含んでください。')
        ]
    )
    password2 = forms.CharField(label='パスワード(再入力)', widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
        labels = {
            'username': '名前／ニックネーム',
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード（再入力）',
        }
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            if password1.lower() in self.cleaned_data.get('username', '').lower():
                raise ValidationError('あなたの他の個人情報と似ているパスワードにはできません。')
            if password1.lower() in self.cleaned_data.get('email', '').lower():
                raise ValidationError('あなたの他の個人情報と似ているパスワードにはできません。')
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError('パスワードが一致しません')
        else:
            raise ValidationError('パスワードを設定してください')
        return cleaned_data