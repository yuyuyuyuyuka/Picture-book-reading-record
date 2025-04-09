from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Child
from .forms import ChildForm

class HomeView(TemplateView):
    template_name = 'picture_book_app/home.html'
    

# 子ども一覧画面
def child_list(request):
    children = Child.objects.filter(family_id=request.user.family_id)
    return render(request, 'picture_book_app/child_list.html', context={
        'children':children,
    })
    
# 子ども登録画面
def child_regist(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('picture_book_app:child_list')
        
    else:
        form = ChildForm()
    return render(request, 'picture_book_app/child_registration.html', context={
        'form': form,
    })