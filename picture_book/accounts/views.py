from django.shortcuts import render, redirect
from .forms import RegistForm
from django.contrib.auth.password_validation import validate_password

def regist(request):
    user_form = RegistForm(request.POST or None)
    if user_form.is_valid():
        user = user_form.save()
    else:
        user_form = RegistForm()
    return render(request, 'accounts/registration.html', context={
        'user_form': user_form
    })