from redis import Redis


class RedisCache:
    def __init__(self):
        self.r = Redis()

    def get(self, key: str):
        val = self.r.get(key)
        # self.r.delete(key)
        return val

    def set(self, key: str, val):
        self.r.set(key, val)


class MemoryCache:
    def __init__(self):
        self.map = {}

    def get(self, key: str):
        val = self.map.get(key)
        # self.map.delete(key)
        return val

    def set(self, key: str, val):
        self.map[key] = val
