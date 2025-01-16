broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
beat_schedule = {
    'parse-reviews-daily': {
        'task': 'tasks.parse_reviews',
        'schedule': 86400.0,  # количество секунд в сутках, раз в сутки запускает скрипт
    },
}