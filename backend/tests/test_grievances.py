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


def test_create_grievance_non_anonymous_with_single_attachment(client):
    """Test creating a non-anonymous grievance with single file attachment"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "John Smith",
        "complainant_email": "john.smith@example.com",
        "complainant_phone": "+676123456",
        "category_type": "Service Complaint",
        "details": "Issue with service delivery - photo attached",
        "island": "Tarawa",
        "attachments": [
            {
                "name": "evidence.jpg",
                "url": "https://example.com/uploads/evidence.jpg",
                "size": 204800,
                "type": "image/jpeg"
            }
        ]
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is False
    assert data["complainant_name"] == "John Smith"
    assert data["complainant_email"] == "john.smith@example.com"
    assert data["complainant_phone"] == "+676123456"
    assert data["details"] == "Issue with service delivery - photo attached"
    assert data["attachments"] is not None
    assert len(data["attachments"]) == 1
    assert data["attachments"][0]["name"] == "evidence.jpg"
    assert data["attachments"][0]["url"] == "https://example.com/uploads/evidence.jpg"
    assert data["attachments"][0]["size"] == 204800
    assert data["attachments"][0]["type"] == "image/jpeg"


def test_create_grievance_non_anonymous_with_multiple_attachments(client):
    """Test creating a non-anonymous grievance with multiple file attachments"""
    payload = {
        "is_anonymous": False,
        "complainant_name": "Jane Doe",
        "complainant_email": "jane.doe@example.com",
        "complainant_phone": "+676789012",
        "complainant_gender": "Female",
        "category_type": "Financial Assistance",
        "details": "Request for assistance - documents attached",
        "island": "Abemama",
        "district": "North",
        "village": "Kariatebike",
        "attachments": [
            {
                "name": "id_card.pdf",
                "url": "https://example.com/uploads/id_card.pdf",
                "size": 512000,
                "type": "application/pdf"
            },
            {
                "name": "proof_of_residence.jpg",
                "url": "https://example.com/uploads/proof.jpg",
                "size": 307200,
                "type": "image/jpeg"
            },
            {
                "name": "application_form.png",
                "url": "https://example.com/uploads/form.png",
                "size": 409600,
                "type": "image/png"
            }
        ]
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is False
    assert data["complainant_name"] == "Jane Doe"
    assert data["complainant_email"] == "jane.doe@example.com"
    assert data["complainant_phone"] == "+676789012"
    assert data["complainant_gender"] == "Female"
    assert data["details"] == "Request for assistance - documents attached"
    assert data["island"] == "Abemama"
    assert data["district"] == "North"
    assert data["village"] == "Kariatebike"
    assert data["attachments"] is not None
    assert len(data["attachments"]) == 3
    assert data["attachments"][0]["name"] == "id_card.pdf"
    assert data["attachments"][0]["type"] == "application/pdf"
    assert data["attachments"][1]["name"] == "proof_of_residence.jpg"
    assert data["attachments"][1]["type"] == "image/jpeg"
    assert data["attachments"][2]["name"] == "application_form.png"
    assert data["attachments"][2]["type"] == "image/png"


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


def test_create_grievance_with_client_provided_id(client):
    """Test creating a grievance with client-provided ID (ULID format)"""
    client_id = "GRV-01K8VARG6HWGB7ET8Y8EGJP6A1"
    payload = {
        "id": client_id,
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test with client-provided ULID"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"] == client_id  # Should use client-provided ID
    assert data["is_anonymous"] is True
    assert data["details"] == "Test with client-provided ULID"


def test_create_grievance_with_client_provided_ulid(client):
    """Test creating a grievance with client-provided ULID format"""
    client_id = "GRV-01K88MF7431X7NF9D4GHQN5742"
    payload = {
        "id": client_id,
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test with client-provided ULID"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"] == client_id  # Should use client-provided ID
    assert data["is_anonymous"] is True


def test_create_grievance_with_invalid_client_id(client):
    """Test that invalid client ID is rejected and server generates new ID"""
    invalid_id = "INVALID-ID-123"
    payload = {
        "id": invalid_id,
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test with invalid client ID"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"] != invalid_id  # Should NOT use invalid ID
    assert data["id"].startswith("GRV-")  # Should generate valid ID
    assert len(data["id"]) == 30  # ULID format: GRV- + 26 chars


def test_create_grievance_without_client_id(client):
    """Test that server generates ID when none provided"""
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test without client ID"
    }
    
    response = client.post("/api/grievances/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"].startswith("GRV-")  # Should generate valid ID
    assert len(data["id"]) == 30  # ULID format


def test_update_grievance_category_type(client):
    """Test updating a grievance category type"""
    # Create a grievance
    create_payload = {
        "is_anonymous": True,
        "category_type": "Original Category",
        "details": "Test grievance for category update"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    assert create_response.status_code == 201
    grievance_id = create_response.json()["id"]
    
    # Update the category type
    update_payload = {
        "category_type": "Updated Category"
    }
    
    update_response = client.put(f"/api/grievances/{grievance_id}/status", json=update_payload)
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["category_type"] == "Updated Category"
    
    # Verify the update persists
    get_response = client.get(f"/api/grievances/{grievance_id}")
    assert get_response.status_code == 200
    retrieved_data = get_response.json()
    assert retrieved_data["category_type"] == "Updated Category"


def test_update_grievance_location_with_hh_id(client):
    """Test that updating grievance with household ID updates location from Odoo"""
    # Create a grievance without location
    create_payload = {
        "is_anonymous": False,
        "complainant_name": "Test User",
        "category_type": "Test",
        "details": "Test grievance"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Verify no location initially
    get_response = client.get(f"/api/grievances/{grievance_id}")
    initial_data = get_response.json()
    assert initial_data["island"] is None
    assert initial_data["district"] is None
    assert initial_data["village"] is None
    
    # Update with HH ID which should populate location from Odoo stub
    update_payload = {
        "hh_id": "HH123"
    }
    
    update_response = client.put(f"/api/grievances/{grievance_id}/status", json=update_payload)
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["hh_id"] == "HH123"
    # Check that Odoo stub populated location data
    assert data["island"] == "Maiana"
    assert data["district"] == "North"
    assert data["village"] == "Tabontebike"


def test_update_grievance_status_and_note(client):
    """Test updating grievance status and note together"""
    # Create a grievance
    create_payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance for status update"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    assert create_response.status_code == 201
    grievance_id = create_response.json()["id"]
    
    # Verify no status initially
    get_response = client.get(f"/api/grievances/{grievance_id}")
    initial_data = get_response.json()
    assert initial_data["external_status"] is None
    assert initial_data["external_status_note"] is None
    
    # Update status and note
    update_payload = {
        "external_status": "Resolved",
        "external_status_note": "Issue has been resolved successfully"
    }
    
    update_response = client.put(f"/api/grievances/{grievance_id}/status", json=update_payload)
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["external_status"] == "Resolved"
    assert data["external_status_note"] == "Issue has been resolved successfully"
    
    # Verify the update persists
    get_response = client.get(f"/api/grievances/{grievance_id}")
    assert get_response.status_code == 200
    retrieved_data = get_response.json()
    assert retrieved_data["external_status"] == "Resolved"
    assert retrieved_data["external_status_note"] == "Issue has been resolved successfully"


def test_update_grievance_status_only(client):
    """Test updating only the grievance status without note"""
    # Create a grievance
    create_payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Update only status
    update_payload = {
        "external_status": "Acknowledged"
    }
    
    update_response = client.put(f"/api/grievances/{grievance_id}/status", json=update_payload)
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["external_status"] == "Acknowledged"
    assert data["external_status_note"] is None


def test_update_grievance_multiple_fields(client):
    """Test updating status, category, and household ID together"""
    # Create a grievance
    create_payload = {
        "is_anonymous": False,
        "complainant_name": "Test User",
        "category_type": "Original Category",
        "details": "Test grievance"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    grievance_id = create_response.json()["id"]
    
    # Update multiple fields
    update_payload = {
        "external_status": "In Progress",
        "external_status_note": "Currently being reviewed",
        "category_type": "Updated Category",
        "hh_id": "HH456"
    }
    
    update_response = client.put(f"/api/grievances/{grievance_id}/status", json=update_payload)
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["external_status"] == "In Progress"
    assert data["external_status_note"] == "Currently being reviewed"
    assert data["category_type"] == "Updated Category"
    assert data["hh_id"] == "HH456"
    # Location should be updated from Odoo stub for HH456
    assert data["island"] == "Abemama"
    assert data["district"] == "West"
    assert data["village"] == "Kariatebike"

