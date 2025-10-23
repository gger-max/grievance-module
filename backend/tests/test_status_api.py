import pytest
import os
from datetime import datetime


def test_status_update_without_auth(client):
    """Test that status update fails without authentication"""
    # Create a grievance first
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Try to update without auth
    status_payload = {
        "status": "Acknowledged",
        "note": "Test note"
    }
    
    response = client.put(f"/api/status/{grievance_id}/status", json=status_payload)
    assert response.status_code == 401
    assert "Bearer token" in response.json()["detail"]


def test_status_update_with_invalid_token(client):
    """Test that status update fails with invalid token"""
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Try to update with invalid token
    status_payload = {
        "status": "Acknowledged",
        "note": "Test note"
    }
    
    response = client.put(
        f"/api/status/{grievance_id}/status",
        json=status_payload,
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 403
    assert "Invalid token" in response.json()["detail"]


def test_status_update_with_valid_token(client, monkeypatch):
    """Test successful status update with valid authentication"""
    # Set a test token
    test_token = "test_secret_token_123"
    monkeypatch.setenv("ODOO_TOKEN", test_token)
    
    # Need to reload the module to pick up the new env var
    from app.routers import status as status_module
    status_module.ODOO_TOKEN = test_token
    status_module.ALLOWED_IPS = []  # Disable IP checking for tests
    
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Update with valid token
    status_payload = {
        "status": "Acknowledged",
        "note": "Received and processing"
    }
    
    response = client.put(
        f"/api/status/{grievance_id}/status",
        json=status_payload,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["ok"] is True
    assert data["id"] == grievance_id
    assert data["status"] == "Acknowledged"
    
    # Verify the update
    get_response = client.get(f"/api/grievances/{grievance_id}")
    grievance = get_response.json()
    assert grievance["external_status"] == "Acknowledged"
    assert grievance["external_status_note"] == "Received and processing"


def test_status_update_not_found(client, monkeypatch):
    """Test status update for non-existent grievance"""
    test_token = "test_secret_token_123"
    monkeypatch.setenv("ODOO_TOKEN", test_token)
    
    from app.routers import status as status_module
    status_module.ODOO_TOKEN = test_token
    status_module.ALLOWED_IPS = []
    
    status_payload = {
        "status": "Acknowledged",
        "note": "Test note"
    }
    
    response = client.put(
        "/api/status/GRV-01234567890123456789012345/status",
        json=status_payload,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 404


def test_status_update_with_timestamp(client, monkeypatch):
    """Test status update with custom timestamp"""
    test_token = "test_secret_token_123"
    monkeypatch.setenv("ODOO_TOKEN", test_token)
    
    from app.routers import status as status_module
    status_module.ODOO_TOKEN = test_token
    status_module.ALLOWED_IPS = []
    
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Update with custom timestamp
    custom_time = "2025-10-21T10:30:00Z"
    status_payload = {
        "status": "In Progress",
        "note": "Under investigation",
        "updated_at": custom_time
    }
    
    response = client.put(
        f"/api/status/{grievance_id}/status",
        json=status_payload,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200


def test_status_update_without_note(client, monkeypatch):
    """Test status update without optional note field"""
    test_token = "test_secret_token_123"
    monkeypatch.setenv("ODOO_TOKEN", test_token)
    
    from app.routers import status as status_module
    status_module.ODOO_TOKEN = test_token
    status_module.ALLOWED_IPS = []
    
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Update without note
    status_payload = {
        "status": "Resolved"
    }
    
    response = client.put(
        f"/api/status/{grievance_id}/status",
        json=status_payload,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Resolved"


def test_status_update_multiple_times(client, monkeypatch):
    """Test updating status multiple times"""
    test_token = "test_secret_token_123"
    monkeypatch.setenv("ODOO_TOKEN", test_token)
    
    from app.routers import status as status_module
    status_module.ODOO_TOKEN = test_token
    status_module.ALLOWED_IPS = []
    
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # First update
    response = client.put(
        f"/api/status/{grievance_id}/status",
        json={"status": "Acknowledged"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Acknowledged"
    
    # Second update
    response = client.put(
        f"/api/status/{grievance_id}/status",
        json={"status": "In Progress", "note": "Being reviewed"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "In Progress"
    
    # Third update
    response = client.put(
        f"/api/status/{grievance_id}/status",
        json={"status": "Resolved", "note": "Issue resolved"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Resolved"
    
    # Verify final state
    get_response = client.get(f"/api/grievances/{grievance_id}")
    grievance = get_response.json()
    assert grievance["external_status"] == "Resolved"
    assert grievance["external_status_note"] == "Issue resolved"
