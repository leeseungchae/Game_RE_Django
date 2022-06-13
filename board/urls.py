
from django.contrib import admin
from django.urls import path
from . import  views

app_name = 'board'

urlpatterns = [
    path('', views.home, name= 'board'),
    path('seacrh2/', views.seacrh2, name='seacrh2')]
