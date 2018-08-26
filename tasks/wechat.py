import itchat
from celery.utils.log import get_task_logger

from app import app
from celeryconfig import receive_user
from utils import cached


logger = get_task_logger(__name__)


def send_msg(msg):
    for user in receive_user:
        send_msg_to_user.delay(user, msg)


@cached
def get_user_name(user):
    try:
        return itchat.search_friends(name=user)[0]['UserName']
    except IndexError:
        return user


@app.task(name='wechat.send_msg',  rate_limit='1/s')
def send_msg_to_user(user, msg):
    username = get_user_name(user)
    if username is None:
        logger.warn('can not find username for user %s', user)
        return

    resp = itchat.send(msg, toUserName=username)
    if not resp:
        logger.error('send msg to %s(%s) failed: msg=%s, error=%s', user, username, msg, resp)
    else:
        logger.info('send msg to %s(%s): %s', user, username, msg)
