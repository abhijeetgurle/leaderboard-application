import json

from kafka import KafkaConsumer

from src.utils.singleton import SingletonMeta


class KafkaConsumerClient(metaclass=SingletonMeta):
    def __init__(self):
        self.bootstrap_server = 'localhost:9092'
        self.topic = 'score_updates'
        self.group_id = 'cass-updater'
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_server,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def consume(self):
        for message in self.consumer:
            yield message.value

