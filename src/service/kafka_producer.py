import json

from kafka import KafkaProducer

from src.utils.singleton import SingletonMeta


class KafkaProducerClient(metaclass=SingletonMeta):
    def __init__(self):
        self._bootstrap_server = 'localhost:9092'
        self._producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = 'score_updates'

    def send(self, key, value):
        key_bytes = key.encode('utf-8') if isinstance(key, str) else key
        self._producer.send(self.topic, key=key_bytes, value=value)