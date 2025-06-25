from cassandra.cluster import Cluster

from src.dao.queries.cassandra_queries import CREATE_LEADERBOARD_KEYSPACE_IF_NOT_EXISTS, CREATE_TABLE_SCORES_IF_NOT_EXISTS
from src.utils.singleton import SingletonMeta


class CassandraDAO(metaclass=SingletonMeta):
    def __init__(self):
        self._url = '127.0.0.1'
        self._cluster = Cluster([self._url])
        self._session = self._cluster.connect()

        self.populate_database()

    def populate_database(self):
        self._session.execute(CREATE_LEADERBOARD_KEYSPACE_IF_NOT_EXISTS)
        self._session.set_keyspace('leaderboard')
        self._session.execute(CREATE_TABLE_SCORES_IF_NOT_EXISTS)

    def get_session(self):
        return self._session

    def execute_query(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        return self._session.execute(query, parameters)