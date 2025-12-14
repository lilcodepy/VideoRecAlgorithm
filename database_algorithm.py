"""
Database-based algorithm learning for the video recommendation system.
This module provides database storage and retrieval capabilities for videos,
user profiles, and recommendation history.
"""

import sqlite3
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from algorithm import LLMVideoRecommender, Video


class DatabaseVideoRecommender(LLMVideoRecommender):
    """
    Extended video recommender with database persistence
    """

    def __init__(self, db_path: str = "video_recommendations.db"):
        super().__init__()
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                tags TEXT,
                category TEXT,
                duration INTEGER,
                upload_date TEXT,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                creator TEXT,
                embedding BLOB
            )
        """)

        # Create user profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                preferences TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)

        # Create watch history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watch_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                video_id TEXT,
                timestamp TEXT,
                rating REAL,
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id),
                FOREIGN KEY (video_id) REFERENCES videos (id)
            )
        """)

        # Create liked videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liked_videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                video_id TEXT,
                timestamp TEXT,
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id),
                FOREIGN KEY (video_id) REFERENCES videos (id)
            )
        """)

        # Create recommendation logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                video_id TEXT,
                recommendation_score REAL,
                timestamp TEXT,
                recommendation_type TEXT,
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id),
                FOREIGN KEY (video_id) REFERENCES videos (id)
            )
        """)

        conn.commit()
        conn.close()

    def add_video_to_db(self, video: Video):
        """Add a video to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Convert tags list to JSON string
        tags_json = json.dumps(video.tags) if video.tags else "[]"

        # Convert embedding to bytes if it exists
        embedding_bytes = None
        if video.embedding is not None:
            embedding_bytes = video.embedding.tobytes()

        cursor.execute("""
            INSERT OR REPLACE INTO videos
            (id, title, description, tags, category, duration, upload_date,
             views, likes, creator, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video.id, video.title, video.description, tags_json,
            video.category, video.duration, video.upload_date,
            video.views, video.likes, video.creator, embedding_bytes
        ))

        conn.commit()
        conn.close()

    def load_videos_from_db(self):
        """Load all videos from the database into memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM videos")
        rows = cursor.fetchall()

        videos = []
        for row in rows:
            # Parse tags from JSON
            tags = json.loads(row[3]) if row[3] else []

            # Load embedding if it exists
            embedding = None
            if row[10] is not None:  # embedding column
                # Convert bytes back to numpy array
                embedding = np.frombuffer(row[10], dtype=np.float64)

            video = Video(
                id=row[0], title=row[1], description=row[2],
                tags=tags, category=row[4], duration=row[5],
                upload_date=row[6], views=row[7], likes=row[8],
                creator=row[9], embedding=embedding
            )
            videos.append(video)

        conn.close()

        # Update the in-memory store
        self.videos = videos

        return videos

    def save_user_profile_to_db(self, user_id: str, preferences: Dict):
        """Save user profile to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        preferences_json = json.dumps(preferences)
        timestamp = datetime.now().isoformat()

        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles
            (user_id, preferences, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, preferences_json, timestamp, timestamp))

        conn.commit()
        conn.close()

    def load_user_profiles_from_db(self):
        """Load all user profiles from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, preferences FROM user_profiles")
        rows = cursor.fetchall()

        for row in rows:
            user_id = row[0]
            preferences = json.loads(row[1]) if row[1] else {}

            # Initialize user profile in memory
            self.user_profiles[user_id] = {
                'preferences': preferences,
                'watch_history': [],
                'liked_videos': [],
                'disliked_videos': []
            }

        # Load watch history for each user
        cursor.execute("""
            SELECT user_id, video_id, timestamp, rating
            FROM watch_history
            ORDER BY timestamp DESC
        """)
        watch_rows = cursor.fetchall()

        for row in watch_rows:
            user_id = row[0]
            if user_id in self.user_profiles:
                self.user_profiles[user_id]['watch_history'].append({
                    'video_id': row[1],
                    'timestamp': pd.Timestamp(row[2]),
                    'rating': row[3]
                })

        # Load liked videos for each user
        cursor.execute("SELECT user_id, video_id, timestamp FROM liked_videos")
        liked_rows = cursor.fetchall()

        for row in liked_rows:
            user_id = row[0]
            video_id = row[1]
            if user_id in self.user_profiles:
                self.user_profiles[user_id]['liked_videos'].append(video_id)

        conn.close()

    def log_recommendation(self, user_id: str, video_id: str, score: float, rec_type: str = "personalized"):
        """Log a recommendation to track effectiveness"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO recommendation_logs
            (user_id, video_id, recommendation_score, timestamp, recommendation_type)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, video_id, score, timestamp, rec_type))

        conn.commit()
        conn.close()

    def get_recommendation_effectiveness(self, user_id: str = None) -> Dict:
        """Analyze the effectiveness of recommendations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get recommendation logs with watch history to analyze click-through rate
        query = """
            SELECT r.user_id, r.video_id, r.recommendation_score, r.timestamp, w.rating
            FROM recommendation_logs r
            LEFT JOIN watch_history w ON r.video_id = w.video_id AND r.user_id = w.user_id
            WHERE r.timestamp >= date('now', '-30 days')
        """

        params = []
        if user_id:
            query += " AND r.user_id = ?"
            params.append(user_id)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        total_recommendations = len(rows)
        clicked_recommendations = sum(1 for row in rows if row[4] is not None)  # Has watch history entry
        avg_rating = sum(row[4] for row in rows if row[4] is not None) / max(1, clicked_recommendations) if clicked_recommendations > 0 else 0

        conn.close()

        return {
            "total_recommendations": total_recommendations,
            "clicked_recommendations": clicked_recommendations,
            "click_through_rate": clicked_recommendations / max(1, total_recommendations),
            "avg_rating": avg_rating
        }

    def update_video_stats(self, video_id: str, views_delta: int = 0, likes_delta: int = 0):
        """Update video statistics in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE videos
            SET views = views + ?, likes = likes + ?
            WHERE id = ?
        """, (views_delta, likes_delta, video_id))

        conn.commit()
        conn.close()

    def add_video(self, video: Video):
        """Override parent method to also add to database"""
        super().add_video(video)
        self.add_video_to_db(video)

    def create_user_profile(self, user_id: str, preferences: Dict):
        """Override parent method to also save to database"""
        super().create_user_profile(user_id, preferences)
        self.save_user_profile_to_db(user_id, preferences)

    def update_user_watch_history(self, user_id: str, video_id: str, rating: float = None):
        """Override parent method to also save to database"""
        super().update_user_watch_history(user_id, video_id, rating)

        # Also add to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO watch_history (user_id, video_id, timestamp, rating)
            VALUES (?, ?, ?, ?)
        """, (user_id, video_id, timestamp, rating))

        conn.commit()
        conn.close()

        # Update video stats
        self.update_video_stats(video_id, views_delta=1)

    def like_video(self, user_id: str, video_id: str):
        """Record that a user liked a video"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO liked_videos (user_id, video_id, timestamp)
            VALUES (?, ?, ?)
        """, (user_id, video_id, timestamp))

        conn.commit()
        conn.close()

        # Update video stats
        self.update_video_stats(video_id, likes_delta=1)

        # Add to user's liked videos in memory
        if user_id in self.user_profiles:
            if video_id not in self.user_profiles[user_id]['liked_videos']:
                self.user_profiles[user_id]['liked_videos'].append(video_id)

    def train_with_db_data(self):
        """Train the recommendation model using historical data from the database"""
        print("Training recommendation model with database data...")

        # Load all data from DB
        self.load_videos_from_db()
        self.load_user_profiles_from_db()

        # Regenerate embeddings based on current data
        self.generate_embeddings()

        print(f"Model trained with {len(self.videos)} videos and {len(self.user_profiles)} user profiles")

    def get_personalized_recommendations_with_feedback(self, user_id: str, n_recommendations: int = 10) -> List[Tuple[Video, float]]:
        """Get recommendations and log them for future analysis"""
        recommendations = self.get_recommendations(user_id, n_recommendations)

        # Log these recommendations
        for video, score in recommendations:
            self.log_recommendation(user_id, video.id, score, "personalized")

        return recommendations


