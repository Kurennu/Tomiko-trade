from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("contacts", views.contacts, name='contacts'),
    path("catalog/", views.catalog, name='catalog'),
    path('catalog/<str:country>/', views.catalog, name='catalog_by_country'),
    path('catalog/car/<int:car_id>/', views.car_detail, name='car_detail')
]
