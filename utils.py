import functools
import hashlib
import redis

from celeryconfig import redis_host, redis_port, store_db


def page_hash(content):
    m = hashlib.md5()
    m.update(content)

    return m.hexdigest()


def get_redis_cli():
    return redis.StrictRedis(host=redis_host, port=redis_port, db=store_db)


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


__CACHED__ = {}


def cached(func):
    global __CACHED__

    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = (func.func_name, args)

        if key not in __CACHED__:
            __CACHED__[key] = func(*args, **kwargs)

        return __CACHED__[key]

    return inner
