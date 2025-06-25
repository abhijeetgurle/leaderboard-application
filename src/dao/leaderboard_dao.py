from src.dao.cassandra_dao import CassandraDAO
from src.dao.queries.cassandra_queries import UPDATE_SCORE_FOR_USER
from src.dao.redis_dao import RedisDao
from src.utils.singleton import SingletonMeta


class LeaderboardDAO(metaclass=SingletonMeta):
    def __init__(self):
        self._cassandra_dao = CassandraDAO()
        self._redis_dao = RedisDao()

    def update_score(self, score, game_id, user_id):
        query = UPDATE_SCORE_FOR_USER
        self._cassandra_dao.execute_query(query, (score, game_id, user_id))

    def get_top_k_scores(self, game_id, k):
        top_users = self._redis_dao.get_top_k(game_id, k)
        return [{"userId": u.decode(), "score": s} for u, s in top_users]

    def get_user_rank(self, game_id, user_id):
        rank = self._redis_dao.get_rank(game_id, user_id)
        return rank

    def increment_user_score(self, game_id, user_id, score):
        return self._redis_dao.increment_by(game_id, score, user_id)

