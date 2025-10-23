"""Email utility for sending notifications via SMTP."""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_smtp_config():
    """Get SMTP configuration from environment variables."""
    return {
        "host": os.getenv("SMTP_HOST", "localhost"),
        "port": int(os.getenv("SMTP_PORT", "1025")),
        "username": os.getenv("SMTP_USERNAME", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "from_email": os.getenv("SMTP_FROM_EMAIL", "noreply@grievance.local"),
        "use_tls": os.getenv("SMTP_USE_TLS", "false").lower() == "true",
    }


def send_grievance_confirmation_email(
    to_email: str,
    grievance_id: str,
    complainant_name: Optional[str] = None,
    details: Optional[str] = None,
) -> bool:
    """
    Send a confirmation email to the complainant after grievance submission.
    
    Args:
        to_email: Recipient email address
        grievance_id: The grievance tracking ID
        complainant_name: Optional name of the complainant
        details: Optional grievance details preview
    
    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        config = get_smtp_config()
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Grievance Confirmation - {grievance_id}"
        msg["From"] = config["from_email"]
        msg["To"] = to_email
        
        # Create email body
        greeting = f"Dear {complainant_name}," if complainant_name else "Dear Complainant,"
        
        text_body = f"""{greeting}

Thank you for submitting your grievance to Vaka Sosiale.

Your grievance has been received and assigned the tracking number:
{grievance_id}

You can use this tracking number to check the status of your grievance at any time.

We will review your submission and update you on the progress.

Best regards,
Vaka Sosiale Grievance Team
"""
        
        html_body = f"""
<html>
<body>
    <p>{greeting}</p>
    
    <p>Thank you for submitting your grievance to Vaka Sosiale.</p>
    
    <p>Your grievance has been received and assigned the tracking number:</p>
    <p><strong>{grievance_id}</strong></p>
    
    <p>You can use this tracking number to check the status of your grievance at any time.</p>
    
    <p>We will review your submission and update you on the progress.</p>
    
    <p>Best regards,<br>
    Vaka Sosiale Grievance Team</p>
</body>
</html>
"""
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(config["host"], config["port"]) as server:
            if config["use_tls"]:
                server.starttls()
            
            if config["username"] and config["password"]:
                server.login(config["username"], config["password"])
            
            server.send_message(msg)
            logger.info(f"Confirmation email sent to {to_email} for grievance {grievance_id}")
            return True
            
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {to_email}: {str(e)}")
        return False
