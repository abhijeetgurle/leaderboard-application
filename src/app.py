from flask import Flask, jsonify, request

from src.consumer.cassandra_consumer import CassandraConsumer
from src.consumer.redis_consumer import RedisConsumer
from src.service.kafka_producer import KafkaProducerClient

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/score', methods=['POST'])
def submit_score():
    data = request.get_json()
    required = {'userId', 'score', 'gameId'}
    if not required.issubset(data):
        return jsonify({'error': 'Missing fields'}), 400

    KafkaProducerClient().send('score_updates', data)
    return jsonify({'status': 'queued'})


if __name__ == '__main__':
    redis_consumer = RedisConsumer()
    cassandra_consumer = CassandraConsumer()
    app.run(debug=True)