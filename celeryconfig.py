import os


broker_url = os.getenv('BROKER_URL', 'redis://localhost:6379/10')
result_backend = os.getenv('BACKEND_URL', 'redis://localhost:6379/11')

include = [
    'tasks.test',
]


# for business
alert_user = os.getenv('ALERT_USER', 'filehelper')
receive_user = os.getenv('RECEIVE_USER', 'filehelper')
store_url = os.getenv('STORE_URL', 'redis://localhost:6379/9')
