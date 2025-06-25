CREATE_LEADERBOARD_KEYSPACE_IF_NOT_EXISTS = '''
CREATE KEYSPACE IF NOT EXISTS leaderboard
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
'''

CREATE_TABLE_SCORES_IF_NOT_EXISTS = '''
CREATE TABLE IF NOT EXISTS scores (
    user_id text,
    game_id text,
    score counter,
    PRIMARY KEY ((game_id), user_id)
)
'''

UPDATE_SCORE_FOR_USER = '''
UPDATE scores SET score = score + %s WHERE game_id = %s AND user_id = %s
'''