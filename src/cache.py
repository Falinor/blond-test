from redis import StrictRedis
from redis_cache import RedisCache

client = StrictRedis(host="redis", decode_responses=True)
cache = RedisCache(redis_client=client)
