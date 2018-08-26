import os
from celery.schedules import crontab

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

broker_db = int(os.getenv('BROKER_DB', 0))
broker_url = 'redis://%s:%d/%d' % (redis_host, redis_port, broker_db)

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
receive_user = os.getenv('RECEIVE_USER', 'filehelper')
receive_user = receive_user.split(',')

store_db = int(os.getenv('STORE_DB', 1))
store_url = 'redis://%s:%d/%d' % (redis_host, redis_port, store_db)
