from app import app
import itchat
from celeryconfig import receive_user


@app.task(name='wechat.send_msg')
def send_msg(msg):
    itchat.send(msg, toUserName=receive_user)
