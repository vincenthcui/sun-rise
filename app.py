from celery import Celery
from celery.signals import worker_init

import celeryconfig


app = Celery(__name__)
app.config_from_object(celeryconfig)


@worker_init.connect()
def login_wechat(*args, **kwargs):
    import itchat
    itchat.auto_login(hotReload=True, enableCmdQR=True, statusStorageDir='run/wechat.pkl')
