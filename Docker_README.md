# Docker Setup for Video Recommendation System

This project includes Docker configuration to containerize the database-based algorithm learning system.

## Docker Files

- `Dockerfile`: Defines the container image with Python environment and dependencies
- `docker-compose.yml`: Defines services for the application and optional database viewer
- `.dockerignore`: Specifies files to exclude from the Docker image

## Prerequisites

- Docker (version 18.09 or later)
- Docker Compose (version 1.25 or later)

## Building and Running

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### Option 2: Using Docker Commands

```bash
# Build the image
docker build -t video-recommender .

# Run the container
docker run -it video-recommender
```

## Services

1. **video-recommender**: Main application service running the recommendation system
2. **sqlite-web** (optional): Web interface to view the SQLite database (available at http://localhost:8080)

## Volumes

- The database file `video_recommendations.db` is persisted in a named volume
- The current directory is mounted to allow access to the database file

## Environment

- The application runs as a non-root user for security
- Default command runs `main.py` which executes the recommendation system

## Testing the Docker Setup

After starting the services, you can:

1. Check logs: `docker-compose logs -f`
2. Access the database viewer at `http://localhost:8080`
3. Verify the database contains data from the recommendation learning process

## Customization

You can modify the Docker configuration to:

- Change the exposed ports
- Add environment variables
- Mount additional volumes
- Adjust resource limits
