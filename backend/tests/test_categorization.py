"""
Tests for LLM-based grievance categorization.

This module tests the categorization service and API endpoint with mocked
OpenAI responses to ensure proper functionality without making real API calls.
"""

import pytest
from unittest.mock import patch, MagicMock
import json
from openai import OpenAIError


def test_categorize_endpoint_registration_issue(client):
    """Test categorization endpoint with a registration-related grievance"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "2",
        "subcategory": "2.3",
        "confidence": "high",
        "reasoning": "The grievance mentions a household member not being registered."
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "My son was not included in the household registration even though he lives with us."
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["category"] == "2"
        assert data["subcategory"] == "2.3"
        assert data["category_name"] == "Registration related"
        assert data["subcategory_name"] == "HH member not registered"
        assert data["confidence"] == "high"
        assert "reasoning" in data
        assert "display" in data


def test_categorize_endpoint_staff_performance(client):
    """Test categorization endpoint with a staff performance issue"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "5",
        "subcategory": "5.3",
        "confidence": "high",
        "reasoning": "The grievance describes discourteous behavior from staff."
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "The staff member was very rude and did not help me with my inquiry."
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["category"] == "5"
        assert data["subcategory"] == "5.3"
        assert data["category_name"] == "Staff performance"
        assert data["subcategory_name"] == "Discourtesy or poor service"


def test_categorize_endpoint_inquiry(client):
    """Test categorization endpoint with a simple inquiry"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "1",
        "subcategory": "1.1",
        "confidence": "high",
        "reasoning": "This is a general inquiry about the program."
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "What documents do I need to bring for registration?"
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["category"] == "1"
        assert data["subcategory"] == "1.1"
        assert data["category_name"] == "Inquiries and suggestions"


def test_categorize_endpoint_others_category(client):
    """Test categorization endpoint defaulting to Others category"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "7",
        "subcategory": None,
        "confidence": "medium",
        "reasoning": "This grievance does not fit neatly into other categories."
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "I have a unique situation that doesn't fit standard categories."
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["category"] == "7"
        assert data["subcategory"] is None
        assert data["category_name"] == "Others (please describe)"
        assert data["subcategory_name"] is None


def test_categorize_endpoint_empty_details(client):
    """Test that empty details return a 422 validation error"""
    payload = {"details": ""}
    
    response = client.post("/api/grievances/categorize/", json=payload)
    assert response.status_code == 422  # Pydantic validation error


def test_categorize_endpoint_missing_details(client):
    """Test that missing details return a 422 validation error"""
    payload = {}
    
    response = client.post("/api/grievances/categorize/", json=payload)
    assert response.status_code == 422  # Pydantic validation error


def test_categorize_endpoint_openai_error(client):
    """Test graceful handling of OpenAI API errors"""
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = OpenAIError("API error")
        
        payload = {
            "details": "This should trigger an error"
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 500
        assert "LLM service error" in response.json()["detail"]


def test_categorize_endpoint_missing_api_key(client):
    """Test that missing OPENAI_API_KEY is handled properly"""
    with patch('app.services.llm_categorizer.os.getenv', return_value=None):
        payload = {
            "details": "This should fail due to missing API key"
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 400
        assert "OPENAI_API_KEY" in response.json()["detail"]


def test_categorize_endpoint_invalid_json_response(client):
    """Test handling of invalid JSON from OpenAI"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Invalid JSON{{{}"
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "Some grievance details"
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        # Should fallback to category 7 (Others)
        data = response.json()
        assert data["category"] == "7"
        assert data["confidence"] == "low"


def test_categorize_endpoint_invalid_category_in_response(client):
    """Test handling of invalid category from OpenAI"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "99",  # Invalid category
        "subcategory": None,
        "confidence": "high",
        "reasoning": "Some reasoning"
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "Some grievance details"
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        # Should fallback to category 7 (Others)
        data = response.json()
        assert data["category"] == "7"


def test_categorize_endpoint_socioeconomic_issue(client):
    """Test categorization of socioeconomic/PMT classification issue"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "3",
        "subcategory": "3.1",
        "confidence": "high",
        "reasoning": "The grievance indicates that a poor/vulnerable household was excluded."
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "We are very poor and need assistance but were not included in the program."
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["category"] == "3"
        assert data["subcategory"] == "3.1"
        assert data["category_name"] == "Socioeconomic (PMT classification)"
        assert data["subcategory_name"] == "Poor/vulnerable excluded"


def test_categorize_endpoint_gender_based_violence(client):
    """Test categorization of gender-based violence issue"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "6",
        "subcategory": "6.2",
        "confidence": "high",
        "reasoning": "The grievance describes sexual harassment."
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "A staff member made inappropriate comments of a sexual nature."
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["category"] == "6"
        assert data["subcategory"] == "6.2"
        assert data["category_name"] == "Gender-based violence"
        assert data["subcategory_name"] == "Sexual harassment"


def test_get_category_display_helper():
    """Test the get_category_display helper function"""
    from app.services.llm_categorizer import get_category_display
    
    # Test with valid category and subcategory
    display = get_category_display("2", "2.3")
    assert display == "2.3 HH member not registered"
    
    # Test with valid category, no subcategory
    display = get_category_display("1", None)
    assert display == "1. Inquiries and suggestions"
    
    # Test with invalid category
    display = get_category_display("99", None)
    assert display == "7. Others (please describe)"
    
    # Test with category 7 (Others)
    display = get_category_display("7", None)
    assert display == "7. Others (please describe)"


def test_categorize_with_missing_subcategory_fills_first(client):
    """Test that missing subcategory gets filled with first available option"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "category": "2",
        "subcategory": None,  # Missing subcategory
        "confidence": "medium",
        "reasoning": "Registration related issue."
    })
    
    with patch('app.services.llm_categorizer.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_response
        
        payload = {
            "details": "I have a registration problem"
        }
        
        response = client.post("/api/grievances/categorize/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["category"] == "2"
        # Should default to first subcategory
        assert data["subcategory"] == "2.1"
        assert data["subcategory_name"] == "HH not registered - not informed"
