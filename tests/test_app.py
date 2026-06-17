"""Test suite for the Mergington High School API endpoints using AAA pattern."""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint."""

    def test_root_redirect_to_static_index(self, test_client):
        """
        Arrange: Create test client
        Act: Send GET request to /
        Assert: Verify redirect response to /static/index.html
        """
        # Arrange
        client = test_client
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, test_client):
        """
        Arrange: Create test client with pre-populated activities
        Act: Send GET request to /activities
        Assert: Verify all activities are returned with correct structure
        """
        # Arrange
        client = test_client
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert data["Chess Club"]["max_participants"] == 12
        assert len(data["Chess Club"]["participants"]) > 0

    def test_get_activities_includes_participant_info(self, test_client):
        """
        Arrange: Create test client
        Act: Send GET request to /activities
        Assert: Verify each activity has required fields including participants list
        """
        # Arrange
        client = test_client
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, test_client, sample_activity):
        """
        Arrange: Create test client and prepare new student email
        Act: Send POST request to signup endpoint
        Assert: Verify student is added to participants list
        """
        # Arrange
        client = test_client
        activity_name = sample_activity["name"]
        email = sample_activity["email"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert f"Signed up {email}" in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email in participants

    def test_signup_missing_email_parameter(self, test_client):
        """
        Arrange: Create test client
        Act: Send POST request without email query parameter
        Assert: Verify request fails with appropriate error
        """
        # Arrange
        client = test_client
        activity_name = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Assert
        assert response.status_code == 422

    def test_signup_nonexistent_activity(self, test_client, sample_activity):
        """
        Arrange: Create test client with non-existent activity name
        Act: Send POST request to signup for invalid activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        client = test_client
        invalid_activity = "Nonexistent Club"
        email = sample_activity["email"]
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_student(self, test_client):
        """
        Arrange: Create test client and use existing participant
        Act: Send POST request to signup with already-enrolled student
        Assert: Verify 400 error is returned
        """
        # Arrange
        client = test_client
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_unregister_successful(self, test_client):
        """
        Arrange: Create test client with existing participant
        Act: Send DELETE request to remove participant
        Assert: Verify participant is removed from activity
        """
        # Arrange
        client = test_client
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert f"Unregistered {email}" in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email not in participants

    def test_unregister_nonexistent_activity(self, test_client):
        """
        Arrange: Create test client with non-existent activity
        Act: Send DELETE request for invalid activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        client = test_client
        invalid_activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_nonexistent_participant(self, test_client):
        """
        Arrange: Create test client with valid activity but non-existent participant
        Act: Send DELETE request for non-enrolled student
        Assert: Verify 404 error is returned
        """
        # Arrange
        client = test_client
        activity_name = "Chess Club"
        non_existent_email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{non_existent_email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_unregister_does_not_affect_other_activities(self, test_client):
        """
        Arrange: Create test client with student in multiple activities
        Act: Send DELETE request to remove from one activity
        Assert: Verify student remains in other activities
        """
        # Arrange
        client = test_client
        email = "sophia@mergington.edu"  # In both Programming Class and Art Workshop
        activity_to_leave = "Programming Class"
        activity_to_remain = "Art Workshop"
        
        # Act
        response = client.delete(
            f"/activities/{activity_to_leave}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify removed from one activity
        activities_response = client.get("/activities")
        participants_left = activities_response.json()[activity_to_leave]["participants"]
        assert email not in participants_left
        
        # Verify still in other activity
        participants_remain = activities_response.json()[activity_to_remain]["participants"]
        assert email in participants_remain
