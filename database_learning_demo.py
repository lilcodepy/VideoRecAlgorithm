"""
Database-based algorithm learning demonstration.
This script shows how to use database-stored user interactions to improve
recommendation algorithms over time.
"""

import sqlite3
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from algorithm import LLMVideoRecommender, Video
from database_algorithm import DatabaseVideoRecommender


def simulate_user_interactions():
    """Simulate user interactions over time to demonstrate learning from database"""
    print("Starting database-based algorithm learning demonstration...")

    # Initialize the database recommender
    recommender = DatabaseVideoRecommender()

    # Create a more diverse set of sample videos
    sample_videos = [
        Video(
            id="ml1",
            title="Introduction to Machine Learning",
            description="Beginner's guide to machine learning concepts",
            tags=["machine learning", "ai", "beginner", "tutorial"],
            category="Education",
            duration=1800,
            upload_date="2023-01-15",
            views=150000,
            likes=5000,
            creator="AI Academy"
        ),
        Video(
            id="ml2",
            title="Deep Learning with TensorFlow",
            description="Advanced deep learning techniques using TensorFlow",
            tags=["deep learning", "tensorflow", "neural networks", "advanced"],
            category="Education",
            duration=2700,
            upload_date="2023-02-20",
            views=95000,
            likes=3200,
            creator="AI Academy"
        ),
        Video(
            id="py1",
            title="Python for Data Science",
            description="Using Python for data analysis and visualization",
            tags=["python", "data science", "pandas", "matplotlib"],
            category="Education",
            duration=2400,
            upload_date="2023-03-10",
            views=210000,
            likes=8500,
            creator="Data University"
        ),
        Video(
            id="web1",
            title="Building Modern Web Applications",
            description="Creating responsive web apps with modern frameworks",
            tags=["web development", "javascript", "react", "frontend"],
            category="Technology",
            duration=3000,
            upload_date="2023-01-30",
            views=320000,
            likes=12000,
            creator="Web Masters"
        ),
        Video(
            id="mob1",
            title="Mobile App Development Guide",
            description="Developing cross-platform mobile applications",
            tags=["mobile", "flutter", "ios", "android"],
            category="Technology",
            duration=2200,
            upload_date="2023-02-05",
            views=78000,
            likes=2800,
            creator="App Developers"
        ),
        Video(
            id="ds1",
            title="Data Structures and Algorithms",
            description="Understanding core computer science concepts",
            tags=["algorithms", "data structures", "computer science", "coding"],
            category="Education",
            duration=3600,
            upload_date="2023-03-01",
            views=180000,
            likes=7500,
            creator="CS University"
        ),
        Video(
            id="devops1",
            title="DevOps Essentials",
            description="Introduction to DevOps practices and tools",
            tags=["devops", "docker", "kubernetes", "ci/cd"],
            category="Technology",
            duration=2000,
            upload_date="2023-01-20",
            views=110000,
            likes=4200,
            creator="DevOps Pro"
        )
    ]

    # Add videos to database
    for video in sample_videos:
        recommender.add_video_to_db(video)

    print(f"Added {len(sample_videos)} videos to database")

    # Create user profiles with different interests
    users = {
        "data_scientist": {
            "interests": ["python", "data science", "machine learning"],
            "preferred_categories": ["Education", "Technology"],
            "experience_level": "intermediate"
        },
        "web_dev": {
            "interests": ["javascript", "react", "web development"],
            "preferred_categories": ["Technology"],
            "experience_level": "advanced"
        },
        "student": {
            "interests": ["algorithms", "computer science", "beginner tutorials"],
            "preferred_categories": ["Education"],
            "experience_level": "beginner"
        }
    }

    # Add users to database
    for user_id, preferences in users.items():
        recommender.save_user_profile_to_db(user_id, preferences)

    print(f"Added {len(users)} user profiles to database")

    # Simulate user interactions over time
    print("\nSimulating user interactions over time...")

    # User 1: Data scientist interactions
    interactions = [
        ("data_scientist", "py1", 5.0),  # Python for Data Science - highly rated
        ("data_scientist", "ml1", 4.5),  # Introduction to ML - good rating
        ("data_scientist", "ds1", 3.0),  # Data Structures - ok but not great
        ("data_scientist", "web1", 2.0),  # Web dev - not interested
        ("data_scientist", "ml2", 5.0),  # Deep Learning - excellent
    ]

    for user_id, video_id, rating in interactions:
        recommender.update_user_watch_history(user_id, video_id, rating)
        if rating >= 4.0:
            recommender.like_video(user_id, video_id)

    # User 2: Web developer interactions
    interactions = [
        ("web_dev", "web1", 5.0),      # Building Modern Web Apps - perfect
        ("web_dev", "devops1", 4.0),   # DevOps Essentials - good
        ("web_dev", "mob1", 2.5),      # Mobile App Dev - not really interested
        ("web_dev", "py1", 3.5),       # Python for Data Science - somewhat useful
    ]

    for user_id, video_id, rating in interactions:
        recommender.update_user_watch_history(user_id, video_id, rating)
        if rating >= 4.0:
            recommender.like_video(user_id, video_id)

    # User 3: Student interactions
    interactions = [
        ("student", "ml1", 4.8),    # Introduction to ML - loved it
        ("student", "ds1", 4.5),    # Data Structures - very helpful
        ("student", "ml2", 2.0),    # Deep Learning - too advanced
        ("student", "py1", 4.0),    # Python for Data Science - good level
    ]

    for user_id, video_id, rating in interactions:
        recommender.update_user_watch_history(user_id, video_id, rating)
        if rating >= 4.0:
            recommender.like_video(user_id, video_id)

    print(f"Simulated {len(interactions)} user interactions")

    # Reload data to include new interactions
    recommender.load_videos_from_db()
    recommender.load_user_profiles_from_db()

    # Retrain the model with the new interaction data
    print("\nRetraining recommendation model with new interaction data...")
    recommender.train_with_db_data()

    # Get recommendations for each user
    print("\n=== RECOMMENDATIONS AFTER LEARNING FROM INTERACTIONS ===")

    for user_id in users.keys():
        print(f"\nRecommendations for {user_id}:")

        # Get personalized recommendations
        recommendations = recommender.get_personalized_recommendations_with_feedback(user_id, n_recommendations=3)

        for i, (video, score) in enumerate(recommendations, 1):
            print(f"  {i}. {video.title} (Score: {score:.3f})")
            print(f"     Category: {video.category}, Views: {video.views:,}")
            print(f"     Tags: {', '.join(video.tags[:3])}")

        # Analyze effectiveness for this user
        effectiveness = recommender.get_recommendation_effectiveness(user_id)
        print(f"  Effectiveness for {user_id}:")
        print(f"    Total Recommendations: {effectiveness['total_recommendations']}")
        print(f"    Click-through Rate: {effectiveness['click_through_rate']:.2%}")
        print(f"    Average Rating: {effectiveness['avg_rating']:.2f}")

    # Show database analytics
    print("\n=== DATABASE ANALYTICS ===")
    overall_effectiveness = recommender.get_recommendation_effectiveness()
    print(f"Overall System Performance:")
    print(f"  Total Recommendations: {overall_effectiveness['total_recommendations']}")
    print(f"  Overall Click-through Rate: {overall_effectiveness['click_through_rate']:.2%}")
    print(f"  Average Rating: {overall_effectiveness['avg_rating']:.2f}")

    # Show popular videos based on database metrics
    conn = sqlite3.connect(recommender.db_path)
    cursor = conn.cursor()

    # Get top videos by views
    cursor.execute("SELECT title, views, likes FROM videos ORDER BY views DESC LIMIT 3")
    top_videos = cursor.fetchall()
    print(f"\nTop Videos by Views:")
    for i, (title, views, likes) in enumerate(top_videos, 1):
        print(f"  {i}. {title} (Views: {views:,}, Likes: {likes:,})")

    # Get most interacted videos (based on watch history)
    cursor.execute("""
        SELECT v.title, COUNT(w.video_id) as watch_count
        FROM videos v
        LEFT JOIN watch_history w ON v.id = w.video_id
        GROUP BY v.id, v.title
        ORDER BY watch_count DESC
        LIMIT 3
    """)
    popular_videos = cursor.fetchall()
    print(f"\nMost Watched Videos:")
    for i, (title, count) in enumerate(popular_videos, 1):
        print(f"  {i}. {title} (Watched {count} times)")

    conn.close()

    print("\nDatabase-based algorithm learning demonstration completed!")


