import json

from kafka import KafkaProducer


class KafkaProducerClient:
    def __init__(self, producer):
        self.bootstrap_server = 'http://localhost:9092'
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = 'score_updates'

    def send(self, key, value):
        self.producer.send(self.topic, key=key, value=value)