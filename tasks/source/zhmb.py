from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
import re
import requests


from app import app
from tasks.wechat import send_msg
from utils import look_same, is_recent

url = 'http://zhmb.gov.cn/jeecms/web/index'
logger = get_task_logger(__name__)
drop_pattern = r'jsessionid=[0-9A-Z]{32}'


@app.task(name='source.zhmb')
def run():
    resp = requests.get(url)
    logger.debug('request %s [%d] %s', url, resp.status_code, resp.content)

    if resp.status_code != 200:
        logger.info('pull content error: url=%s, status_code=%s, resp=%s' % (url, resp.status_code, resp.content))
        return

    try:
        soup = BeautifulSoup(resp.content, 'html.parser')
        area = soup.find(id='con_yu_1').table
    except KeyError as e:
        logger.warn('parse document error: %s, html=%s' % e, resp.content)
        return

    # guard = re.sub(drop_pattern, '', str(area))
    # if look_same(url, guard):
    #     logger.info('page duplicated: url=%s' % url)
    #     return

    for tr in area.find_all('tr'):
        msg = tr.td.p.strong.string.strip()

        if not is_recent(url, msg.encode('utf8'), expire=300):
            msg = "%s\n%s" % (tr.td.p.strong.string.strip(), url)
            send_msg(msg)
        else:
            logger.info('skip sent msg: %s', msg)
