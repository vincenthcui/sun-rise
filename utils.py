import hashlib
import re
import redis

from celeryconfig import store_url


def parse_redis_params(url):
    pattern = r'redis://([0-9.]+|localhost):(\d+)/(\d+)'
    return re.search(pattern, url).groups()


def page_hash(content):
    m = hashlib.md5()
    m.update(content)

    return m.hexdigest()


def get_redis_cli():
    host, port, db = parse_redis_params(store_url)
    return redis.StrictRedis(host=host, port=port, db=db)


def look_same(key, value):
    client = get_redis_cli()
    key = 'duplicate:%s' % key

    old = client.get(key)
    new = page_hash(value)

    if old != new:
        client.set(key, new)

    return old == new


def is_exists(key, value):
    client = get_redis_cli()
    key = 'exist:%s' % key

    exists = client.lrange(key, 0, -1)
    exists = [x.decode('utf8') for x in exists]

    if value not in exists:
        client.rpush(key, value)
        client.ltrim(key, 0, 100)

    return value in exists
