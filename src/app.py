import threading

from flask import Flask, jsonify, request

from src.consumer.cassandra_consumer import CassandraConsumer
from src.consumer.redis_consumer import RedisConsumer
from src.dao.leaderboard_dao import LeaderboardDAO
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

@app.route('/topk', methods=['GET'])
def top_k():
    game_id = request.args.get('gameId')
    k = request.args.get('k', default=10, type=int)
    if not game_id:
        return jsonify({'error': 'gameId is required'}), 400

    res = LeaderboardDAO().get_top_k_scores(game_id, k)
    return jsonify(res)

@app.route('/rank/<user_id>', methods=['GET'])
def get_rank(user_id):
    game_id = request.args.get('gameId')
    if not game_id:
        return jsonify({'error': 'gameId is required'}), 400
    rank = LeaderboardDAO().get_user_rank(game_id, user_id)
    if rank is None:
        return jsonify({'error': 'user not found'}), 404
    return jsonify({'userId': user_id, 'rank': rank + 1})


if __name__ == '__main__':
    redis_consumer = RedisConsumer()
    cassandra_consumer = CassandraConsumer()

    threading.Thread(target=redis_consumer.run, daemon=True).start()
    threading.Thread(target=cassandra_consumer.consume, daemon=True).start()
    app.run(debug=True)