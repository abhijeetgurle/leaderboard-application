from src.dao.leaderboard_dao import LeaderboardDAO
from src.service.kafka_consumer import KafkaConsumerClient


class CassandraConsumer:
    def __init__(self):
        self._leaderboard_dao = LeaderboardDAO()
        self._consumer = KafkaConsumerClient(group_id="cass_consumer")

    def consume(self):
        for message in self._consumer.consume():
            print('Message from cassandra consumer: ', message)
            self._leaderboard_dao.update_score(message['score'], message['gameId'], message['userId'])