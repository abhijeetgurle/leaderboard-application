import redis

from src.service.kafka_consumer import KafkaConsumerClient

r = redis.Redis()

class RedisConsumer:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def run(self):
        for msg in KafkaConsumerClient(group_id="redis_consumer").consume():
            data = msg
            key = f"leaderboard:{data['gameId']}"
            self.redis_client.zincrby(key, data['score'], data['userId'])