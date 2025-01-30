from celery import shared_task
from django.core.management import call_command
from main.reviews import main as parse_reviews_main
from main.clips import main as parse_clips_main


@shared_task
def parse_reviews():
    parse_reviews_main()


@shared_task
def parse_vk_clips():
    parse_clips_main()


@shared_task
def update_car_prices_task():
    call_command('update_car_prices')