"""Unit tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "HelloFace" in response.json()["message"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "models_loaded" in data


def test_get_stats():
    """Test stats endpoint."""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "recognition_threshold" in data


def test_get_users():
    """Test get users endpoint."""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "total" in data


# Note: Full enrollment and recognition tests require actual images
# These would be integration tests with test images
