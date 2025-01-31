import sys
import os

print(sys.path)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TomikoProject.TomikoProject.settings')

from decimal import Decimal
from main.models import *



def get_currency_rate(currency):
    try:
        rate = CurrencyRate.objects.get(currency=currency).rate
        # print(f"Получен курс для валюты {currency}: {rate}")
        return rate
    except CurrencyRate.DoesNotExist:
        # print(f"Не найден курс для валюты {currency}")
        return None



def calculate_customs_fee(price_in_rubles):
    if price_in_rubles <= 200000:
        return 755
    elif 200000 < price_in_rubles <= 450000:
        return 1550
    elif 450000 < price_in_rubles <= 1200000:
        return 3100
    elif 1200000 < price_in_rubles <= 2700000:
        return 8530
    elif 2700000 < price_in_rubles <= 4200000:
        return 12000
    elif 4200000 < price_in_rubles <= 5500000:
        return 15500
    elif 5500000 < price_in_rubles <= 7000000:
        return 20000
    elif 7000000 < price_in_rubles <= 8000000:
        return 23000
    elif 8000000 < price_in_rubles <= 9000000:
        return 25000
    elif 9000000 < price_in_rubles <= 10000000:
        return 27000
    else:
        return 30000

  

def calculate_unified_rate(cars):
    try:
        engine_volume = int(cars.engine_volume)
    except ValueError:
        engine_volume = 0
    currency_code = cars.brand_country.currency_code
    rate = get_currency_rate(currency_code)
    if rate is None:
        raise ValueError(f"Не найден курс для валюты {currency_code}")
    price_in_rubles = Decimal(cars.price) * Decimal(rate)
    euro_rate = get_currency_rate('EUR')
    price_in_euro = price_in_rubles / Decimal(euro_rate)
    # print(f"Цена автомобиля в рублях: {price_in_rubles}, цена в евро: {price_in_euro}")

    age = 2024 - cars.year
    if age < 3:
        if price_in_euro <= 8500:
            result = max(price_in_euro * Decimal('0.54'), Decimal('2.5') * engine_volume)
        elif 8500 < price_in_euro <= 16700:
            result = max(price_in_euro * Decimal('0.48'), Decimal('3.5') * engine_volume)
        elif 16700 < price_in_euro <= 42300:
            result = max(price_in_euro * Decimal('0.48'), Decimal('5.5') * engine_volume)
        elif 42300 < price_in_euro <= 84500:
            result = max(price_in_euro * Decimal('0.48'), Decimal('7.5') * engine_volume)
        elif 84500 < price_in_euro <= 169000:
            result = max(price_in_euro * Decimal('0.48'), Decimal('15') * engine_volume)
        else:
            result = max(price_in_euro * Decimal('0.48'), Decimal('20') * engine_volume)
    elif 3 <= age <= 5:
        if engine_volume <= 1000:
            result = Decimal('1.5') * engine_volume
        elif 1000 < engine_volume <= 1500:
            result = Decimal('1.7') * engine_volume
        elif 1500 < engine_volume <= 1800:
            result = Decimal('2.5') * engine_volume
        elif 1800 < engine_volume <= 2300:
            result = Decimal('2.7') * engine_volume
        elif 2300 < engine_volume <= 3000:
            result = Decimal('3') * engine_volume
        else:
            result = Decimal('3.6') * engine_volume
    else:
        if engine_volume <= 1000:
            result = Decimal('3') * engine_volume
        elif 1000 < engine_volume <= 1500:
            result = Decimal('3.2') * engine_volume
        elif 1500 < engine_volume <= 1800:
            result = Decimal('3.5') * engine_volume
        elif 1800 < engine_volume <= 2300:
            result = Decimal('4.8') * engine_volume
        elif 2300 < engine_volume <= 3000:
            result = Decimal('5') * engine_volume
        else:
            result = Decimal('5.7') * engine_volume

    result_in_rubles = result * Decimal(euro_rate)
    # print(f"Единая ставка (евро): {result}, в рублях: {result_in_rubles}")
    return result_in_rubles



def calculate_scrapping_fee(cars):
    age = 2024 - cars.year
    try:
        engine_volume = int(cars.engine_volume)
    except ValueError:
        engine_volume = 0
    if age < 3:
        if engine_volume <= 1000:
            return 20000 * Decimal('0.17')
        elif 1000 < engine_volume <= 2000:
            return 20000 * Decimal('0.17')
        elif 2000 < engine_volume <= 3000:
            return 20000 * Decimal('0.17')
        else:
            return 0
    else:
        if engine_volume <= 1000:
            return 20000 * Decimal('0.26')
        elif 1000 < engine_volume <= 2000:
            return 20000 * Decimal('0.26')
        elif 2000 < engine_volume <= 3000:
            return 20000 * Decimal('0.26')
        else:
            return 0



def calculate_total_duty(cars):
    valid_countries = ['Китай', 'Корея', 'Япония']
    if cars.brand_country is None or cars.brand_country.country not in valid_countries:
        return 0
    if cars.brand_country is None:
        # print(f"Информация о стране бренда автомобиля {cars.id} отсутствует. Пропустить расчет таможенной пошлины.")
        return 0 
    currency_code = cars.brand_country.currency_code
    # print(f"Автомобиль {cars.id} соответствует марке страны {cars.brand_country.country} и код валюты {currency_code}.")
    if currency_code is None:
        # print(f"Автомобиль {cars.id} не имеет кода валюты страны бренда {cars.brand_country.country}, поэтому расчет таможенной пошлины пропущен.")
        return 0 
    rate = get_currency_rate(currency_code)
    if rate is None:
        # print(f"Не найден курс для валюты {currency_code}，пропустить расчет таможенных пошлин.")
        return 0 
    price_in_rubles = Decimal(cars.price) * Decimal(rate)
    # print(f"Цена автомобиля в исходной валюте: {cars.price}, курс: {rate}, цена в рублях: {price_in_rubles}")

    customs_fee = calculate_customs_fee(price_in_rubles)
    # print(f"Таможенное оформление: {customs_fee}")

    unified_rate = calculate_unified_rate(cars)
    # print(f"Единая ставка: {unified_rate}")
    
    scrapping_fee = calculate_scrapping_fee(cars)
    # print(f"Утилизационный сбор: {scrapping_fee}")

    return customs_fee + unified_rate + scrapping_fee