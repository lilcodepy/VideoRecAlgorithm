"""
Test script to verify the Docker setup for the video recommendation system
"""
import os
import subprocess
import sys
import time
from pathlib import Path


def test_docker_build():
    """Test if Docker image builds successfully"""
    print("Testing Docker build...")

    try:
        # Build the Docker image
        result = subprocess.run([
            "docker", "build", "-t", "video-recommender-test", "."
        ], capture_output=True, text=True, cwd="/workspace")

        if result.returncode == 0:
            print("✓ Docker image built successfully")
            return True
        else:
            print(f"✗ Docker build failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ Docker is not installed or not in PATH")
        return False


def test_docker_compose_up():
    """Test if Docker Compose services start successfully"""
    print("Testing Docker Compose setup...")

    try:
        # Start services in detached mode
        result = subprocess.run([
            "docker-compose", "up", "-d"
        ], capture_output=True, text=True, cwd="/workspace")

        if result.returncode == 0:
            print("✓ Docker Compose services started successfully")
            return True
        else:
            print(f"✗ Docker Compose failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ Docker Compose is not installed or not in PATH")
        return False


def test_application_run():
    """Test if the application runs correctly inside Docker"""
    print("Testing application functionality inside Docker...")

    try:
        # Run the main application in the container
        result = subprocess.run([
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/app",
            "video-recommender-test",
            "python", "database_learning_demo.py"
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print("✓ Application ran successfully in Docker")
            print(f"Output preview: {result.stdout[:500]}...")
            return True
        else:
            print(f"✗ Application failed in Docker: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Application timed out in Docker")
        return False
    except Exception as e:
        print(f"✗ Error running application in Docker: {e}")
        return False


def test_database_persistence():
    """Test if database persists correctly"""
    print("Testing database persistence...")

    # Check if database file exists
    db_path = Path("/workspace/video_recommendations.db")
    if db_path.exists():
        size = db_path.stat().st_size
        if size > 0:
            print(f"✓ Database exists and has content ({size} bytes)")
            return True
        else:
            print("✗ Database exists but is empty")
            return False
    else:
        print("✗ Database file does not exist")
        return False


def cleanup():
    """Clean up test resources"""
    print("Cleaning up...")

    # Stop Docker Compose services if they're running
    try:
        subprocess.run(["docker-compose", "down"],
                      capture_output=True, text=True, cwd="/workspace")
    except:
        pass

    # Remove test image if it exists
    try:
        subprocess.run(["docker", "rmi", "-f", "video-recommender-test"],
                      capture_output=True, text=True)
    except:
        pass


def main():
    """Run all tests"""
    print("Starting Docker setup tests for Video Recommendation System...\n")

    tests = [
        ("Docker Build", test_docker_build),
        ("Docker Compose", test_docker_compose_up),
        ("Application Run", test_application_run),
        ("Database Persistence", test_database_persistence),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        success = test_func()
        results.append((test_name, success))
        print()

    # Summary
    print("--- Test Summary ---")
    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Docker setup is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the Docker setup.")
        return False


if __name__ == "__main__":
    try:
        success = main()
        cleanup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during tests: {e}")
        cleanup()
        sys.exit(1)
