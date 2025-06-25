import redis

from src.dao.leaderboard_dao import LeaderboardDAO
from src.service.kafka_consumer import KafkaConsumerClient

r = redis.Redis()

class RedisConsumer:
    def __init__(self):
        self.leaderboard_dao = LeaderboardDAO()

    def run(self):
        for msg in KafkaConsumerClient(group_id="redis_consumer").consume():
            print('Message from redis consumer: ', msg)
            data = msg
            key = f"leaderboard:{data['gameId']}"
            print("key: ", key)
            self.leaderboard_dao.increment_user_score(game_id=data['gameId'], user_id=data['userId'], score=data['score'])