from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Child

class HomeView(TemplateView):
    template_name = 'picture_book_app/home.html'
    

# 子ども一覧画面
def child_list(request):
    children = Child.objects.filter(family_id=request.user.family_id)
    return render(request, 'picture_book_app/child_list.html', context={
        'children':children,
    })