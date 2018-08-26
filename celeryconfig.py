import os


broker_url = os.getenv('BROKER_URL', 'redis://localhost:6379/10')
result_backend = os.getenv('BACKEND_URL', 'redis://localhost:6379/11')

include = [
    'tasks.test',
]
