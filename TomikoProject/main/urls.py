from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("contacts", views.contacts, name='contacts'),
    path("catalog/", views.car_catalog, name='catalog'),
]
