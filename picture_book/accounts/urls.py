from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('regist/',views.regist, name='regist'),
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('request_password_reset/', views.request_password_reset, name='request_password_reset'),
    
]
