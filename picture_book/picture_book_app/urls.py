from django.urls import path
from .views import HomeView
from . import views

app_name = 'picture_book_app'


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('child_list/', views.child_list, name='child_list'),
]
