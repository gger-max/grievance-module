def test_read_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["service"] == "Grievance Management API"
