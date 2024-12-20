from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Cars

def index(request):
    cars = Cars.objects.all() 
    return render(request, 'index.html', {'cars': cars})

def contacts(request):
    return render(request, 'contacts.html')

# Функция для карточек и пагинатора
def car_catalog(request):
    cars = Cars.objects.all()
    items_per_page = 12 # Сколько карточек будет на странице (в дизайне вроде 12, так что пока 12)
    paginator = Paginator(cars, items_per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog.html', {'page_obj': page_obj})

# Функция для слайдера по странам
def slider_view(request):
    cars_korea = Cars.objects.filter(brand_country__country='Корея')
    cars_japan = Cars.objects.filter(brand_country__country='Япония')
    cars_china = Cars.objects.filter(brand_country__country='Китай')

    countries_and_cars = [
        ('Из Кореи', cars_korea),
        ('Из Японии', cars_japan),
        ('Из Китая', cars_china),
    ]

    context = {
        'countries_and_cars': countries_and_cars,
    }
    return render(request, 'index.html', context)
