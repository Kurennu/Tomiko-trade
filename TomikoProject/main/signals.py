from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cars
from .utils import calculate_total_duty, get_currency_rate
from decimal import Decimal

@receiver(pre_save, sender=Cars)
def calculate_and_update_price(sender, instance, **kwargs):
    total_duty = calculate_total_duty(instance)
    original_price = instance.price
    rate = get_currency_rate(instance.brand_country.currency_code)
    if rate is not None:
        price_in_rubles = Decimal(original_price) * Decimal(rate)
        final_price = price_in_rubles + total_duty
        instance.price_new = int(final_price)
    else:
        print(f"Не найден курс для валюты {instance.brand_country.currency_code} для автомобиля {instance.id}")