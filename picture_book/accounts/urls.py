from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('regist/',views.regist, name='regist'),
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('request_password_reset/', views.request_password_reset, name='request_password_reset'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/',views.password_reset_complete, name='password_reset_complete'),
]