def create_sample_data_in_db():
    """Create sample data in the database"""
    recommender = DatabaseVideoRecommender()

    # Create sample videos
    sample_videos = [
        Video(
            id="vid1",
            title="Python Machine Learning Tutorial",
            description="Learn machine learning with Python from scratch",
            tags=["python", "machine learning", "tutorial", "programming"],
            category="Education",
            duration=1800,
            upload_date="2023-01-15",
            views=150000,
            likes=5000,
            creator="ML Academy"
        ),
        Video(
            id="vid2",
            title="Advanced React Patterns",
            description="Explore advanced React patterns and best practices",
            tags=["react", "javascript", "web development", "frontend"],
            category="Technology",
            duration=2400,
            upload_date="2023-02-20",
            views=95000,
            likes=3200,
            creator="React Masters"
        ),
        Video(
            id="vid3",
            title="Cooking Italian Pasta",
            description="Learn to cook authentic Italian pasta at home",
            tags=["cooking", "italian", "pasta", "food"],
            category="Food",
            duration=900,
            upload_date="2023-03-10",
            views=210000,
            likes=8500,
            creator="Chef Mario"
        ),
        Video(
            id="vid4",
            title="Travel to Japan Guide",
            description="Complete guide to traveling in Japan",
            tags=["travel", "japan", "tourism", "adventure"],
            category="Travel",
            duration=3000,
            upload_date="2023-01-30",
            views=320000,
            likes=12000,
            creator="Wanderlust World"
        ),
        Video(
            id="vid5",
            title="Financial Planning Basics",
            description="Essential financial planning strategies for beginners",
            tags=["finance", "investment", "money", "planning"],
            category="Finance",
            duration=1500,
            upload_date="2023-02-05",
            views=78000,
            likes=2800,
            creator="Money Matters"
        )
    ]

    # Add videos to DB
    for video in sample_videos:
        recommender.add_video_to_db(video)

    # Create user profiles
    user_preferences = {
        "interests": ["python", "machine learning", "programming"],
        "preferred_categories": ["Education", "Technology"],
        "min_duration": 1000,
        "max_duration": 3000
    }

    recommender.save_user_profile_to_db("user123", user_preferences)

    # Add some watch history
    recommender.update_user_watch_history("user123", "vid1", rating=5.0)
    recommender.update_user_watch_history("user123", "vid2", rating=4.0)

    # Like a video
    recommender.like_video("user123", "vid1")

    print("Sample data created in database successfully!")

    return recommender


