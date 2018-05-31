from redis import StrictRedis
from constants import REDIS_HOST, REDIS_PORT


def get_redis_connection():
    r = StrictRedis(host = REDIS_HOST,
                    port = REDIS_PORT)
    return r


def set_redis_key(key, value, time):
    conn = get_redis_connection()
    conn.set(key, value, ex=time)


def get_redis_key(key):
    conn = get_redis_connection()
    return conn.get(key)
