import json

from kafka import KafkaConsumer


class KafkaConsumerClient:
    def __init__(self, group_id: str):
        self.bootstrap_server = 'localhost:9092'
        self.topic = 'score_updates'
        self.group_id = group_id
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_server,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def consume(self):
        for message in self.consumer:
            print('Message from kafka: ', message)
            yield message.value

