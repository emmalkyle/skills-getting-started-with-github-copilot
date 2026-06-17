"""Pytest configuration and fixtures for testing the Mergington High School API."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_client():
    """
    Provide a TestClient for making HTTP requests to the FastAPI app.
    Reset activities to a known state before each test to prevent state pollution.
    """
    # Reset activities to initial state
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the school soccer team for drills and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "nina@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Practice tennis skills and compete in friendly matches",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ryan@mergington.edu", "lily@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["sophia@mergington.edu", "isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform scenes, build acting skills, and put on a play",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["luke@mergington.edu", "maya@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science challenges and build experimental projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["julia@mergington.edu", "noah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills in debate",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["oliver@mergington.edu", "rachael@mergington.edu"]
        }
    })
    
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Provide a sample activity for tests."""
    return {
        "name": "Chess Club",
        "email": "newstudent@mergington.edu"
    }
