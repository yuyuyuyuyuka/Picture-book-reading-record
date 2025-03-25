from django.shortcuts import render
from .forms import RegistForm

def regist(request):
    user_form = RegistForm(request.POST or None)
    return render(request, 'accounts/registration.html', context={
        'user_form': user_form
    })