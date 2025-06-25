import redis

from src.utils.singleton import SingletonMeta


class RedisDao(metaclass=SingletonMeta):
    def __init__(self):
        self._redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def set_key(self, key, value):
        self._redis_client.set(key, value)

    def get_key(self, key):
        return self._redis_client.get(key)

    def get_top_k(self, key, k):
        return self._redis_client.zrevrange(key, 0, k - 1, withscores=True)

    def get_rank(self, key, entity):
        return self._redis_client.zrevrank(key, entity)

    def increment_by(self, key, score, entity):
        return self._redis_client.zincrby(key, score, entity)