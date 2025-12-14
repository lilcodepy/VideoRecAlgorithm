"""
Main entry point for the database-based video recommendation system.
This script demonstrates the complete database-driven algorithm learning approach.
"""

from database_algorithm import DatabaseVideoRecommender
from database_learning_demo import simulate_user_interactions, analyze_user_behavior_patterns
from algorithm import Video


def main():
    print("=== Database-Based Algorithm Learning for Video Recommendations ===\n")

    # Initialize the database-based recommender
    recommender = DatabaseVideoRecommender()

    print("1. Database-based recommender initialized successfully")
    print(f"   Database path: {recommender.db_path}")

    # Show basic functionality
    print("\n2. Demonstrating basic database operations...")

    # Add a sample video to the database
    sample_video = Video(
        id="demo_video",
        title="Database Learning Introduction",
        description="An introduction to database-based algorithm learning",
        tags=["database", "machine learning", "recommendations", "python"],
        category="Education",
        duration=1200,
        upload_date="2023-05-15",
        views=0,
        likes=0,
        creator="AI Research Team"
    )

    recommender.add_video(sample_video)
    print(f"   Added video: {sample_video.title}")

    # Create a user profile
    user_preferences = {
        "interests": ["database", "machine learning", "recommendations"],
        "preferred_categories": ["Education", "Technology"],
        "min_duration": 600,
        "max_duration": 3000
    }

    recommender.create_user_profile("demo_user", user_preferences)
    print(f"   Created user profile: demo_user")

    # Simulate user interaction
    recommender.update_user_watch_history("demo_user", "demo_video", rating=4.5)
    recommender.like_video("demo_user", "demo_video")
    print(f"   Recorded user interaction: demo_user watched and liked demo_video")

    # Get recommendations
    recommendations = recommender.get_personalized_recommendations_with_feedback("demo_user", n_recommendations=1)
    print(f"   Generated recommendation for demo_user")

    # Show recommendation effectiveness
    effectiveness = recommender.get_recommendation_effectiveness("demo_user")
    print(f"   User effectiveness metrics: CTR={effectiveness['click_through_rate']:.2%}, Avg Rating={effectiveness['avg_rating']:.2f}")

    # Run the full simulation
    print("\n3. Running comprehensive database learning simulation...")
    simulate_user_interactions()

    print("\n4. Analyzing user behavior patterns...")
    analyze_user_behavior_patterns()

    print("\n=== Database-Based Algorithm Learning Complete ===")
    print("\nKey Features Demonstrated:")
    print("• Persistent storage of videos, user profiles, and interactions")
    print("• Continuous learning from user feedback")
    print("• Recommendation effectiveness tracking")
    print("• User behavior analysis and pattern recognition")
    print("• Collaborative filtering based on historical data")


if __name__ == "__main__":
    main()
