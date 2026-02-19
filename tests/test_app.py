"""
Test cases for Mergington High School API endpoints
Testing GET /activities, POST signup, and DELETE unregister
"""


def test_get_activities_returns_all(client):
    """
    Test GET /activities returns all activities with 200 status
    
    Arrange: Client is ready
    Act: GET /activities
    Assert: 200 status, returns dict with 9 activities
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    assert "Soccer Team" in activities
    assert "Basketball Club" in activities
    assert "Art Workshop" in activities
    assert "Drama Club" in activities
    assert "Debate Team" in activities
    assert "Science Club" in activities


def test_get_activities_includes_participants(client):
    """
    Test GET /activities includes participants list for each activity
    
    Arrange: Client is ready
    Act: GET /activities
    Assert: Each activity has participants field with expected data
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    # Verify each activity has required fields including participants
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)
    
    # Verify Chess Club has expected initial participants
    chess_club = activities["Chess Club"]
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_signup_new_participant_success(client):
    """
    Test POST /activities/{activity}/signup with new email returns 200
    
    Arrange: New email not yet registered for Chess Club
    Act: POST signup with newstudent@mergington.edu
    Assert: 200 status, success message, participant added to list
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up" in data["message"]
    assert new_email in data["message"]
    
    # Verify participant was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_email_returns_400(client):
    """
    Test POST /activities/{activity}/signup with duplicate email returns 400
    
    Arrange: michael@mergington.edu already registered for Chess Club
    Act: POST signup with same email
    Assert: 400 status, error message about already signed up
    """
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={duplicate_email}"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client):
    """
    Test POST /activities/{activity}/signup with invalid activity returns 404
    
    Arrange: Activity "Fake Club" doesn't exist
    Act: POST signup for non-existent activity
    Assert: 404 status, error message about activity not found
    """
    # Arrange
    invalid_activity = "Fake Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_existing_participant_success(client):
    """
    Test DELETE /activities/{activity}/unregister removes existing participant
    
    Arrange: michael@mergington.edu is registered for Chess Club
    Act: DELETE unregister
    Assert: 200 status, success message, participant removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    
    # Verify participant exists before removal
    activities_before = client.get("/activities").json()
    assert existing_email in activities_before[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={existing_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Removed" in data["message"]
    assert existing_email in data["message"]
    
    # Verify participant was actually removed
    activities_after = client.get("/activities").json()
    assert existing_email not in activities_after[activity_name]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """
    Test DELETE /activities/{activity}/unregister with invalid activity returns 404
    
    Arrange: Activity "Fake Club" doesn't exist
    Act: DELETE unregister from non-existent activity
    Assert: 404 status, error message about activity not found
    """
    # Arrange
    invalid_activity = "Fake Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_nonexistent_participant_returns_400(client):
    """
    Test DELETE /activities/{activity}/unregister with unregistered email returns 400
    
    Arrange: notregistered@example.com is not in Chess Club
    Act: DELETE unregister for non-existent participant
    Assert: 400 status (matching actual app behavior), error message
    """
    # Arrange
    activity_name = "Chess Club"
    unregistered_email = "notregistered@example.com"
    
    # Verify participant doesn't exist
    activities_before = client.get("/activities").json()
    assert unregistered_email not in activities_before[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={unregistered_email}"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()
