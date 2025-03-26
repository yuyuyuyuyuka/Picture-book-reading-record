from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistForm, UserLoginForm, RequestPasswordResetForm
from .models import PasswordResetToken
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import uuid

# アカウント作成
def regist(request):
    user_form = RegistForm(request.POST or None)
    if user_form.is_valid():
        user = user_form.save()
        login(request, user)
        messages.success(request,'アカウントが作成されました')
        return redirect ('picture_book_app: home')
    return render(request, 'accounts/registration.html', context={
        'user_form': user_form
    })
    
# ログイン
def user_login(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        # 認証処理
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            messages.success(request, 'ログインできました')
            return redirect('picture_book_app: home')
        else:
            messages.error(request,'メールアドレスまたはバスワードが間違っています')
    return render(request, 'accounts/login.html', context={
        'login_form': login_form
    })
    
# ログアウト
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('accounts:login')

# パスワード再設定
def request_password_reset(request):
    form = RequestPasswordResetForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email=email)
        # 新しいトークン作成
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        if not created:
            password_reset_token.token = uuid.uuid4
            password_reset_token.used = False
            password_reset_token.save()
        user.is_active = False
        user.save()
        print(password_reset_token.token)
    return render(request, 'accounts/password_reset_form.html', context={
        'reset_form':form
    })