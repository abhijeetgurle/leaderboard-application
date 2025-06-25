# Leaderboard Application

A high-performance, scalable leaderboard system built with Flask, Kafka, Redis, and Cassandra for real-time score tracking and ranking.

## Architecture

This application implements a distributed leaderboard system with the following components:

- **Flask API Server**: REST API for score submission and leaderboard queries
- **Apache Kafka**: Message streaming platform for asynchronous score processing
- **Redis**: In-memory data store for fast leaderboard queries and real-time rankings
- **Apache Cassandra**: Distributed database for persistent score storage
- **Multi-Consumer Architecture**: Separate consumers for Redis and Cassandra data processing

## Features

- 🚀 **High Performance**: Redis-backed leaderboards for sub-millisecond query times
- 📈 **Scalable**: Distributed architecture with Kafka for handling high-volume score updates
- 🔄 **Real-time**: Instant leaderboard updates with asynchronous processing
- 💾 **Persistent**: Cassandra ensures data durability and consistency
- 🎮 **Multi-Game Support**: Handle leaderboards for multiple games simultaneously
- 📊 **Flexible Queries**: Get top-K scores and individual user rankings

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the application.

### Submit Score

```
POST /score
Content-Type: application/json

{
    "userId": "user123",
    "score": 1500,
    "gameId": "game456"
}
```

Submits a score update for a user in a specific game. The score is queued for asynchronous processing.

### Get Top K Scores

```
GET /topk?gameId=game456&k=10
```

Retrieves the top K players for a specific game (default: top 10).

**Response:**

```json
[
    {"userId": "user123", "score": 1500},
    {"userId": "user456", "score": 1400},
    ...
]
```

### Get User Rank

```
GET /rank/{userId}?gameId=game456
```

Gets the current rank of a specific user in a game.

**Response:**

```json
{
  "userId": "user123",
  "rank": 5
}
```

## Prerequisites

- Docker and Docker Compose
- Python 3.8+

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd leaderboard-application
```

### 2. Start Infrastructure Services

```bash
docker-compose up -d
```

This will start:

- Cassandra (port 9042)
- Redis (port 6379)
- Zookeeper (port 2181)
- Kafka (port 9092)

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database Schema

Wait for Cassandra to be fully initialized (usually 30-60 seconds), then set up the required keyspace and tables:

```bash
# Connect to Cassandra and create the schema
docker exec -it cassandra-node1 cqlsh -e "
CREATE KEYSPACE IF NOT EXISTS leaderboard
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE leaderboard;

CREATE TABLE IF NOT EXISTS user_scores (
    game_id text,
    user_id text,
    score int,
    PRIMARY KEY (game_id, user_id)
);
"
```

### 5. Create Kafka Topic

```bash
docker exec kafka kafka-topics --create --topic score_updates --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 6. Run the Application

```bash
python src/app.py
```

The application will start on `http://localhost:5000` with background consumers running.

## Usage Examples

### Submit a Score

```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{"userId": "player1", "score": 2500, "gameId": "tetris"}'
```

### Get Top 5 Players

```bash
curl "http://localhost:5000/topk?gameId=tetris&k=5"
```

### Check Player Rank

```bash
curl "http://localhost:5000/rank/player1?gameId=tetris"
```

## Project Structure

```
leaderboard-application/
├── src/
│   ├── app.py                      # Flask application and API endpoints
│   ├── consumer/
│   │   ├── cassandra_consumer.py   # Cassandra data consumer
│   │   └── redis_consumer.py       # Redis data consumer
│   ├── dao/
│   │   ├── cassandra_dao.py        # Cassandra data access layer
│   │   ├── redis_dao.py            # Redis data access layer
│   │   ├── leaderboard_dao.py      # Main leaderboard data operations
│   │   └── queries/
│   │       └── cassandra_queries.py # CQL query definitions
│   ├── service/
│   │   ├── kafka_consumer.py       # Kafka consumer client
│   │   └── kafka_producer.py       # Kafka producer client
│   └── utils/
│       └── singleton.py            # Singleton pattern implementation
├── docker-compose.yml              # Infrastructure services definition
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Data Flow

1. **Score Submission**: Client submits score via REST API
2. **Message Queue**: Score is published to Kafka topic
3. **Parallel Processing**:
   - Redis Consumer updates leaderboard for fast queries
   - Cassandra Consumer persists data for durability
4. **Query Response**: Leaderboard queries are served from Redis for optimal performance

## Configuration

The application uses default configurations for all services. For production deployments, consider:

- Configuring Cassandra replication factor
- Setting up Kafka with multiple brokers
- Implementing Redis persistence
- Adding authentication and authorization
- Setting up monitoring and logging

## Development

### Running Tests

```bash
# Add your test commands here
pytest tests/
```

### Adding New Games

Simply use a new `gameId` when submitting scores. The system automatically handles multiple games.

## Production Considerations

- **Monitoring**: Implement health checks for all services
- **Security**: Add authentication, rate limiting, and input validation
- **Scaling**: Configure Kafka partitions and Cassandra nodes based on load
- **Backup**: Set up regular backups for Cassandra data
- **Load Balancing**: Use multiple Flask instances behind a load balancer

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license information here]
