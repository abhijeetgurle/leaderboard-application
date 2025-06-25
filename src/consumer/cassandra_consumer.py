from src.dao.leaderboard_dao import LeaderboardDAO
from src.service.kafka_consumer import KafkaConsumerClient
from src.utils.singleton import SingletonMeta


class CassandraConsumer(metaclass=SingletonMeta):
    def __init__(self):
        self._leaderboard_dao = LeaderboardDAO()
        self._consumer = KafkaConsumerClient(group_id="cass_consumer")

    def consume(self):
        for message in self._consumer.consume():
            self._leaderboard_dao.update_score(message['score'], message['gameId'], message['userId'])