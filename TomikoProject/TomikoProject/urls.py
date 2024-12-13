from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Путь для админки
    path('catalog/', include('main.urls')),  # Путь для каталога
]
