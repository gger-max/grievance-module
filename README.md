<div align="center">

#  Grievance Management System

### _Modern, scalable grievance tracking for Vaka Sosiale_

<br>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/Tests-102%20passing-success.svg?style=flat)](backend/tests/)

<br>

<img src="docs/images/figure-10-grm-architecture.png" alt="GRM Architecture" width="750">

<br>

**Capture grievances via Typebot**  **Process through FastAPI**  **Store in PostgreSQL/MinIO**

<br>

[Quick Start](#-quick-start)  [Architecture](#-architecture)  [API](#-api-endpoints)  [Testing](#-testing)

</div>

---

##  Quick Start

```bash
docker network create grievance_net
docker compose up -d --build
```

| Service | URL |
|---------|-----|
|  API Docs | http://localhost:8000/docs |
|  Typebot | http://localhost:8081 |
|  MinIO | http://localhost:9001 |

##  Architecture

| Service | Port | Purpose |
|---------|------|---------|
| FastAPI | 8000 | REST API |
| Typebot | 8081/8082 | Chatbot |
| PostgreSQL | 5432/5433 | Databases |
| MinIO | 9000/9001 | File storage |
| Redis | 6379 | Cache |

**Features:** ULID-only IDs (`GRV-[A-Z0-9]{26}`)  Client-provided IDs  PDF Receipts  **Status Tracking**  Multi-file attachments  MinIO S3 storage  Custom CORS **LLM-based Categorization** **Gmail Email Notifications**

##  Testing

### Run All Tests
```bash
# Run complete test suite (102 tests)
docker compose exec api pytest tests/ -v

# Run specific test file
docker compose exec api pytest tests/test_grievances.py -v

# Run categorization tests
docker compose exec api pytest tests/test_categorization.py -v

# Run email notification tests
docker compose exec api pytest tests/test_email_notifications.py -v

# Run with coverage
docker compose exec api pytest tests/ --cov=app --cov-report=html
```

### Test Coverage (102 tests)
- ✅ **Grievance CRUD** (25 tests) - Create, read, update, delete operations
- ✅ **Email Notifications** (12 tests) - Confirmation emails for non-anonymous submissions
- ✅ **Client ID Handling** - ULID format validation (`GRV-[A-Z0-9]{26}`)
- ✅ **Typebot Integration** (16 tests) - Full chatbot flow, payload formats
- ✅ **Status API** (7 tests) - Authentication, authorization, updates
- ✅ **Batch Operations** (12 tests) - Bulk updates, error handling
- ✅ **Status Check Flow** (6 tests) - End-to-end status tracking from Typebot
- ✅ **LLM Categorization** (14 tests) - Auto-categorization, error handling, validation
- ✅ **Empty String Handling** (9 tests) - Typebot empty field compatibility
- ✅ **Main App** (1 test) - Health check endpoint

### Client-Provided ID Support
The API accepts **ULID-format IDs only**: `GRV-[A-Z0-9]{26}` (e.g., `GRV-01K88MF7431X7NF9D4GHQN5742`)

- IDs are generated client-side using ULID library in Typebot JavaScript
- If an invalid ID is provided, the server generates a new ULID automatically
- Ensures tracking ID displayed to user matches database ID

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/grievances/` | Create new grievance |
| POST | `/api/grievances/submit-simple` | Create grievance (simplified response) |
| GET | `/api/grievances/{id}` | **Check status** - Get grievance details |
| GET | `/api/grievances/{id}/receipt.pdf` | Download PDF receipt |
| PUT | `/api/grievances/{id}/status` | Update grievance status |
| GET | `/api/grievances/export` | Export recent grievances |
| PUT | `/api/grievances/status-batch` | Batch status updates |
| POST | `/api/grievances/categorize/` | **LLM-based categorization** |

##  LLM-based Categorization

The system uses OpenAI's GPT models to automatically categorize grievances based on complainant input. Categorization happens **automatically** when grievances are created, or can be called manually via the API endpoint.

### Automatic Categorization

Every grievance submitted **without** a `category_type` field will be automatically categorized using LLM:

1. **Submission**: User submits grievance through Typebot or API
2. **Auto-categorize**: System calls OpenAI API with grievance details
3. **Storage**: Grievance is saved with the suggested category (e.g., "5.3 Discourtesy or poor service")
4. **Graceful Failure**: If categorization fails (no API key, API error), grievance is still created without a category

```bash
# Example: Grievance submitted without category_type
POST /api/grievances/
{
  "details": "Staff was rude when I asked for help",
  "is_anonymous": true
}

# Result: Automatically categorized as "5.3 Discourtesy or poor service"
```

**Note:** If a `category_type` is provided in the request, automatic categorization is skipped.

### Manual Categorization Endpoint

You can also categorize text manually using the dedicated endpoint:

```bash
curl -X POST "http://localhost:8000/api/grievances/categorize/" \
  -H "Content-Type: application/json" \
  -d '{"details": "Staff was rude when I asked for help"}'
```

Response:
```json
{
  "category": "5",
  "subcategory": "5.3",
  "category_name": "Staff performance",
  "subcategory_name": "Discourtesy or poor service",
  "confidence": "high",
  "reasoning": "The grievance describes discourteous staff behavior.",
  "display": "5.3 Discourtesy or poor service"
}
```

### Configuration

Add your OpenAI API key to `backend/.env`:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini  # Optional, defaults to gpt-4o-mini
```

### Categories Supported

1. Inquiries and suggestions (1.1-1.2)
2. Registration related (2.1-2.4)
3. Socioeconomic/PMT classification (3.1-3.3)
4. Misbehavior of registrant (4.1-4.2)
5. Staff performance (5.1-5.4)
6. Gender-based violence (6.1-6.2)
7. Others

For detailed documentation, see [docs/LLM_CATEGORIZATION.md](docs/LLM_CATEGORIZATION.md).

##  Email Notifications

Automatic confirmation emails are sent via **Gmail SMTP** to complainants who submit non-anonymous grievances with a valid email address.

### Features
- 📧 **Gmail SMTP** integration for production email delivery
- 🔒 **Graceful failure handling** - grievance creation succeeds even if email fails
- ✉️ **Professional templates** with grievance tracking ID and PDF receipt
- 🎯 **Configurable** - supports Gmail app passwords or other SMTP providers

### Configuration
Set these environment variables in `docker-compose.yml`:
```yaml
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SMTP_USERNAME: your-email@gmail.com
SMTP_PASSWORD: your-app-password  # Gmail app password (no spaces)
SMTP_FROM_EMAIL: your-email@gmail.com
SMTP_FROM_NAME: "Grievance System"
```

**Note:** Gmail requires [app-specific passwords](https://support.google.com/accounts/answer/185833) when 2FA is enabled.

See [EMAIL_NOTIFICATIONS.md](backend/EMAIL_NOTIFICATIONS.md) for detailed configuration and testing.

##  PDF Receipts

Professional PDF receipts are automatically generated for each grievance submission. Recipients can download their receipt at any time using the tracking ID.

### Features
- 🖼️ **Branded header** with organization logo (Vaka Sosiale)
- 📊 **Table format** - Clean 2-column layout with bold labels and italic content
- 🕒 **Local timestamps** - User-friendly date/time format (e.g., "Thu Jan 30 2025 12:34:56")
- 👤 **Complainant information** - Name, email, phone, gender (for non-anonymous)
- 🏠 **Household details** - Household ID and landmark (when provided)
- 📎 **Attachment details** - File names and sizes in human-readable format (B/KB/MB)
- ✅ **Conditional rendering** - Only shows fields that have data

### Access Receipts
Download via API endpoint:
```bash
GET /api/grievances/{grievance_id}/receipt.pdf
```

Example:
```bash
curl -o receipt.pdf http://localhost:8000/api/grievances/GRV-01K88MF7431X7NF9D4GHQN5742/receipt.pdf
```

### PDF Layout
- **Logo**: Centered at top (50mm × 15mm)
- **Title**: "Grievance / Feedback Receipt" (center-aligned)
- **Information Table**: Two columns with grid borders
  - Column 1 (45mm): Labels in **bold** (e.g., "Grievance ID:", "Created at:")
  - Column 2 (125mm): Content in *italic* (e.g., ID value, timestamp)
- **Attachments Table**: Separate section if files are attached

### Technical Details
The PDF is generated on-demand using ReportLab library with proper text wrapping and responsive layout. Logo file is bundled in the Docker container at `backend/app/static/images/VAKA SOCIALE_final_NEW.png`.

##  Typebot Integration

### Configuration Files
- **Production:** `typebot-export-grievance-intake.json` (consolidated flow)
- **Authentication:** Gmail SMTP with magic link login
- **Environment:** `NEXT_PUBLIC_E2E_TEST=false` (enforces authentication)

### Features
- 🤖 **Chatbot interface** for user-friendly grievance submission
- 📎 **File attachments** - upload images, PDFs, documents (max 10MB)
- 🆔 **ULID generation** - client-side ID generation using JavaScript
- 🔐 **Anonymous & non-anonymous** submission flows
- 📧 **Email receipts** with PDF attachments for non-anonymous users
- 📊 **Status tracking** - users can check grievance status with tracking ID

### Status Check Feature

Users can check their grievance status at any time:

1. **Select "Check status?"** from the welcome menu
2. **Enter tracking ID** (e.g., `GRV-01K88MF7431X7NF9D4GHQN5742`)
3. **View status information**:
   - Current status (Pending, Under Review, Resolved, etc.)
   - Status notes from case workers
   - Location details (Island, District, Village)
   - Category type and submission date
   - Household ID (if applicable)

📖 **See [docs/STATUS_CHECK_FEATURE.md](docs/STATUS_CHECK_FEATURE.md) and [docs/TYPEBOT_ID_SOLUTION.md](docs/TYPEBOT_ID_SOLUTION.md) for detailed documentation**

### ID Generation Workflow
IDs are generated client-side using ULID to ensure tracking ID matches database ID:

1. **JavaScript ULID generation** in Typebot "Set variable" blocks
   ```javascript
   function ulid() { /* ULID implementation */ }
   return 'GRV-' + ulid();
   ```
2. ID stored in `grievance_id` variable
3. **Webhook** sends ID to API: `http://api:8000/api/grievances/` (Docker service name)
4. **API validates** ULID format: `^GRV-[A-Z0-9]{26}$`
5. **Confirmation** displays tracking ID: `{{grievance_id}}`
6. **Email receipt** includes PDF and tracking information

This ensures the displayed tracking ID matches the database ID for receipt downloads and status tracking. See [docs/TYPEBOT_ID_SOLUTION.md](docs/TYPEBOT_ID_SOLUTION.md) for implementation details.

##  Troubleshooting

| Issue | Solution |
|-------|----------|
| Typebot Auto-login | Ensure `NEXT_PUBLIC_E2E_TEST=false` in docker-compose.yml |
| Typebot Test Error | Use "Publish" not "Test" for webhook integration |
| Email Not Sending | Check Gmail app password (no spaces), verify SMTP settings |
| Webhook Failed | Use Docker service name `http://api:8000` not `localhost:8000` |
| File Upload Error | Check MinIO bucket exists and is accessible |
| CORS Errors | Fixed with custom middleware in FastAPI |
| Network Issues | `docker network create grievance_net` |
| ID Validation Error | Ensure ULID format: `GRV-[A-Z0-9]{26}` (26 characters) |
| Code Not Updating | Restart container: `docker compose restart api` |
| Tests Not Found | Tests are in container: `docker compose exec api pytest tests/` |
| Test File Not Updating | Use `docker cp` if tests folder not volume-mounted |

##  Development Setup

### Volume Mounts
For live code reloading during development, volume mounts are configured in `docker-compose.yml`:
```yaml
volumes:
  - ./backend/app:/app/app  # Live code reload
```

After code changes, restart the container to clear Python bytecode cache:
```bash
docker compose restart api
```

### Running Tests Locally
Tests use an in-memory SQLite database and don't require PostgreSQL:
```bash
cd backend
pytest tests/ -v
```

##  Deployment

### Production Checklist
- [ ] Remove development volume mounts from `docker-compose.yml`
- [ ] Set `NEXT_PUBLIC_E2E_TEST=false` for Typebot authentication
- [ ] Configure Gmail SMTP credentials (use app password)
- [ ] Set `NEXTAUTH_SECRET` for Typebot session encryption
- [ ] Set `ODOO_TOKEN` environment variable for status API
- [ ] Configure `ODOO_ALLOWED_IPS` for IP whitelisting
- [ ] Set `OPENAI_API_KEY` for LLM categorization feature
- [ ] Set `DATABASE_URL` to production PostgreSQL
- [ ] Configure MinIO S3 storage with production credentials
- [ ] Create `grievance-attachments` bucket in MinIO
- [ ] Enable HTTPS/TLS for all services
- [ ] Configure backup strategy for PostgreSQL and MinIO
- [ ] Set up monitoring and logging
- [ ] Update Typebot webhook URLs to production API endpoint
- [ ] Update Typebot configuration with production URLs

### Environment Variables Reference
```yaml
# API
DATABASE_URL: postgresql://user:pass@postgres:5432/grievance
OPENAI_API_KEY: sk-...
OPENAI_MODEL: gpt-4o-mini
ODOO_TOKEN: your-secret-token
ODOO_ALLOWED_IPS: 192.168.1.0/24,10.0.0.1

# Email
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SMTP_USERNAME: your-email@gmail.com
SMTP_PASSWORD: your-app-password
SMTP_FROM_EMAIL: your-email@gmail.com

# Typebot
NEXT_PUBLIC_E2E_TEST: false
NEXTAUTH_SECRET: your-secret-key
ENCRYPTION_SECRET: your-encryption-key
TYPEBOT_DATABASE_URL: postgresql://user:pass@postgres:5433/typebot

# MinIO
S3_ENDPOINT: minio:9000
S3_ACCESS_KEY: minioadmin
S3_SECRET_KEY: minioadmin
S3_BUCKET: grievance-attachments
```

See full docs for detailed production configuration and security guidelines.

---

<div align="center">

**Built with  for Vaka Sosiale**

FastAPI  PostgreSQL  Typebot  MinIO  Redis  Docker

</div>