def demo_database_functionality():
    """Demonstrate the database functionality"""
    print("Initializing database-based recommendation system...")

    # Create recommender with DB
    recommender = DatabaseVideoRecommender()

    # Load data from DB
    recommender.load_videos_from_db()
    recommender.load_user_profiles_from_db()

    if not recommender.videos:
        # Create sample data if DB is empty
        print("No videos found in database. Creating sample data...")
        create_sample_data_in_db()
        recommender.load_videos_from_db()
        recommender.load_user_profiles_from_db()

    print(f"\nLoaded {len(recommender.videos)} videos from database")
    print(f"Loaded {len(recommender.user_profiles)} user profiles from database")

    # Train the model with DB data
    recommender.train_with_db_data()

    # Get recommendations
    recommendations = recommender.get_personalized_recommendations_with_feedback("user123", n_recommendations=3)

    print("\nTop 3 Recommendations for user123:")
    for i, (video, score) in enumerate(recommendations, 1):
        print(f"{i}. {video.title} (Score: {score:.3f})")
        print(f"   Category: {video.category}, Views: {video.views:,}")
        print(f"   Tags: {', '.join(video.tags[:3])}")
        print()

    # Show recommendation effectiveness
    effectiveness = recommender.get_recommendation_effectiveness("user123")
    print("Recommendation Effectiveness Metrics:")
    print(f"  Total Recommendations: {effectiveness['total_recommendations']}")
    print(f"  Click-through Rate: {effectiveness['click_through_rate']:.2%}")
    print(f"  Average Rating: {effectiveness['avg_rating']:.2f}")


if __name__ == "__main__":
    demo_database_functionality()
