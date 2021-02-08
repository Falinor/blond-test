from json import JSONEncoder
from typing import Any

from redis import StrictRedis
from redis_cache import RedisCache


class Encoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        encode = getattr(o, "encode", None)
        if callable(encode):
            return o.encode()
        return o.__dict__


client = StrictRedis(host="localhost", decode_responses=True)
cache = RedisCache(redis_client=client, serializer=Encoder().encode)
