from celery import Celery

import celeryconfig


app = Celery(__name__)
app.config_from_object(celeryconfig)
