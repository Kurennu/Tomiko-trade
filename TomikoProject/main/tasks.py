from celery import Celery
from main.reviews import main as parse_reviews_main
from main.clips import main as parse_clips_main

app = Celery('tasks')


@app.task
def parse_reviews():
    parse_reviews_main()


@app.task
def parse_vk_clips():
    parse_clips_main()