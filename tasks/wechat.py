import itchat

from app import app
from celeryconfig import receive_user


@app.task(name='wechat.send_msg',  rate_limit='1/s')
def send_msg(msg):
    for user in receive_user:
        itchat.send(msg, toUserName=user)
