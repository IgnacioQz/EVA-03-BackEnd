from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('formulario/', views.formulario, name="formulario"),
    path('sala/<int:id>/', views.detalleSala, name='sala_detalle'),
]

