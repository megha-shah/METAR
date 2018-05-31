from redis import StrictRedis
from constants import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, CACHE_EXPIRE_TIME

def get_redis_connection():
	try:
		r = StrictRedis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD, decode_responses=True)
		return r
	except Exception as e:
		print(e)

def set_redis_key(key,value,time):
	conn = get_redis_connection()
	conn.set(key, value, ex=time)

def get_redis_key(key):
	conn = get_redis_connection()
	return conn.get(key)
