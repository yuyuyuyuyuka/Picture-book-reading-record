from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'picture_book_app/home.html'