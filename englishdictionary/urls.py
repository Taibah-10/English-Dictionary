from django.contrib import admin
from django.urls import path
from englishdictionary import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
]