import pytest
from datetime import datetime, timezone


def test_batch_update_success(client):
    """Test batch updating multiple grievances"""
    # Create some grievances first
    grievance_ids = []
    for i in range(3):
        payload = {
            "is_anonymous": True,
            "category_type": f"Category {i}",
            "details": f"Test grievance {i}"
        }
        response = client.post("/api/grievances/", json=payload)
        assert response.status_code == 201
        grievance_ids.append(response.json()["id"])
    
    # Batch update them
    batch_payload = {
        "updates": [
            {
                "gid": grievance_ids[0],
                "external_status": "Acknowledged",
                "external_status_note": "Received and logged"
            },
            {
                "gid": grievance_ids[1],
                "external_status": "In Progress",
                "external_status_note": "Under investigation",
                "category_type": "Updated Category"
            },
            {
                "gid": grievance_ids[2],
                "external_status": "Resolved",
                "hh_id": "HH123"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 3
    
    # Check all updates succeeded
    for result in data["results"]:
        assert result["ok"] is True
        assert "gid" in result
        assert "updated_fields" in result


def test_batch_update_partial_success(client):
    """Test batch update with some valid and some invalid IDs"""
    # Create one valid grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    valid_id = response.json()["id"]
    
    # Batch update with one valid and one invalid ID
    batch_payload = {
        "updates": [
            {
                "gid": valid_id,
                "external_status": "Acknowledged"
            },
            {
                "gid": "GRV-01234567890123456789012345",  # Valid format but doesn't exist
                "external_status": "In Progress"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    results = data["results"]
    
    # First should succeed
    assert results[0]["ok"] is True
    assert results[0]["gid"] == valid_id
    
    # Second should fail
    assert results[1]["ok"] is False
    assert results[1]["gid"] == "GRV-01234567890123456789012345"
    assert "error" in results[1]
    assert "not found" in results[1]["error"].lower()


def test_batch_update_with_location_fields(client):
    """Test batch update with location field overrides"""
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Update with location fields
    batch_payload = {
        "updates": [
            {
                "gid": grievance_id,
                "island": "Tarawa",
                "district": "South",
                "village": "Betio"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["results"][0]["ok"] is True
    assert "island" in data["results"][0]["updated_fields"]
    assert "district" in data["results"][0]["updated_fields"]
    assert "village" in data["results"][0]["updated_fields"]
    
    # Verify the update
    get_response = client.get(f"/api/grievances/{grievance_id}")
    grievance = get_response.json()
    assert grievance["island"] == "Tarawa"
    assert grievance["district"] == "South"
    assert grievance["village"] == "Betio"


def test_batch_update_empty_list(client):
    """Test batch update with empty updates list"""
    batch_payload = {
        "updates": []
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["results"] == []


def test_batch_update_with_timestamp(client):
    """Test batch update with external_updated_at timestamp"""
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Update with custom timestamp
    custom_time = datetime(2025, 10, 21, 12, 0, 0, tzinfo=timezone.utc)
    batch_payload = {
        "updates": [
            {
                "gid": grievance_id,
                "external_status": "Processed",
                "external_updated_at": custom_time.isoformat()
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["results"][0]["ok"] is True
    assert "external_updated_at" in data["results"][0]["updated_fields"]

