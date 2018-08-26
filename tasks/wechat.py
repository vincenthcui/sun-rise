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
    resp = itchat.send(msg, toUserName=user)
    if not resp:
        logger.error('send msg to %s faild: msg=%s, error=%s', user, msg, resp)
    else:
        logger.info('send msg to %s: %s', user, msg)
