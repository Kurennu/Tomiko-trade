from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Cars

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

from django.shortcuts import render
from .models import Cars, Brands
from django.db.models import Q

from django.shortcuts import render
from .models import Cars, Brands
from django.core.paginator import Paginator
import json

def catalog(request):
    queryset = Cars.objects.all()
    
    # Brand filter
    brand = request.GET.get('brand')
    if brand:
        queryset = queryset.filter(brand_country__brand__iexact=brand)
    
    # Model filter
    model = request.GET.get('model')
    if model:
        queryset = queryset.filter(model__iexact=model)
    
    # Year range filter
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    if year_from:
        queryset = queryset.filter(year__gte=int(year_from))
    if year_to:
        queryset = queryset.filter(year__lte=int(year_to))
    
    # Mileage range filter
    mileage_from = request.GET.get('mileage_from')
    mileage_to = request.GET.get('mileage_to')
    if mileage_from:
        queryset = queryset.filter(mileage__gte=int(mileage_from))
    if mileage_to:
        queryset = queryset.filter(mileage__lte=int(mileage_to))
    
    # Engine volume range filter
    engine_from = request.GET.get('engine_from')
    engine_to = request.GET.get('engine_to')
    if engine_from:
        queryset = queryset.filter(engine_volume__gte=int(engine_from))
    if engine_to:
        queryset = queryset.filter(engine_volume__lte=int(engine_to))
    
    # Transmission filter
    transmission = request.GET.get('transmission')
    if transmission:
        queryset = queryset.filter(transmission__iexact=transmission)
    
    # Drive filter
    drive = request.GET.get('drive')
    if drive:
        queryset = queryset.filter(drive__iexact=drive)
    
    # Color filter
    color = request.GET.get('color')
    if color:
        queryset = queryset.filter(color__iexact=color)
    
    # Get unique values only for existing records
    existing_brands = Cars.objects.values_list('brand_country__brand', flat=True).distinct()
    brands = list(existing_brands)

    # Get models by brand
    models_by_brand = {}
    for brand in brands:
        models = list(Cars.objects.filter(brand_country__brand=brand)
                     .values_list('model', flat=True)
                     .distinct())
        models_by_brand[brand] = models

    # Get unique values for other filters
    transmissions = list(Cars.objects.values_list('transmission', flat=True).distinct())
    drives = list(Cars.objects.values_list('drive', flat=True).distinct())
    colors = list(Cars.objects.values_list('color', flat=True).distinct())
    
    # Pagination
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