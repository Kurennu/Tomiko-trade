from celery import Celery
from main.reviews import main

app = Celery('tasks')


@app.task
def parse_reviews():
    main()