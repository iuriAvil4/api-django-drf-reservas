from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('salas/', views.get_salas, name='get_salas'),
    path('reservas/', views.get_reservas, name='get_reservas'),
    path('data/salas/', views.sala_manage, name='sala_manage'),
    path('data/reservas/', views.reserva_manage, name='reserva_manage'),
]