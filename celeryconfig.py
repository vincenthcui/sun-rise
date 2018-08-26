import os

from celery.schedules import crontab

broker_url = os.getenv('BROKER_URL', 'redis://localhost:6379/10')

include = [
    'tasks.test',
    'tasks.wechat',
    'tasks.source.zhzgj',
]

beat_schedule = {
    'source.zhzgj': {
        'task': 'source.zhzgj',
        'schedule': crontab(minute='*'),
    }
}

# for business
alert_user = os.getenv('ALERT_USER', 'filehelper')
receive_user = os.getenv('RECEIVE_USER', 'filehelper')
store_url = os.getenv('STORE_URL', 'redis://localhost:6379/9')
