from django.core.management.base import BaseCommand
from main.models import Cars
from main.utils import calculate_total_duty, get_currency_rate
from decimal import Decimal

class Command(BaseCommand):
    def handle(self, *args, **options):
        cars = Cars.objects.all()
        for car in cars:
            original_price = car.price
            total_duty = calculate_total_duty(car)
            currency_code = car.brand_country.currency_code
            rate = get_currency_rate(currency_code)
            if rate is None:
                self.stdout.write(self.style.ERROR(f"Не найден курс для валюты {currency_code} для автомобиля {car.id}"))
                continue
            price_in_rubles = Decimal(original_price) * Decimal(rate)
            final_price = price_in_rubles + total_duty
            car.price_new = int(final_price)
            car.save()
        self.stdout.write(self.style.SUCCESS('Успешно обновленные цены на автомобили находятся в колонке price_new.'))