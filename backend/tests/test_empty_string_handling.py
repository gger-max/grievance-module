"""
Test that empty strings from Typebot are properly handled by converting them to None.
This is critical for non-anonymous grievance submissions where some fields may be empty.
"""
import pytest


def test_non_anonymous_with_empty_email(client):
    """Test non-anonymous grievance with empty email string (as Typebot sends)"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "John Doe",
        "complainant_email": "",  # Empty string instead of null
        "complainant_phone": "+676123456",
        "complainant_gender": "Male",
        "grievance_details": "Need assistance"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is False
    assert data["complainant_name"] == "John Doe"
    assert data["complainant_email"] is None  # Should be None, not empty string
    assert data["complainant_phone"] == "+676123456"


def test_non_anonymous_with_all_empty_optional_fields(client):
    """Test non-anonymous with only name provided, all other fields empty"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "Jane Smith",
        "complainant_email": "",
        "complainant_phone": "",
        "complainant_gender": "",
        "hh_id": "",
        "hh_address": "",
        "island": "",
        "district": "",
        "village": "",
        "category_type": "",
        "grievance_details": "Urgent matter"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is False
    assert data["complainant_name"] == "Jane Smith"
    assert data["complainant_email"] is None
    assert data["complainant_phone"] is None
    assert data["complainant_gender"] is None
    assert data["hh_id"] is None
    assert data["hh_address"] is None
    assert data["island"] is None
    assert data["district"] is None
    assert data["village"] is None
    assert data["category_type"] is None


def test_anonymous_with_empty_complainant_fields(client):
    """Test anonymous grievance with empty complainant fields (typical Typebot flow)"""
    payload = {
        "is_anonymous": True,
        "complainant_name": "",
        "complainant_email": "",
        "complainant_phone": "",
        "complainant_gender": "",
        "grievance_details": "Anonymous complaint"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is True
    assert data["complainant_name"] is None
    assert data["complainant_email"] is None
    assert data["complainant_phone"] is None
    assert data["complainant_gender"] is None


def test_mixed_empty_and_filled_fields(client):
    """Test with some fields filled and some empty"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "Bob Johnson",
        "complainant_email": "bob@example.com",  # Valid email
        "complainant_phone": "",  # Empty
        "complainant_gender": "Male",  # Filled
        "hh_id": "",  # Empty
        "hh_address": "123 Main St",  # Filled
        "grievance_details": "Mixed data test"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["complainant_name"] == "Bob Johnson"
    assert data["complainant_email"] == "bob@example.com"
    assert data["complainant_phone"] is None  # Empty → None
    assert data["complainant_gender"] == "Male"
    assert data["hh_id"] is None  # Empty → None
    assert data["hh_address"] == "123 Main St"


def test_empty_grievance_details_converted_to_none(client):
    """Test that empty grievance_details is converted to None"""
    payload = {
        "is_anonymous": True,
        "grievance_details": ""  # Empty details
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["details"] is None


def test_empty_category_type(client):
    """Test that empty category_type is converted to None"""
    payload = {
        "is_anonymous": True,
        "category_type": "",
        "grievance_details": "Test"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["category_type"] is None


def test_valid_email_not_affected(client):
    """Ensure valid emails are not affected by empty string conversion"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "Alice Williams",
        "complainant_email": "alice@example.com",
        "grievance_details": "Test with valid email"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["complainant_email"] == "alice@example.com"


def test_null_values_still_work(client):
    """Ensure explicit null values still work correctly"""
    payload = {
        "is_anonymous": True,
        "complainant_name": None,
        "complainant_email": None,
        "complainant_phone": None,
        "grievance_details": "Test with explicit nulls"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["complainant_name"] is None
    assert data["complainant_email"] is None
    assert data["complainant_phone"] is None


def test_typebot_realistic_non_anonymous_payload(client):
    """
    Test a realistic payload from Typebot for non-anonymous submission.
    This mimics what Typebot actually sends when a user chooses not to be anonymous.
    """
    payload = {
        "is_anonymous": False,
        "complainant_name": "Maria Garcia",
        "complainant_email": "maria@example.com",
        "complainant_phone": "+676789012",
        "complainant_gender": "Female",
        "is_hh_registered": True,
        "hh_id": "HH2024123",
        "hh_address": "Village Center, Island",
        "island": "Tongatapu",
        "district": "",  # Empty - not provided by user
        "village": "Nuku'alofa",
        "category_type": "",  # Empty - not selected
        "grievance_details": "I need help with housing assistance",
        "grievance_details_attachment_friendly": "",  # Empty - no attachments
        "attachments": None
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is False
    assert data["complainant_name"] == "Maria Garcia"
    assert data["complainant_email"] == "maria@example.com"
    assert data["complainant_phone"] == "+676789012"
    assert data["is_hh_registered"] is True
    assert data["hh_id"] == "HH2024123"
    assert data["district"] is None  # Empty string → None
    assert data["category_type"] is None  # Empty string → None
    assert data["village"] == "Nuku'alofa"
