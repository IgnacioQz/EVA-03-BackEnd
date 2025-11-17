from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('main/', views.main, name='main'),
    path('admin-reservas/', views.admin_view, name='admin'),
]

