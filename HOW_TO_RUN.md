# How to Run the Docker-Based Database Learning System

## Prerequisites

- Python 3.7+ (for local execution)
- Docker and Docker Compose (for containerized execution)

## Local Execution

To run the system locally without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main application
python main.py

# Or run the database learning demo
python database_learning_demo.py

# Run unit tests
python -m pytest test_database_algorithm.py

# Run integration tests
python integration_test.py
```

## Docker Execution

To run the system using Docker:

```bash
# Build and run with Docker Compose (recommended)
docker-compose up --build

# Or build and run manually
docker build -t video-recommender .
docker run -it video-recommender
```

## File Structure

```
/workspace/
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Multi-service orchestration
├── .dockerignore             # Files to exclude from Docker
├── main.py                   # Main application entry point
├── database_learning_demo.py # Learning demonstration
├── database_algorithm.py     # Core database implementation
├── algorithm.py              # Base recommendation algorithm
├── test_database_algorithm.py # Unit tests
├── integration_test.py       # Integration tests
├── Docker_README.md          # Docker usage instructions
├── DOCKER_DATABASE_LEARNING_SUMMARY.md # This documentation
├── req.txt / requirements.txt # Python dependencies
├── video_recommendations.db  # SQLite database file
└── ...
```

## Key Features Demonstrated

1. **Database Persistence**: All data stored in SQLite database
2. **Continuous Learning**: System learns from user interactions
3. **Effectiveness Tracking**: Metrics for recommendation performance
4. **User Behavior Analysis**: Pattern recognition and collaborative filtering
5. **Containerization**: Easy deployment with Docker

## Testing the System

The system includes multiple levels of testing:

- **Unit Tests**: Verify individual components (`test_database_algorithm.py`)
- **Integration Tests**: Validate system integration (`integration_test.py`)
- **Functional Tests**: Demonstrate complete workflow (`main.py`, `database_learning_demo.py`)

## Customization Options

You can customize the system by:

1. Modifying the Docker configuration in `docker-compose.yml`
2. Adding new recommendation algorithms in `database_algorithm.py`
3. Extending the database schema for additional features
4. Adjusting the learning parameters and metrics

## Next Steps

1. Run `python main.py` to see the complete system in action
2. Run `docker-compose up --build` to deploy with Docker
3. Review the database at `video_recommendations.db` using any SQLite viewer
4. Examine the test files to understand the implementation details
