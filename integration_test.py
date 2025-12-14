"""
Integration test for the Docker-based database learning system
"""
import os
import sqlite3
import sys
from database_algorithm import DatabaseVideoRecommender
from algorithm import Video, create_sample_data


def test_database_integration():
    """Test that the database and algorithm integration works properly"""
    print("Testing database and algorithm integration...")

    # Create a test database
    test_db_path = "test_integration.db"

    try:
        # Initialize recommender with test database
        recommender = DatabaseVideoRecommender(db_path=test_db_path)

        # Add sample videos
        sample_videos = create_sample_data()
        for video in sample_videos:
            recommender.add_video(video)

        # Create user profiles
        user_preferences = {
            "interests": ["python", "machine learning", "programming"],
            "preferred_categories": ["Education", "Technology"],
            "min_duration": 1000,
            "max_duration": 3000
        }

        recommender.create_user_profile("test_user", user_preferences)

        # Generate embeddings
        recommender.generate_embeddings()

        # Test recommendations
        recommendations = recommender.get_recommendations("test_user", n_recommendations=3)

        print(f"✓ Generated {len(recommendations)} recommendations")
        assert len(recommendations) <= 3, "Should have at most 3 recommendations"

        # Test that data is saved to database
        recommender.load_videos_from_db()
        videos_in_db = recommender.videos
        print(f"✓ Loaded {len(videos_in_db)} videos from database")
        assert len(videos_in_db) == len(sample_videos), "All videos should be in database"

        # Test user profile saved to database
        recommender.load_user_profiles_from_db()
        assert "test_user" in recommender.user_profiles, "User profile should be in database"

        # Test interaction recording
        if videos_in_db:
            first_video_id = videos_in_db[0].id
            recommender.update_user_watch_history("test_user", first_video_id, rating=4.5)
            recommender.like_video("test_user", first_video_id)

            # Reload to check if interaction was saved
            recommender.load_user_profiles_from_db()
            user_data = recommender.user_profiles["test_user"]
            assert len(user_data["watch_history"]) >= 1, "Watch history should contain at least one item"
            assert first_video_id in user_data["liked_videos"], "Liked video should be recorded"

        # Test effectiveness tracking
        effectiveness = recommender.get_recommendation_effectiveness()
        print(f"✓ Effectiveness metrics: {effectiveness}")

        print("✓ All integration tests passed!")
        return True

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False
    finally:
        # Clean up test database
        if os.path.exists(test_db_path):
            os.remove(test_db_path)


def test_database_file_exists():
    """Test that the main database file exists and is valid"""
    print("Testing main database file...")

    if not os.path.exists("video_recommendations.db"):
        print("✗ Main database file does not exist")
        return False

    try:
        conn = sqlite3.connect("video_recommendations.db")
        cursor = conn.cursor()

        # Check if required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        required_tables = ['videos', 'user_profiles', 'watch_history', 'liked_videos', 'recommendation_logs']
        missing_tables = [table for table in required_tables if table not in tables]

        if missing_tables:
            print(f"✗ Missing tables: {missing_tables}")
            return False

        print(f"✓ Database contains all required tables: {tables}")

        # Check some data counts
        cursor.execute("SELECT COUNT(*) FROM videos;")
        video_count = cursor.fetchone()[0]
        print(f"✓ Database contains {video_count} videos")

        cursor.execute("SELECT COUNT(*) FROM user_profiles;")
        user_count = cursor.fetchone()[0]
        print(f"✓ Database contains {user_count} user profiles")

        conn.close()
        print("✓ Database integrity check passed!")
        return True

    except Exception as e:
        print(f"✗ Database integrity check failed: {e}")
        return False


def main():
    """Run all integration tests"""
    print("Running integration tests for Docker-based database learning system...\n")

    tests = [
        ("Database Integration", test_database_integration),
        ("Database File Check", test_database_file_exists),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        success = test_func()
        results.append((test_name, success))
        print()

    # Summary
    print("--- Integration Test Summary ---")
    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} integration tests passed")

    if passed == total:
        print("🎉 All integration tests passed! Docker setup is ready.")
        return True
    else:
        print("❌ Some integration tests failed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
