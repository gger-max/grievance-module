# Email Notifications for Grievances

## Overview

The grievance system automatically sends confirmation emails to complainants when they submit non-anonymous grievances with a valid email address.

## Features

- **Automatic Email Sending**: Emails are sent automatically when a non-anonymous grievance is created with a valid email address
- **Graceful Failure Handling**: If email sending fails, the grievance is still created successfully
- **MailHog Integration**: Configured to work with MailHog for testing in development
- **Customizable Templates**: Email content includes grievance ID and complainant name

## Configuration

Email settings are configured via environment variables in `backend/.env`:

```bash
SMTP_HOST=mailhog              # SMTP server hostname
SMTP_PORT=1025                 # SMTP server port
SMTP_USERNAME=                 # SMTP username (optional)
SMTP_PASSWORD=                 # SMTP password (optional)
SMTP_FROM_EMAIL=noreply@vakasosiale.gov.to  # From email address
SMTP_USE_TLS=false            # Whether to use TLS
```

## Email Content

The confirmation email includes:

- Personalized greeting (if name provided)
- Grievance tracking ID (e.g., `GRV-01K88MF7431X7NF9D4GHQN5742`)
- Instructions for tracking the grievance
- Contact information for Vaka Sosiale

## When Emails Are Sent

Emails are sent when **ALL** of the following conditions are met:

1. The grievance is **not anonymous** (`is_anonymous: false`)
2. A valid **email address** is provided (`complainant_email`)
3. The grievance is successfully created in the database

## When Emails Are NOT Sent

Emails are **not** sent in the following cases:

- Anonymous grievances (`is_anonymous: true`)
- No email address provided (`complainant_email` is `null` or empty)
- Email sending fails (grievance is still created)

## Testing with MailHog

MailHog is included in `docker-compose.yml` for testing email functionality:

1. **Start the stack**: `docker compose up -d`
2. **Access MailHog UI**: http://localhost:8025
3. **Submit a non-anonymous grievance** with an email address
4. **View the email** in MailHog's web interface

## Production Configuration

For production use, update the SMTP settings to use a real email service:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@vakasosiale.gov.to
SMTP_USE_TLS=true
```

## API Behavior

The `/api/grievances/` endpoint behavior:

```python
# Non-anonymous with email → Sends email
POST /api/grievances/
{
    "is_anonymous": false,
    "complainant_email": "user@example.com",
    "complainant_name": "John Doe",
    "grievance_details": "..."
}
# → Grievance created + Email sent

# Anonymous → No email
POST /api/grievances/
{
    "is_anonymous": true,
    "grievance_details": "..."
}
# → Grievance created, no email

# Non-anonymous without email → No email
POST /api/grievances/
{
    "is_anonymous": false,
    "complainant_name": "Jane Doe",
    "grievance_details": "..."
}
# → Grievance created, no email
```

## Testing

Run the email notification tests:

```bash
# Run all email tests
pytest tests/test_email_notifications.py -v

# Run specific test
pytest tests/test_email_notifications.py::test_email_sent_for_non_anonymous_grievance -v
```

## Implementation Details

- **Email Module**: `app/utils/email.py`
- **Integration**: `app/routers/grievances.py` (in `create_grievance` endpoint)
- **Tests**: `tests/test_email_notifications.py` (12 tests)

## Troubleshooting

### Email not sending in Docker

1. Verify MailHog is running: `docker compose ps | grep mailhog`
2. Check SMTP settings in `backend/.env`
3. View API logs: `docker compose logs api`

### Test emails in MailHog

- Access MailHog UI at http://localhost:8025
- All test emails are captured and displayed
- No actual emails are sent to real addresses

## Security Considerations

- Email sending failures are logged but don't expose sensitive information
- SMTP credentials should be stored securely (use secrets management in production)
- Email content doesn't include sensitive grievance details
- Email addresses are validated using Pydantic's `EmailStr` type
