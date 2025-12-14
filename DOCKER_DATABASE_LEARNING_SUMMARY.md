# Docker-Based Database Learning System for Video Recommendations

## Overview

This project implements a comprehensive video recommendation system with database persistence and algorithm learning capabilities, packaged in Docker containers for easy deployment and scaling.

## Components

### 1. Database Algorithm Implementation (`database_algorithm.py`)
- Extends the base recommendation system with database persistence
- Uses SQLite for storing videos, user profiles, watch history, and recommendation logs
- Implements continuous learning from user interactions
- Tracks recommendation effectiveness metrics

### 2. Database Learning Demo (`database_learning_demo.py`)
- Demonstrates the learning capabilities of the system
- Simulates user interactions over time
- Retrains the recommendation model with new data
- Analyzes user behavior patterns and collaborative filtering

### 3. Docker Configuration
- `Dockerfile`: Defines the application container with Python environment
- `docker-compose.yml`: Orchestrates the application and optional database viewer
- `.dockerignore`: Excludes unnecessary files from the Docker image

## Docker Setup

### Prerequisites
- Docker (version 18.09 or later)
- Docker Compose (version 1.25 or later)

### Building and Running

#### Using Docker Compose (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up --build -d
```

#### Using Docker Commands
```bash
# Build the image
docker build -t video-recommender .

# Run the container
docker run -it video-recommender
```

## Database Schema

The system uses SQLite with the following tables:

1. **videos**: Stores video metadata including title, description, tags, and embeddings
2. **user_profiles**: Stores user preferences and profile information
3. **watch_history**: Tracks user video interactions with ratings
4. **liked_videos**: Records user likes for collaborative filtering
5. **recommendation_logs**: Logs recommendations for effectiveness analysis

## Learning Mechanisms

### 1. Content-Based Learning
- Updates video embeddings based on content and user feedback
- Uses TF-IDF vectorization for text-based similarity

### 2. Collaborative Learning
- Analyzes user behavior patterns from watch history
- Identifies similar users for cross-recommendations
- Uses liked videos to refine user profiles

### 3. Effectiveness Tracking
- Monitors click-through rates and average ratings
- Tracks recommendation performance over time
- Provides analytics for system optimization

## Key Features

### Database Persistence
- All data stored in SQLite database for persistence
- Automatic schema creation and management
- Support for complex queries and analytics

### Continuous Learning
- Real-time updates from user interactions
- Model retraining with new data
- Adaptive recommendation algorithms

### Analytics and Monitoring
- Comprehensive effectiveness metrics
- User behavior analysis
- Content popularity tracking

### Scalability
- Containerized architecture for easy scaling
- Database-based design supports large user bases
- Modular components for extensibility

## Testing

The system includes comprehensive testing:

1. **Unit Tests**: Test individual components (`test_database_algorithm.py`)
2. **Integration Tests**: Verify system integration (`integration_test.py`)
3. **Docker Tests**: Validate container functionality (when Docker is available)

## Usage Examples

The system can be used for:
- Personalized video recommendations
- Content discovery platforms
- Learning management systems
- Media streaming services

## Performance Considerations

- SQLite is suitable for small to medium-scale applications
- For larger deployments, consider PostgreSQL or other production databases
- The TF-IDF model is efficient for text-based similarity
- Embedding generation can be optimized for large datasets

## Extending the System

The modular design allows for:
- Adding new recommendation algorithms
- Integrating with different database systems
- Implementing advanced machine learning models
- Adding real-time analytics capabilities

## Files Summary

- `Dockerfile`: Docker image definition
- `docker-compose.yml`: Multi-service orchestration
- `.dockerignore`: Files to exclude from Docker build
- `database_algorithm.py`: Core database implementation
- `database_learning_demo.py`: Learning demonstration
- `test_database_algorithm.py`: Unit tests
- `integration_test.py`: Integration tests
- `Docker_README.md`: Docker usage instructions
- `DOCKER_DATABASE_LEARNING_SUMMARY.md`: This document
