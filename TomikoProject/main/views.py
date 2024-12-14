from django.shortcuts import render
from .cars_models import Cars

def index(request):
    return render(request, 'index.html')

def catalog_view(request): # Функция для чтения бд и передачи машинок в каталог
    cars = Cars.objects.all() # Получаем все машинки из таблицы cars
    return render(request, 'catalog.html', {'cars': cars}) # Передаем данные в шаблон
