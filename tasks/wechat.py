import itchat
from celery.utils.log import get_task_logger

from app import app
from celeryconfig import receive_user


logger = get_task_logger(__name__)


def send_msg(msg):
    for user in receive_user:
        send_msg_to_user.delay(user, msg)


@app.task(name='wechat.send_msg',  rate_limit='1/s')
def send_msg_to_user(user, msg):
    logger.info('send msg to %s: %s', user, msg)
    itchat.send(msg, toUserName=user)