def analyze_user_behavior_patterns():
    """Analyze user behavior patterns stored in the database to improve recommendations"""
    recommender = DatabaseVideoRecommender()

    conn = sqlite3.connect(recommender.db_path)
    cursor = conn.cursor()

    print("\n=== USER BEHAVIOR ANALYSIS ===")

    # Find users with similar preferences based on their interactions
    cursor.execute("""
        SELECT user_id, video_id, rating
        FROM watch_history
        WHERE rating IS NOT NULL
        ORDER BY user_id, rating DESC
    """)
    user_ratings = cursor.fetchall()

    # Group ratings by user
    user_video_preferences = {}
    for user_id, video_id, rating in user_ratings:
        if user_id not in user_video_preferences:
            user_video_preferences[user_id] = []
        user_video_preferences[user_id].append((video_id, rating))

    # Find users with overlapping preferences
    user_ids = list(user_video_preferences.keys())
    similar_users = {}

    for i, user1 in enumerate(user_ids):
        for user2 in user_ids[i+1:]:
            # Calculate overlap in watched videos
            videos1 = set([vid for vid, _ in user_video_preferences[user1]])
            videos2 = set([vid for vid, _ in user_video_preferences[user2]])

            common_videos = videos1.intersection(videos2)
            if len(common_videos) > 0:
                print(f"Users {user1} and {user2} share {len(common_videos)} common videos")

                # Find videos that user1 liked but user2 hasn't seen
                user1_high_rated = [vid for vid, rating in user_video_preferences[user1] if rating >= 4.0]
                user2_seen = [vid for vid, _ in user_video_preferences[user2]]

                potential_recommendations = [vid for vid in user1_high_rated if vid not in user2_seen]

                if potential_recommendations:
                    print(f"  Potential recommendations from {user1} to {user2}: {potential_recommendations[:2]}")

    conn.close()


if __name__ == "__main__":
    simulate_user_interactions()
    analyze_user_behavior_patterns()
