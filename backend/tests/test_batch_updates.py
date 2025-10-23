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


def test_batch_update_all_invalid_ids(client):
    """Test batch update where all grievance IDs are invalid"""
    batch_payload = {
        "updates": [
            {
                "gid": "GRV-01234567890123456789012345",
                "external_status": "Acknowledged"
            },
            {
                "gid": "GRV-98765432109876543210987654",
                "external_status": "In Progress"
            },
            {
                "gid": "GRV-11111111111111111111111111",
                "external_status": "Resolved"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["results"]) == 3
    
    # All should fail
    for result in data["results"]:
        assert result["ok"] is False
        assert "error" in result
        assert "not found" in result["error"].lower()


def test_batch_update_duplicate_ids(client):
    """Test batch update with duplicate IDs in same request"""
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Test",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Try to update same grievance multiple times in one batch
    batch_payload = {
        "updates": [
            {
                "gid": grievance_id,
                "external_status": "Acknowledged"
            },
            {
                "gid": grievance_id,
                "external_status": "In Progress"
            },
            {
                "gid": grievance_id,
                "external_status": "Resolved"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["results"]) == 3
    
    # All updates should succeed (last one wins)
    for result in data["results"]:
        assert result["ok"] is True
    
    # Verify final status is from the last update
    get_response = client.get(f"/api/grievances/{grievance_id}")
    grievance = get_response.json()
    assert grievance["external_status"] == "Resolved"


def test_batch_update_invalid_gid_format(client):
    """Test batch update with invalid grievance ID format"""
    batch_payload = {
        "updates": [
            {
                "gid": "INVALID-ID-123",
                "external_status": "Acknowledged"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 422  # Validation error
    
    # Check error details
    data = response.json()
    assert "detail" in data


def test_batch_update_all_fields(client):
    """Test batch update with all available fields"""
    # Create a grievance
    payload = {
        "is_anonymous": True,
        "category_type": "Original Category",
        "details": "Test grievance"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Update all fields at once
    custom_time = datetime(2025, 10, 22, 15, 30, 0, tzinfo=timezone.utc)
    batch_payload = {
        "updates": [
            {
                "gid": grievance_id,
                "external_status": "Resolved",
                "external_status_note": "Fully resolved after investigation",
                "external_updated_at": custom_time.isoformat(),
                "category_type": "Updated Category",
                "hh_id": "HH-12345",
                "island": "Tarawa",
                "district": "North",
                "village": "Bikenibeu"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["results"][0]["ok"] is True
    
    # Verify all 8 fields were updated
    updated_fields = data["results"][0]["updated_fields"]
    assert len(updated_fields) == 8
    assert "external_status" in updated_fields
    assert "external_status_note" in updated_fields
    assert "external_updated_at" in updated_fields
    assert "category_type" in updated_fields
    assert "hh_id" in updated_fields
    assert "island" in updated_fields
    assert "district" in updated_fields
    assert "village" in updated_fields
    
    # Verify the updates persisted
    get_response = client.get(f"/api/grievances/{grievance_id}")
    grievance = get_response.json()
    assert grievance["external_status"] == "Resolved"
    assert grievance["external_status_note"] == "Fully resolved after investigation"
    assert grievance["category_type"] == "Updated Category"
    assert grievance["hh_id"] == "HH-12345"
    assert grievance["island"] == "Tarawa"
    assert grievance["district"] == "North"
    assert grievance["village"] == "Bikenibeu"


def test_batch_update_large_batch(client):
    """Test batch update with many grievances (stress test)"""
    # Create 20 grievances
    grievance_ids = []
    for i in range(20):
        payload = {
            "is_anonymous": True,
            "category_type": f"Category {i}",
            "details": f"Test grievance {i}"
        }
        response = client.post("/api/grievances/", json=payload)
        assert response.status_code == 201
        grievance_ids.append(response.json()["id"])
    
    # Batch update all of them
    batch_payload = {
        "updates": [
            {
                "gid": gid,
                "external_status": "Processed",
                "external_status_note": f"Batch processed item {i}"
            }
            for i, gid in enumerate(grievance_ids)
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["results"]) == 20
    
    # All should succeed
    for result in data["results"]:
        assert result["ok"] is True
        assert "external_status" in result["updated_fields"]
        assert "external_status_note" in result["updated_fields"]
    
    # Spot check a few grievances
    for i in [0, 10, 19]:
        get_response = client.get(f"/api/grievances/{grievance_ids[i]}")
        grievance = get_response.json()
        assert grievance["external_status"] == "Processed"
        assert f"item {i}" in grievance["external_status_note"]


def test_batch_update_transaction_isolation(client):
    """Test that failed updates don't affect successful ones (transaction isolation)"""
    # Create two valid grievances
    valid_ids = []
    for i in range(2):
        payload = {
            "is_anonymous": True,
            "category_type": "Test",
            "details": f"Valid grievance {i}"
        }
        response = client.post("/api/grievances/", json=payload)
        assert response.status_code == 201
        valid_ids.append(response.json()["id"])
    
    # Mix valid and invalid updates
    batch_payload = {
        "updates": [
            {
                "gid": valid_ids[0],
                "external_status": "Success 1"
            },
            {
                "gid": "GRV-99999999999999999999999999",  # Invalid
                "external_status": "Should Fail"
            },
            {
                "gid": valid_ids[1],
                "external_status": "Success 2"
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    
    # First should succeed
    assert data["results"][0]["ok"] is True
    assert data["results"][0]["gid"] == valid_ids[0]
    
    # Second should fail
    assert data["results"][1]["ok"] is False
    assert "not found" in data["results"][1]["error"].lower()
    
    # Third should succeed
    assert data["results"][2]["ok"] is True
    assert data["results"][2]["gid"] == valid_ids[1]
    
    # Verify both valid updates persisted despite middle failure
    for idx, valid_id in enumerate(valid_ids):
        get_response = client.get(f"/api/grievances/{valid_id}")
        grievance = get_response.json()
        assert grievance["external_status"] == f"Success {idx + 1}"


def test_batch_update_empty_string_values(client):
    """Test batch update with empty string values (should update to empty)"""
    # Create a grievance with values
    payload = {
        "is_anonymous": True,
        "category_type": "Original Category",
        "details": "Test grievance",
        "island": "Tarawa",
        "hh_id": "HH123"
    }
    response = client.post("/api/grievances/", json=payload)
    grievance_id = response.json()["id"]
    
    # Update with empty strings (clearing values)
    batch_payload = {
        "updates": [
            {
                "gid": grievance_id,
                "external_status": "",
                "external_status_note": "",
                "hh_id": ""
            }
        ]
    }
    
    response = client.put("/api/grievances/status-batch", json=batch_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["results"][0]["ok"] is True
    
    # Verify empty strings were set
    get_response = client.get(f"/api/grievances/{grievance_id}")
    grievance = get_response.json()
    assert grievance["external_status"] == ""
    assert grievance["external_status_note"] == ""
    assert grievance["hh_id"] == ""

