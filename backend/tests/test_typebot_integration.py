"""
Test that Typebot's webhook payload format is correctly accepted by the API.
Comprehensive integration tests covering all Typebot flow scenarios.
"""
import pytest


def test_typebot_payload_with_grievance_details_field(client):
    """Test that API accepts 'grievance_details' field name from Typebot"""
    # This is the exact format Typebot sends
    typebot_payload = {
        "is_anonymous": True,
        "grievance_details": "Test grievance from Typebot webhook",  # Note: "grievance_details" not "details"
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    if response.status_code != 201:
        print(f"Error: {response.json()}")
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"].startswith("GRV-")
    assert data["details"] == "Test grievance from Typebot webhook"  # Should be mapped to "details"
    assert data["is_anonymous"] is True


def test_typebot_payload_with_complainant_info(client):
    """Test Typebot payload with full complainant information"""
    typebot_payload = {
        "is_anonymous": False,
        "complainant_name": "John Doe",
        "complainant_email": "john@example.com",
        "complainant_phone": "+676123456",
        "complainant_gender": "Male",
        "is_hh_registered": True,
        "hh_id": "HH12345",
        "hh_address": "Test Village, Test Island",
        "grievance_details": "Need assistance with housing issue",
        "grievance_details_attachment_friendly": "photo1.jpg: https://example.com/photo1.jpg",
        "attachments": [
            {
                "name": "photo1.jpg",
                "url": "https://example.com/photo1.jpg",
                "size": 102400,
                "type": "image/jpeg"
            }
        ]
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    if response.status_code != 201:
        print(f"Error response: {response.json()}")
    assert response.status_code == 201
    
    data = response.json()
    assert data["complainant_name"] == "John Doe"
    assert data["complainant_email"] == "john@example.com"
    assert data["hh_id"] == "HH12345"
    assert data["details"] == "Need assistance with housing issue"
    assert len(data["attachments"]) == 1
    assert data["attachments"][0]["name"] == "photo1.jpg"


def test_typebot_with_location_fields(client):
    """Test Typebot payload with island, district, and village"""
    typebot_payload = {
        "is_anonymous": True,
        "grievance_details": "Issue in specific location",
        "island": "Tarawa",
        "district": "South Tarawa",
        "village": "Bairiki"
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["island"] == "Tarawa"
    assert data["district"] == "South Tarawa"
    assert data["village"] == "Bairiki"
    assert data["details"] == "Issue in specific location"


def test_typebot_with_category_type(client):
    """Test Typebot payload with category_type field"""
    typebot_payload = {
        "is_anonymous": False,
        "complainant_name": "Jane Smith",
        "complainant_email": "jane@example.com",
        "grievance_details": "Financial assistance request",
        "category_type": "Financial Assistance"
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["category_type"] == "Financial Assistance"
    assert data["complainant_name"] == "Jane Smith"


def test_typebot_household_not_registered(client):
    """Test Typebot payload when household is not registered"""
    typebot_payload = {
        "is_anonymous": False,
        "complainant_name": "Bob Johnson",
        "complainant_email": "bob@example.com",
        "is_hh_registered": False,
        "hh_id": None,
        "hh_address": None,
        "grievance_details": "Not registered in Vaka Sosiale"
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_hh_registered"] is False
    assert data["hh_id"] is None


def test_typebot_multiple_attachments(client):
    """Test Typebot payload with multiple file attachments"""
    typebot_payload = {
        "is_anonymous": False,
        "complainant_name": "Mary Jones",
        "complainant_email": "mary@example.com",
        "grievance_details": "Multiple documents attached",
        "attachments": [
            {
                "name": "document1.pdf",
                "url": "https://example.com/doc1.pdf",
                "size": 204800,
                "type": "application/pdf"
            },
            {
                "name": "photo1.jpg",
                "url": "https://example.com/photo1.jpg",
                "size": 102400,
                "type": "image/jpeg"
            },
            {
                "name": "evidence.png",
                "url": "https://example.com/evidence.png",
                "size": 153600,
                "type": "image/png"
            }
        ]
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert len(data["attachments"]) == 3
    assert data["attachments"][0]["name"] == "document1.pdf"
    assert data["attachments"][1]["name"] == "photo1.jpg"
    assert data["attachments"][2]["name"] == "evidence.png"


def test_typebot_status_lookup_success(client):
    """Test the GET grievance endpoint used by Typebot status lookup"""
    # First create a grievance
    create_payload = {
        "is_anonymous": False,
        "complainant_name": "Test User",
        "complainant_email": "test@example.com",
        "grievance_details": "Test for status lookup",
        "island": "Test Island",
        "category_type": "Test Category",
        "hh_id": "HH999"
    }
    
    create_response = client.post("/api/grievances/", json=create_payload)
    assert create_response.status_code == 201
    grievance_id = create_response.json()["id"]
    
    # Now look it up (as Typebot would)
    lookup_response = client.get(f"/api/grievances/{grievance_id}")
    assert lookup_response.status_code == 200
    
    data = lookup_response.json()
    assert data["id"] == grievance_id
    assert data["details"] == "Test for status lookup"
    assert data["island"] == "Test Island"
    assert data["category_type"] == "Test Category"
    assert data["hh_id"] == "HH999"
    assert data["is_anonymous"] is False
    assert "external_status" in data
    assert "created_at" in data


def test_typebot_status_lookup_not_found(client):
    """Test Typebot status lookup with invalid ID"""
    response = client.get("/api/grievances/GRV-INVALID00000000000000000")
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data


def test_typebot_status_lookup_invalid_format(client):
    """Test Typebot status lookup with malformed ID"""
    response = client.get("/api/grievances/INVALID-ID")
    # API returns 404 for any non-existent ID (doesn't validate format on GET)
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data


def test_api_still_accepts_details_field(client):
    """Test that API still accepts the standard 'details' field name"""
    # Standard API payload using "details" instead of "grievance_details"
    standard_payload = {
        "is_anonymous": True,
        "details": "Test using standard field name"
    }
    
    response = client.post("/api/grievances/", json=standard_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["details"] == "Test using standard field name"


def test_typebot_empty_fields(client):
    """Test that Typebot's empty string fields are handled correctly"""
    typebot_payload = {
        "is_anonymous": True,
        "grievance_details": "Anonymous submission with minimal fields"
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is True
    assert data["details"] == "Anonymous submission with minimal fields"


def test_typebot_full_anonymous_flow(client):
    """Test complete anonymous flow as Typebot would submit it"""
    typebot_payload = {
        "is_anonymous": True,
        "complainant_name": None,
        "complainant_email": None,
        "complainant_phone": None,
        "complainant_gender": None,
        "is_hh_registered": None,
        "hh_id": None,
        "hh_address": None,
        "grievance_details": "Anonymous complaint about service delivery",
        "category_type": "Service Delivery",
        "island": "Kiritimati",
        "district": None,
        "village": None,
        "grievance_details_attachment_friendly": None,
        "attachments": None
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is True
    assert data["complainant_name"] is None
    assert data["details"] == "Anonymous complaint about service delivery"
    assert data["category_type"] == "Service Delivery"
    assert data["island"] == "Kiritimati"


def test_typebot_full_named_flow_with_household(client):
    """Test complete named flow with household registration"""
    typebot_payload = {
        "is_anonymous": False,
        "complainant_name": "Alice Williams",
        "complainant_email": "alice@example.com",
        "complainant_phone": "+676555123",
        "complainant_gender": "Female",
        "is_hh_registered": True,
        "hh_id": "HH2024001",
        "hh_address": "Main Street, Betio",
        "grievance_details": "Request for housing assistance",
        "category_type": "Housing",
        "island": "Tarawa",
        "district": "Betio",
        "village": "Betio Town",
        "grievance_details_attachment_friendly": "id_card.jpg",
        "attachments": [
            {
                "name": "id_card.jpg",
                "url": "https://example.com/id_card.jpg",
                "size": 256000,
                "type": "image/jpeg"
            }
        ]
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["is_anonymous"] is False
    assert data["complainant_name"] == "Alice Williams"
    assert data["complainant_email"] == "alice@example.com"
    assert data["is_hh_registered"] is True
    assert data["hh_id"] == "HH2024001"
    assert data["hh_address"] == "Main Street, Betio"
    assert data["details"] == "Request for housing assistance"
    assert data["category_type"] == "Housing"
    assert data["island"] == "Tarawa"
    assert data["district"] == "Betio"
    assert data["village"] == "Betio Town"
    assert len(data["attachments"]) == 1


def test_typebot_receipt_pdf_generation(client):
    """Test PDF receipt generation as used by Typebot confirmation"""
    # Create a grievance
    typebot_payload = {
        "is_anonymous": False,
        "complainant_name": "Receipt Test User",
        "complainant_email": "receipt@example.com",
        "grievance_details": "Test for PDF receipt"
    }
    
    create_response = client.post("/api/grievances/", json=typebot_payload)
    assert create_response.status_code == 201
    grievance_id = create_response.json()["id"]
    
    # Request the PDF receipt
    pdf_response = client.get(f"/api/grievances/{grievance_id}/receipt.pdf")
    assert pdf_response.status_code == 200
    assert pdf_response.headers["content-type"] == "application/pdf"
    assert len(pdf_response.content) > 0  # PDF has content


def test_typebot_both_grievance_details_and_details_provided(client):
    """Test when both 'grievance_details' and 'details' are provided"""
    typebot_payload = {
        "is_anonymous": True,
        "grievance_details": "This should be ignored",
        "details": "This should be used"
    }
    
    response = client.post("/api/grievances/", json=typebot_payload)
    assert response.status_code == 201
    
    data = response.json()
    # When both are provided, 'details' takes precedence (standard API behavior)
    assert data["details"] == "This should be used"
