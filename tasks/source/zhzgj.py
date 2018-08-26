from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
import requests
from urlparse import urljoin


from app import app
from tasks.wechat import send_msg
from utils import look_same, is_exists

url = 'http://www.zhzgj.gov.cn/zwfw/ywgs/kzxxxgh_50440/'
logger = get_task_logger(__name__)


@app.task(name='source.zhzgj')
def run():
    resp = requests.get(url)
    logger.debug('request %s [%d] %s', url, resp.status_code, resp.content)

    if resp.status_code != 200:
        logger.info('pull content error: url=%s, status_code=%s, resp=%s' % (url, resp.status_code, resp.content))
        return

    if look_same(url, resp.content):
        logger.info('page duplicated: url=%s' % url)
        return

    try:
        soup = BeautifulSoup(resp.content, 'html.parser')
        area = soup.find(id='container').find_all(class_='con_right')[0].find_all('ul')[0]
    except KeyError as e:
        logger.warn('parse document error: %s, html=%s' % e, resp.content)
        return

    for li in area.find_all('li'):
        href = urljoin(url, li.a.get('href'))
        title = li.a.get('title')

        if is_exists(url, title):
            continue

        msg = '%s\n%s' % (title, href)
        send_msg(msg)

        logger.info('send msg to receiver: %s', msg)
