from django.shortcuts import render, redirect, get_object_or_404
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
def child_create(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)  #一旦保存止める
            child.family_id = request.user.family_id  #家族IDセット
            child.save()
            return redirect ('picture_book_app:child_list')
        
    else:
        form = ChildForm()
    return render(request, 'picture_book_app/child_registration.html', context={
        'form': form,
    })


# 子ども編集
def child_update(request, pk):
    child = get_object_or_404()
