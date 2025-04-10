from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Child, Book
from .forms import ChildForm, BookForm

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
    child = get_object_or_404(Child, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            return redirect('picture_book_app:child_list')
    
    else:
        form = ChildForm(instance=child)
    return render(request, 'picture_book_app/child_update.html', context={
        'form': form,
        'child': child,
    })


# 子ども削除
def child_delete(request, pk):
    child = get_object_or_404(Child, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        child.delete()
        return redirect('picture_book_app:child_list')
    
    return render(request, 'picture_book_app/child_update.html', context={
        'child': child,
    })


# 絵本新規登録画面
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('picture_book_app:book_list')
    else:
        form = BookForm()
    
    return render(request, 'picture_book_app/book_create.html', {
        'form': form,
    })


# 絵本一覧画面
def book_list(request):
    books = Book.objects.all()
    return render(request, 'picture_book_app/book_list.html', context={
        'books':books
    }) 