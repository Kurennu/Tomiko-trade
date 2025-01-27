from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Cars, Brands
import json
from django.http import JsonResponse
from .utils import *

def index(request):
    cars = Cars.objects.all() 
    return render(request, 'index.html', {'cars': cars})

def contacts(request):
    return render(request, 'contacts.html')

# Функция для карточек и пагинатора
# def car_catalog(request):
#     cars = Cars.objects.all()
#     items_per_page = 12 # Сколько карточек будет на странице (в дизайне вроде 12, так что пока 12)
#     paginator = Paginator(cars, items_per_page)

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'catalog.html', {'page_obj': page_obj})


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


def catalog(request):
    queryset = Cars.objects.all()
    

    brand = request.GET.get('brand')
    if brand:
        queryset = queryset.filter(brand_country__brand__iexact=brand)
    

    model = request.GET.get('model')
    if model:
        queryset = queryset.filter(model__iexact=model)
    

    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    if year_from:
        queryset = queryset.filter(year__gte=int(year_from))
    if year_to:
        queryset = queryset.filter(year__lte=int(year_to))
    
    mileage_from = request.GET.get('mileage_from')
    mileage_to = request.GET.get('mileage_to')
    if mileage_from:
        queryset = queryset.filter(mileage__gte=int(mileage_from))
    if mileage_to:
        queryset = queryset.filter(mileage__lte=int(mileage_to))
    
    engine_from = request.GET.get('engine_from')
    engine_to = request.GET.get('engine_to')
    if engine_from:
        queryset = queryset.filter(engine_volume__gte=int(engine_from))
    if engine_to:
        queryset = queryset.filter(engine_volume__lte=int(engine_to))
    
    transmission = request.GET.get('transmission')
    if transmission:
        queryset = queryset.filter(transmission__iexact=transmission)
    
    drive = request.GET.get('drive')
    if drive:
        queryset = queryset.filter(drive__iexact=drive)
    
    color = request.GET.get('color')
    if color:
        queryset = queryset.filter(color__iexact=color)
    
    existing_brands = Cars.objects.values_list('brand_country__brand', flat=True).distinct()
    brands = list(existing_brands)

    models_by_brand = {}
    for brand in brands:
        models = list(Cars.objects.filter(brand_country__brand=brand)
                     .values_list('model', flat=True)
                     .distinct())
        models_by_brand[brand] = models

    transmissions = list(Cars.objects.values_list('transmission', flat=True).distinct())
    drives = list(Cars.objects.values_list('drive', flat=True).distinct())
    colors = list(Cars.objects.values_list('color', flat=True).distinct())
    

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'brands_json': json.dumps(brands),
        'models_by_brand': json.dumps(models_by_brand),
        'transmissions_json': json.dumps(transmissions),
        'drives_json': json.dumps(drives),
        'colors_json': json.dumps(colors),
    }
    
    return render(request, 'catalog.html', context)



def calculate_car_duty(request, car_id):
    try:
        car = Cars.objects.get(id=car_id)
        total_duty = calculate_total_duty(car)
        final_price = car.price * get_currency_rate(car.brand.country_currency) + total_duty
        return JsonResponse({'total_duty': total_duty, 'final_price': final_price})
    except Cars.DoesNotExist:
        return JsonResponse({'error': 'Car not found'}, status=404)