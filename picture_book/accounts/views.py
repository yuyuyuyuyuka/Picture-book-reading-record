from django.shortcuts import render, redirect
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout


def regist(request):
    user_form = RegistForm(request.POST or None)
    if user_form.is_valid():
        user = user_form.save()
    else:
        user_form = RegistForm()
    return render(request, 'accounts/registration.html', context={
        'user_form': user_form
    })
    
def user_login(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        # 認証処理
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
        else:
            login_form.add_error('email','メールアドレスまたはバスワードが間違っています')
    return render(request, 'accounts/login.html', context={
        'login_form': login_form
    })