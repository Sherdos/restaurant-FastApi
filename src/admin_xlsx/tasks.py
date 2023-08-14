import asyncio

from celery import Celery

from src.admin_xlsx.admin import update_admin
from src.config import (
    RABBITMQ_DEFAULT_HOST,
    RABBITMQ_DEFAULT_PASS,
    RABBITMQ_DEFAULT_USER,
)

celery = Celery('tasks', broker=f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_DEFAULT_HOST}:5672')


celery.conf.imports = ('src.admin_xlsx.tasks',)


@celery.task
def update_admin_xlsx():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_admin())


celery.conf.beat_schedule = {
    'sync-every-15-seconds': {
        'task': 'src.admin_xlsx.tasks.update_admin_xlsx',
        'schedule': 15.0,  # Интервал в секундах
    },
}
