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
    path('book_create/', views.book_create, name='book_create'),
    path('book_list/', views.book_list, name='book_list'),
    path('book_update/<int:pk>/', views.book_update, name='book_update'),
    path('book_delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('book_detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('reading_record_create/', views.reading_record_create, name='reading_record_create'),
    path('reading_record_list/', views.reading_record_list, name='reading_record_list'),
    path('reading_record_detail/<int:pk>/', views.reading_record_detail, name='reading_record_detail'),
]
