"""
Unit tests for the database algorithm implementation
"""
import unittest
import tempfile
import os
from database_algorithm import DatabaseVideoRecommender
from algorithm import Video


class TestVideoRecommendationSystemDB(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()

        self.system = DatabaseVideoRecommender(db_path=self.temp_db.name)

        # Create sample data
        self.video1 = Video(
            id="1",
            title="Python Tutorial",
            description="Learn Python programming",
            tags=["python", "programming", "tutorial"],
            category="Education",
            duration=300,
            upload_date="2023-01-01",
            views=0,
            likes=0,
            creator="CodeAcademy"
        )

        self.video2 = Video(
            id="2",
            title="Machine Learning Basics",
            description="Introduction to ML concepts",
            tags=["machine learning", "ai", "tutorial"],
            category="Education",
            duration=600,
            upload_date="2023-01-02",
            views=0,
            likes=0,
            creator="ML Academy"
        )

    def tearDown(self):
        # Clean up temporary database file
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_add_video_to_db(self):
        """Test adding a video to the database"""
        self.system.add_video(self.video1)
        # Reload videos from database to check if it was saved
        self.system.load_videos_from_db()

        videos = self.system.videos
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0].title, "Python Tutorial")

    def test_add_user_to_db(self):
        """Test adding a user to the database"""
        self.system.create_user_profile("test_user", {"education": 0.8, "technology": 0.6})
        # Reload user profiles from database to check if it was saved
        self.system.load_user_profiles_from_db()

        self.assertIn("test_user", self.system.user_profiles)
        self.assertEqual(self.system.user_profiles["test_user"]["preferences"]["education"], 0.8)

    def test_save_rating(self):
        """Test saving a rating to the database"""
        self.system.add_video(self.video1)
        self.system.create_user_profile("test_user", {"education": 0.8, "technology": 0.6})

        # Save a rating via watch history
        self.system.update_user_watch_history("test_user", "1", rating=4.5)

        # Check that the rating was saved by reloading
        self.system.load_user_profiles_from_db()

        # Check if the rating exists in the user's watch history
        watch_history = self.system.user_profiles["test_user"]["watch_history"]
        self.assertEqual(len(watch_history), 1)
        self.assertEqual(watch_history[0]["rating"], 4.5)

    def test_get_user_recommendations(self):
        """Test getting recommendations for a user"""
        self.system.add_video(self.video1)
        self.system.add_video(self.video2)
        self.system.create_user_profile("test_user", {"education": 0.8, "technology": 0.6})

        # Generate embeddings to enable recommendations
        self.system.generate_embeddings()

        # Get initial recommendations
        recommendations = self.system.get_recommendations("test_user", n_recommendations=5)

        # Should get some recommendations even without ratings
        self.assertIsNotNone(recommendations)
        self.assertIsInstance(recommendations, list)

    def test_update_user_profile(self):
        """Test updating user profile in database"""
        self.system.create_user_profile("test_user", {"education": 0.8, "technology": 0.6})

        # Update user preferences by creating profile again
        new_preferences = {"education": 0.9, "technology": 0.7, "science": 0.5}
        self.system.create_user_profile("test_user", new_preferences)

        # Reload to verify changes
        self.system.load_user_profiles_from_db()

        updated_prefs = self.system.user_profiles["test_user"]["preferences"]
        self.assertEqual(updated_prefs['education'], 0.9)
        self.assertEqual(updated_prefs['science'], 0.5)

    def test_save_interaction(self):
        """Test saving user interaction"""
        self.system.add_video(self.video1)
        self.system.create_user_profile("test_user", {"education": 0.8, "technology": 0.6})

        # Save an interaction via watch history
        self.system.update_user_watch_history("test_user", "1", rating=4.0)

        # Check that the interaction was saved by reloading
        self.system.load_user_profiles_from_db()

        # Check if the interaction exists in the user's watch history
        watch_history = self.system.user_profiles["test_user"]["watch_history"]
        self.assertEqual(len(watch_history), 1)
        self.assertEqual(watch_history[0]["rating"], 4.0)

    def test_effectiveness_tracking(self):
        """Test effectiveness tracking methods"""
        # Initially should have no tracked metrics
        effectiveness = self.system.get_recommendation_effectiveness()

        # These should return valid values
        self.assertIn("total_recommendations", effectiveness)
        self.assertIn("clicked_recommendations", effectiveness)
        self.assertIn("click_through_rate", effectiveness)
        self.assertIn("avg_rating", effectiveness)

        # Initially all values should be 0 or 0.0
        self.assertEqual(effectiveness["total_recommendations"], 0)
        self.assertEqual(effectiveness["clicked_recommendations"], 0)
        self.assertEqual(effectiveness["click_through_rate"], 0)


def run_tests():
    """Function to run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
