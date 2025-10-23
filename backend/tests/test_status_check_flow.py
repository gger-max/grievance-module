"""
Comprehensive tests for the grievance status check feature from Typebot.

This module tests the complete flow of checking a grievance's status,
simulating what happens when a user interacts with the Typebot interface.
"""
import pytest
from datetime import datetime, timezone


def test_complete_status_check_flow(client):
    """
    Test the complete status check flow as it would be used from Typebot.
    
    This simulates:
    1. User submits a grievance and receives an ID
    2. User later checks the status using that ID
    3. User sees all relevant status information
    """
    # Step 1: Create a grievance (simulating Typebot submission)
    create_payload = {
        "is_anonymous": False,
        "complainant_name": "John Doe",
        "complainant_email": "john@example.com",
        "complainant_phone": "+676123456",
        "grievance_details": "Test grievance for status check",
        "category_type": "Service Delivery",
        "island": "Tarawa",
        "district": "South Tarawa",
        "village": "Bairiki"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    assert create_response.status_code == 201
    
    created_data = create_response.json()
    grievance_id = created_data["id"]
    
    # Verify the ID format matches what Typebot expects
    assert grievance_id.startswith("GRV-")
    assert len(grievance_id) == 30  # GRV- + 26 character ULID
    
    # Step 2: Check status (simulating Typebot status lookup)
    status_response = client.get(f"/api/grievances/{grievance_id}")
    assert status_response.status_code == 200
    
    status_data = status_response.json()
    
    # Step 3: Verify all expected fields are present and correct
    # These are the fields that Typebot displays to users
    assert status_data["id"] == grievance_id
    assert status_data["details"] == "Test grievance for status check"
    assert status_data["category_type"] == "Service Delivery"
    assert status_data["island"] == "Tarawa"
    assert status_data["district"] == "South Tarawa"
    assert status_data["village"] == "Bairiki"
    assert status_data["is_anonymous"] is False
    
    # Status fields (may be None initially)
    assert "external_status" in status_data
    assert "external_status_note" in status_data
    
    # Timestamps
    assert "created_at" in status_data
    assert "updated_at" in status_data
    
    # Personal information (since not anonymous)
    assert status_data["complainant_name"] == "John Doe"
    assert status_data["complainant_email"] == "john@example.com"
    assert status_data["complainant_phone"] == "+676123456"


def test_status_check_with_external_status_update(client):
    """
    Test status check after an external system (like Odoo) has updated the status.
    
    This verifies that users can see status updates made by case workers.
    """
    # Create a grievance
    create_payload = {
        "is_anonymous": True,
        "grievance_details": "Need urgent assistance",
        "category_type": "Emergency"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Simulate an external system updating the status (this would normally require auth)
    # For this test, we'll use the internal update endpoint
    update_payload = {
        "external_status": "Under Review",
        "external_status_note": "Case assigned to social worker",
        "external_updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    update_response = client.put(
        f"/api/grievances/{grievance_id}/status",
        json=update_payload
    )
    assert update_response.status_code == 200
    
    # Now check the status (as user would from Typebot)
    status_response = client.get(f"/api/grievances/{grievance_id}")
    assert status_response.status_code == 200
    
    status_data = status_response.json()
    assert status_data["external_status"] == "Under Review"
    assert status_data["external_status_note"] == "Case assigned to social worker"


def test_status_check_anonymous_grievance(client):
    """
    Test status check for an anonymous grievance.
    
    Verifies that personal information is not leaked for anonymous submissions.
    """
    create_payload = {
        "is_anonymous": True,
        "grievance_details": "Anonymous feedback",
        "category_type": "General Feedback"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Check status
    status_response = client.get(f"/api/grievances/{grievance_id}")
    status_data = status_response.json()
    
    # Verify no personal information is exposed
    assert status_data["is_anonymous"] is True
    assert status_data["complainant_name"] is None
    assert status_data["complainant_email"] is None
    assert status_data["complainant_phone"] is None
    
    # But other information should be present
    assert status_data["details"] == "Anonymous feedback"
    assert status_data["category_type"] == "General Feedback"


def test_status_check_with_invalid_id_format(client):
    """
    Test that status check fails gracefully with invalid ID format.
    
    This matches the validation done in Typebot's regex check.
    """
    # Test various invalid formats
    invalid_ids = [
        "INVALID",
        "GRV-123",  # Too short
        "GRV-TOOLONGID0123456789ABCDEFGHIJKLMNOP",  # Too long
        "GRV",  # Just prefix
        "01K88MF7431X7NF9D4GHQN5742",  # Missing prefix
    ]
    
    for invalid_id in invalid_ids:
        response = client.get(f"/api/grievances/{invalid_id}")
        assert response.status_code == 404
        assert "detail" in response.json()


def test_status_check_multiple_times(client):
    """
    Test that a user can check status multiple times.
    
    This is a common use case where users want to track progress.
    """
    # Create a grievance
    create_payload = {
        "is_anonymous": False,
        "complainant_name": "Jane Smith",
        "complainant_email": "jane@example.com",
        "grievance_details": "Request for information",
        "category_type": "Information Request"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Check status multiple times
    for i in range(3):
        status_response = client.get(f"/api/grievances/{grievance_id}")
        assert status_response.status_code == 200
        
        status_data = status_response.json()
        assert status_data["id"] == grievance_id
        assert status_data["details"] == "Request for information"


def test_status_check_with_household_info(client):
    """
    Test status check for grievance with household registration.
    
    Verifies that household information is properly returned.
    """
    create_payload = {
        "is_anonymous": False,
        "complainant_name": "Bob Wilson",
        "is_hh_registered": True,
        "hh_id": "HH2024001",
        "hh_address": "123 Main Street",
        "grievance_details": "Housing assistance request",
        "category_type": "Housing",
        "island": "Abemama",
        "district": "West",
        "village": "Kariatebike"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Check status
    status_response = client.get(f"/api/grievances/{grievance_id}")
    status_data = status_response.json()
    
    # Verify household information is returned
    assert status_data["is_hh_registered"] is True
    assert status_data["hh_id"] == "HH2024001"
    assert status_data["hh_address"] == "123 Main Street"
    assert status_data["island"] == "Abemama"
    assert status_data["district"] == "West"
    assert status_data["village"] == "Kariatebike"
