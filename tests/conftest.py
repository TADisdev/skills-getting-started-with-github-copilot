"""
Pytest fixtures for API testing
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """Create a TestClient for making API requests"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically reset the activities dictionary before each test
    to ensure test isolation and prevent tests from affecting each other
    """
    # Store the original state
    original_activities = copy.deepcopy(activities)
    
    # Yield control to the test
    yield
    
    # Restore the original state after the test
    activities.clear()
    activities.update(original_activities)
