FROM python:2.7.14-alpine3.7

RUN pip install celery redis itchat beautifulsoup4 requests

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

