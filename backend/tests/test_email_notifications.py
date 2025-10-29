"""
Tests for email notification functionality when grievances are submitted.
Specifically tests email sending when not anonymous.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.utils.email import send_grievance_confirmation_email, get_smtp_config


def test_email_sent_for_non_anonymous_grievance(client):
    """Test that email is sent when a non-anonymous grievance is created"""
    with patch("app.routers.grievances.send_grievance_confirmation_email") as mock_email:
        mock_email.return_value = True
        
        payload = {
            "is_anonymous": False,
            "complainant_name": "John Doe",
            "complainant_email": "john.doe@example.com",
            "complainant_phone": "+676123456",
            "grievance_details": "Test grievance for email notification"
        }
        
        response = client.post("/api/grievances/", json=payload)
        assert response.status_code == 201
        
        data = response.json()
        grievance_id = data["id"]
        
        # Verify email function was called with correct parameters
        mock_email.assert_called_once()
        call_args = mock_email.call_args
        assert call_args[1]["to_email"] == "john.doe@example.com"
        assert call_args[1]["grievance_id"] == grievance_id
        assert call_args[1]["complainant_name"] == "John Doe"


def test_no_email_sent_for_anonymous_grievance(client):
    """Test that no email is sent for anonymous grievances"""
    with patch("app.routers.grievances.send_grievance_confirmation_email") as mock_email:
        payload = {
            "is_anonymous": True,
            "grievance_details": "Anonymous grievance - no email should be sent"
        }
        
        response = client.post("/api/grievances/", json=payload)
        assert response.status_code == 201
        
        # Verify email function was NOT called
        mock_email.assert_not_called()


def test_no_email_sent_when_email_not_provided(client):
    """Test that no email is sent when complainant email is not provided"""
    with patch("app.routers.grievances.send_grievance_confirmation_email") as mock_email:
        payload = {
            "is_anonymous": False,
            "complainant_name": "Jane Smith",
            "complainant_email": None,  # No email provided
            "grievance_details": "Non-anonymous but no email"
        }
        
        response = client.post("/api/grievances/", json=payload)
        assert response.status_code == 201
        
        # Verify email function was NOT called
        mock_email.assert_not_called()


def test_send_grievance_confirmation_email_success():
    """Test successful email sending"""
    mock_smtp = MagicMock()
    
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        result = send_grievance_confirmation_email(
            to_email="test@example.com",
            grievance_id="GRV-01K88MF7431X7NF9D4GHQN5742",
            complainant_name="Test User",
            details="Test grievance details"
        )
        
        assert result is True
        mock_smtp.send_message.assert_called_once()


def test_send_grievance_confirmation_email_without_name():
    """Test email sending without complainant name"""
    mock_smtp = MagicMock()
    
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        result = send_grievance_confirmation_email(
            to_email="test@example.com",
            grievance_id="GRV-01K88MF7431X7NF9D4GHQN5742",
        )
        
        assert result is True
        mock_smtp.send_message.assert_called_once()


def test_send_grievance_confirmation_email_failure():
    """Test email sending failure handling"""
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp_class.side_effect = Exception("SMTP connection failed")
        
        result = send_grievance_confirmation_email(
            to_email="test@example.com",
            grievance_id="GRV-01K88MF7431X7NF9D4GHQN5742",
        )
        
        # Should return False on failure but not raise exception
        assert result is False


def test_get_smtp_config_defaults():
    """Test SMTP configuration with default values"""
    with patch.dict("os.environ", {}, clear=True):
        config = get_smtp_config()
        
        assert config["host"] == "localhost"
        assert config["port"] == 1025
        assert config["username"] == ""
        assert config["password"] == ""
        assert config["from_email"] == "noreply@grievance.local"
        assert config["use_tls"] is False


def test_get_smtp_config_from_env():
    """Test SMTP configuration from environment variables"""
    env_vars = {
        "SMTP_HOST": "smtp.example.com",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "user@example.com",
        "SMTP_PASSWORD": "secret123",
        "SMTP_FROM_EMAIL": "noreply@example.com",
        "SMTP_USE_TLS": "true",
    }
    
    with patch.dict("os.environ", env_vars):
        config = get_smtp_config()
        
        assert config["host"] == "smtp.example.com"
        assert config["port"] == 587
        assert config["username"] == "user@example.com"
        assert config["password"] == "secret123"
        assert config["from_email"] == "noreply@example.com"
        assert config["use_tls"] is True


def test_email_continues_after_failure(client):
    """Test that grievance creation succeeds even if email fails"""
    with patch("app.routers.grievances.send_grievance_confirmation_email") as mock_email:
        # Simulate email sending failure
        mock_email.return_value = False
        
        payload = {
            "is_anonymous": False,
            "complainant_name": "Alice Brown",
            "complainant_email": "alice@example.com",
            "grievance_details": "Test grievance with email failure"
        }
        
        response = client.post("/api/grievances/", json=payload)
        
        # Grievance should still be created successfully
        assert response.status_code == 201
        data = response.json()
        assert data["complainant_email"] == "alice@example.com"
        
        # Verify email function was called
        mock_email.assert_called_once()


def test_email_content_includes_grievance_id():
    """Test that email content includes the grievance ID"""
    mock_smtp = MagicMock()
    grievance_id = "GRV-01K88MF7431X7NF9D4GHQN5742"
    
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        send_grievance_confirmation_email(
            to_email="test@example.com",
            grievance_id=grievance_id,
            complainant_name="Test User",
        )
        
        # Verify send_message was called
        assert mock_smtp.send_message.called
        
        # Get the message that was sent
        sent_message = mock_smtp.send_message.call_args[0][0]
        
        # Convert message to string to check content
        message_str = sent_message.as_string()
        
        # Verify grievance ID is in the email
        assert grievance_id in message_str
        assert "Grievance Confirmation" in message_str


def test_email_includes_complainant_name_in_greeting():
    """Test that email greeting includes complainant name when provided"""
    mock_smtp = MagicMock()
    
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        send_grievance_confirmation_email(
            to_email="test@example.com",
            grievance_id="GRV-01K88MF7431X7NF9D4GHQN5742",
            complainant_name="Jane Doe",
        )
        
        sent_message = mock_smtp.send_message.call_args[0][0]
        message_str = sent_message.as_string()
        
        # Verify name is in greeting
        assert "Dear Jane Doe" in message_str


def test_multiple_non_anonymous_submissions_send_separate_emails(client):
    """Test that multiple non-anonymous grievances each trigger separate emails"""
    with patch("app.routers.grievances.send_grievance_confirmation_email") as mock_email:
        mock_email.return_value = True
        
        # First grievance
        payload1 = {
            "is_anonymous": False,
            "complainant_name": "User One",
            "complainant_email": "user1@example.com",
            "grievance_details": "First grievance"
        }
        response1 = client.post("/api/grievances/", json=payload1)
        assert response1.status_code == 201
        
        # Second grievance
        payload2 = {
            "is_anonymous": False,
            "complainant_name": "User Two",
            "complainant_email": "user2@example.com",
            "grievance_details": "Second grievance"
        }
        response2 = client.post("/api/grievances/", json=payload2)
        assert response2.status_code == 201
        
        # Verify email was sent twice
        assert mock_email.call_count == 2
        
        # Verify different emails were sent
        first_call = mock_email.call_args_list[0]
        second_call = mock_email.call_args_list[1]
        
        assert first_call[1]["to_email"] == "user1@example.com"
        assert second_call[1]["to_email"] == "user2@example.com"
