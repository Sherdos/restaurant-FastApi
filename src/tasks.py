from celery import Celery

celery = Celery('tasks',  broker='amqp://admin:12345@localhost:5672')

@celery.task
def update_admin_xlsx():
    pass



celery.conf.beat_schedule = {
    'sync-every-15-seconds': {
        'task': 'src.tasks.update_admin_xlsx',
        'schedule': 15.0,  # Интервал в секундах
    },
}

