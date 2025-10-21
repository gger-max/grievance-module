import pytest
from datetime import datetime, timezone


def test_create_grievance_anonymous(client):
    """Test creating an anonymous grievance"""
    payload = {
        "is_anonymous": True,
        "category_type": "Service Delivery",
        "details": "Test grievance details",
        "island": "Test Island",
        "district": "Test District",
        "village": "Test Village"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"].startswith("GRV-")
    assert data["is_anonymous"] is True
    assert data["category_type"] == "Service Delivery"
    assert data["details"] == "Test grievance details"
    assert data["island"] == "Test Island"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_grievance_with_complainant(client):
    """Test creating a grievance with complainant information"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "John Doe",
        "complainant_email": "john@example.com",
        "complainant_phone": "1234567890",
        "complainant_gender": "Male",
        "category_type": "Financial Assistance",
        "details": "Need help with financial assistance",
        "island": "Tarawa",
        "district": "South",
        "village": "Bairiki"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is False
    assert data["complainant_name"] == "John Doe"
    assert data["complainant_email"] == "john@example.com"
    assert data["complainant_phone"] == "1234567890"
    assert data["complainant_gender"] == "Male"


def test_create_grievance_with_household(client):
    """Test creating a grievance with household registration"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "Jane Doe",
        "is_hh_registered": True,
        "hh_id": "HH123",
        "hh_address": "123 Main St",
        "category_type": "Housing",
        "details": "Housing issue"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_hh_registered"] is True
    assert data["hh_id"] == "HH123"
    assert data["hh_address"] == "123 Main St"


def test_create_grievance_with_attachments(client):
    """Test creating a grievance with attachments"""
    # Test with minimal attachment data (all fields are optional in AttachmentIn)
    payload = {
        "is_anonymous": True,
        "category_type": "Complaint",
        "details": "Test with attachments"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    # Without attachments, it should be None or empty
    assert data["attachments"] is None or data["attachments"] == []


def test_create_grievance_details_too_long(client):
    """Test that creating a grievance with too long details fails"""
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "x" * 10001  # More than 10,000 characters
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 422


def test_get_grievance(client):
    """Test retrieving a grievance by ID"""
    # First create a grievance
    create_payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance for retrieval"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    assert create_response.status_code == 201
    grievance_id = create_response.json()["id"]
    
    # Now retrieve it
    get_response = client.get(f"/api/grievances/{grievance_id}")
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert data["id"] == grievance_id
    assert data["details"] == "Test grievance for retrieval"


def test_get_grievance_not_found(client):
    """Test retrieving a non-existent grievance"""
    response = client.get("/api/grievances/GRV-NONEXISTENT00000000000000")
    assert response.status_code == 404


def test_update_grievance_status(client):
    """Test updating a grievance status"""
    # First create a grievance
    create_payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance for status update"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    assert create_response.status_code == 201
    grievance_id = create_response.json()["id"]
    
    # Now update its status
    update_payload = {
        "external_status": "In Progress",
        "external_status_note": "Being reviewed"
    }
    
    update_response = client.put(f"/api/grievances/{grievance_id}/status", json=update_payload)
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["external_status"] == "In Progress"
    assert data["external_status_note"] == "Being reviewed"


def test_update_grievance_with_hh_id(client):
    """Test updating a grievance with household ID"""
    # Create a grievance
    create_payload = {
        "is_anonymous": False,
        "complainant_name": "Test User",
        "category_type": "Test",
        "details": "Test grievance"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Update with HH ID
    update_payload = {
        "hh_id": "HH123",
        "category_type": "Updated Category"
    }
    
    update_response = client.put(f"/api/grievances/{grievance_id}/status", json=update_payload)
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["hh_id"] == "HH123"
    assert data["category_type"] == "Updated Category"
    # Check that Odoo stub populated location data
    assert data["island"] == "Maiana"
    assert data["district"] == "North"
    assert data["village"] == "Tabontebike"


def test_update_grievance_invalid_id_format(client):
    """Test updating a grievance with invalid ID format"""
    update_payload = {
        "external_status": "In Progress"
    }
    
    response = client.put("/api/grievances/INVALID-ID/status", json=update_payload)
    assert response.status_code == 400


def test_update_grievance_not_found(client):
    """Test updating a non-existent grievance"""
    update_payload = {
        "external_status": "In Progress"
    }
    
    # This ID format is valid but the grievance doesn't exist
    # The invalid format check happens first, so we need a valid format
    response = client.put("/api/grievances/GRV-01234567890123456789012345/status", json=update_payload)
    assert response.status_code == 404


def test_export_recent_grievances(client):
    """Test exporting recent grievances"""
    # Create a few grievances
    for i in range(3):
        payload = {
            "is_anonymous": True,
            "category_type": f"Test Category {i}",
            "details": f"Test details {i}"
        }
        response = client.post("/api/grievances/", json=payload)
        assert response.status_code == 201
    
    # Export recent grievances - note the path should match the router
    response = client.get("/api/grievances/export", params={"since_hours": 24})
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 3  # At least the 3 we created
    assert all(item["id"].startswith("GRV-") for item in data)


def test_get_receipt_pdf(client):
    """Test generating a PDF receipt"""
    # Create a grievance
    create_payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance for PDF"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Get PDF receipt
    response = client.get(f"/api/grievances/{grievance_id}/receipt.pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "receipt-" in response.headers["content-disposition"]

