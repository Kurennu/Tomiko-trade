from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Cars, Brands, Clips, Reviews
import json

def index(request):
    clips = Clips.objects.all()
    cars = Cars.objects.all()
    reviews = Reviews.objects.all()
    context = {
        'clips': clips,
        'cars': cars,
        'reviews': reviews
    }
    return render(request, 'index.html', context)

def contacts(request):
    return render(request, 'contacts.html')

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


def catalog(request, country=None):
    queryset = Cars.objects.all()
    
    country_mapping = {
        'korea': 'Корея',
        'japan': 'Япония',
        'china': 'Китай'
    }
    
    title_mapping = {
        'korea': 'Автомобили из Кореи',
        'japan': 'Автомобили из Японии',
        'china': 'Автомобили из Китая'
    }
    

    if country and country in country_mapping:
        current_country = country_mapping[country]
        queryset = queryset.filter(brand_country__country=current_country)
        page_title = title_mapping[country]
        

        existing_brands = Cars.objects.filter(
            brand_country__country=current_country
        ).values_list('brand_country__brand', flat=True).distinct()
    else:
        page_title = 'Каталог автомобилей'
        current_country = None
        existing_brands = Cars.objects.values_list('brand_country__brand', flat=True).distinct()
    
    brands = list(existing_brands)
    

    models_by_brand = {}
    for brand in brands:
        models_query = Cars.objects.filter(brand_country__brand=brand)
        if current_country:
            models_query = models_query.filter(brand_country__country=current_country)
        
        models = list(models_query.values_list('model', flat=True).distinct())
        models_by_brand[brand] = models

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
        queryset = queryset.filter(engine_volume__gte=float(engine_from))
    if engine_to:
        queryset = queryset.filter(engine_volume__lte=float(engine_to))
    
    transmission = request.GET.get('transmission')
    if transmission:
        queryset = queryset.filter(transmission__iexact=transmission)
    
    drive = request.GET.get('drive')
    if drive:
        queryset = queryset.filter(drive__iexact=drive)
    
    color = request.GET.get('color')
    if color:
        queryset = queryset.filter(color__iexact=color)
    
 
    transmissions_query = Cars.objects
    drives_query = Cars.objects
    colors_query = Cars.objects
    
    if current_country:
        transmissions_query = transmissions_query.filter(brand_country__country=current_country)
        drives_query = drives_query.filter(brand_country__country=current_country)
        colors_query = colors_query.filter(brand_country__country=current_country)
    
    transmissions = list(transmissions_query.values_list('transmission', flat=True).distinct())
    drives = list(drives_query.values_list('drive', flat=True).distinct())
    colors = list(colors_query.values_list('color', flat=True).distinct())
    
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'brands_json': json.dumps(brands),
        'models_by_brand': json.dumps(models_by_brand),
        'transmissions_json': json.dumps(transmissions),
        'drives_json': json.dumps(drives),
        'colors_json': json.dumps(colors),
        'page_title': page_title,
        'current_country': country,
    }
    
    return render(request, 'catalog.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    similar_cars = Cars.objects.filter(brand_country__brand=car.brand_country.brand).exclude(id=car.id)[:4]
    
    context = {
        'car': car,
        'similar_cars': similar_cars,
    }
    return render(request, 'product.html', context)


def promo(request):
    return render(request, 'promo.html')

def error(request):
    return render(request, '405.html')