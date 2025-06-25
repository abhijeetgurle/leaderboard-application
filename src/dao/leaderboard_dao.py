from src.dao.cassandra_dao import CassandraDAO
from src.dao.queries.cassandra_queries import UPDATE_SCORE_FOR_USER
from src.utils.singleton import SingletonMeta


class LeaderboardDAO(metaclass=SingletonMeta):
    def __init__(self):
        self._cassandra_dao = CassandraDAO()

    def update_score(self, score, game_id, user_id):
        query = UPDATE_SCORE_FOR_USER
        self._cassandra_dao.execute_query(query, (score, game_id, user_id))
