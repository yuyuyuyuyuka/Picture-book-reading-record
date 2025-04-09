from django.urls import path
from .views import HomeView
from . import views

app_name = 'picture_book_app'


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('child_list/', views.child_list, name='child_list'),
    path('child_create/', views.child_create, name='child_create'),
    path('child_update/<int:pk>/', views.child_update, name='child_update'),
    path('child_delete/<int:pk>/', views.child_delete, name='child_delete'),
]
