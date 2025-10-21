# Grievance Management System.

Monorepo for the **Vaka Sosiale** GRM. It captures grievances via Typebot, processes and classifies them through a FastAPI middleware, stores data in PostgreSQL/MinIO, and integrates with Vaka Sosiale for analytics and feedback.<p align="center">

  <img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture Overview" width="720">

<p align="center"></p>

## Repository layout

grievance-module/# 

├── backend/              # FastAPI app, tests, Dockerfile# 
├── frontend-typebot/     # Typebot export, embed snippets, docs# ├─ .github/workflows/ # GitHub Actions
├── infra/                # docker-compose, .env.example, local run# ├─ .gitignore
├── ops/                  # CI/CD workflows and helper scripts# ├─ .gitattributes
├── docs/                 # report docs, images, diagrams# ├─ LICENSE
├── .github/workflows/    # GitHub Actions# ├─ README.md
├── .gitignore# └─ SECURITY.md
├── .gitattributes
├── LICENSE## Quick start (local)
├── README.md
└── SECURITY.md```bash

# 1) Start infra (DB/Redis/MinIO) + API + Typebot* (optional)

cd infra

## Quick Start (Local)cp .env.example .env

# edit values, then:

```bashdocker compose up -d

# 1) Create external Docker network for API-Typebot communication

docker network create grievance_net# 2) Visit:

# API docs:          http://localhost:8000/docs

# 2) Start all services (DB/Redis/MinIO/API/Typebot)# Typebot Builder*:  http://localhost:8081

docker compose up -d --build# Typebot Viewer*:   http://localhost:8082

# MinIO Console:     http://localhost:9001
# 3) Visit:
# API docs:          http://localhost:8000/docs
# Typebot Builder:   http://localhost:8081
# Typebot Viewer:    http://localhost:8082
# MinIO Console:     http://localhost:9001
# MailHog (email):   http://localhost:8025
```

## Architecture

### Services

- **FastAPI Backend** (`backend/`): REST API for grievance management
  - Endpoints: `/api/grievances`, `/api/status`
  - Features: CRUD operations, PDF receipt generation, attachment handling
  - Storage: PostgreSQL + MinIO (S3-compatible)
  - Tests: 41 passing tests (26 general + 15 Typebot integration)

- **Typebot** (`frontend-typebot/`): No-code chatbot for grievance intake
  - Builder (port 8081): Design and configure bot flows
  - Viewer (port 8082): Public-facing bot interface
  - Two export versions:
    - `typebot-export-grievance-intake-qwdn4no.json`: Production (server-side webhooks)
    - `typebot-export-grievance-intake-LOCALHOST-TEST.json`: Development (browser webhooks)

- **PostgreSQL**: Two databases
  - `grievance` (port 5432): Main grievance data
  - `typebot` (port 5433): Typebot configuration

- **MinIO** (ports 9000/9001): S3-compatible object storage for attachments

- **Redis** (port 6379): Caching and session storage

- **MailHog** (ports 1025/8025): Email testing (SMTP + web UI)

### Networking

The system uses two Docker networks:

1. **`default`** (auto-created): Internal service communication
2. **`grievance_net`** (external): Enables Typebot → API communication
   - API is accessible as `grievance-api:8000` from Typebot services

## Testing

### Run Backend Tests

```bash
# All tests (41 total)
docker exec grievancemodule-api-1 pytest

# Typebot integration tests only (15 tests)
docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py

# With coverage
docker exec grievancemodule-api-1 pytest --cov=app
```

### Test Typebot Integration

**Option 1: Published Bot (Recommended)**
1. Open Typebot Builder: http://localhost:8081
2. Import `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`
3. Click **"Publish"** (not "Test" - CSP restrictions apply to preview mode)
4. Access published bot URL
5. Submit a grievance - webhook executes server-side

**Option 2: Browser Testing**
1. Open `test-browser-webhook.html` in browser
2. Click "Test Webhook"
3. Simulates client-side webhook execution with CORS

### Test Coverage

**Typebot Integration Tests** (`test_typebot_integration.py`):
- ✅ Field mapping (Typebot → API schema)
- ✅ Complainant information handling
- ✅ Location data (island, district, village)
- ✅ Category types
- ✅ Attachment handling (single & multiple files)
- ✅ Anonymous submissions
- ✅ Named submissions with full details
- ✅ Household registration flow
- ✅ Status lookup by grievance ID
- ✅ PDF receipt generation
- ✅ Email notifications
- ✅ Error handling and validation

## Typebot Configuration

### Production Setup (Server-side webhooks)

File: `typebot-export-grievance-intake-qwdn4no.json`

```json
{
  "isExecutedOnClient": false,
  "webhook": {
    "url": "http://grievance-api:8000/api/grievances",
    "method": "POST",
    "headers": [{"key": "Content-Type", "value": "application/json"}]
  }
}
```

- Webhooks execute from Typebot Viewer container
- Uses Docker internal network (`grievance_net`)
- API accessible as `grievance-api:8000`

### Development Setup (Browser webhooks)

File: `typebot-export-grievance-intake-LOCALHOST-TEST.json`

```json
{
  "isExecutedOnClient": true,
  "webhook": {
    "url": "http://localhost:8000/api/grievances"
  }
}
```

- Webhooks execute in user's browser
- Requires CORS configuration (already configured)
- For testing in Typebot Builder environment

### CORS Configuration

The API uses custom CORS middleware to support:
- All origins including `null` (for `file://` protocol)
- Browser-based webhook execution
- Typebot client-side mode

```python
# backend/app/main.py
@app.middleware("http")
async def custom_cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "*")
    # Handles OPTIONS preflight and adds CORS headers to all responses
```

## API Endpoints

### Grievances

**Create Grievance**
```bash
POST /api/grievances
Content-Type: application/json

{
  "is_anonymous": true,
  "complainant_name": "John Doe",
  "complainant_email": "john@example.com",
  "complainant_phone": "+676123456",
  "complainant_gender": "Male",
  "is_hh_registered": false,
  "hh_id": "HH123",
  "hh_address": "Main Street",
  "island": "Tongatapu",
  "district": "Nuku'alofa",
  "village": "Kolofo'ou",
  "category_type": "Registration",
  "details": "Issue description...",
  "attachments": [
    {
      "name": "photo.jpg",
      "url": "https://...",
      "size": 1024,
      "type": "image/jpeg"
    }
  ]
}

Response: 201 Created
{
  "id": "GRV-01ABC123...",
  "created_at": "2025-10-21T12:00:00Z",
  ...
}
```

**Get Grievance**
```bash
GET /api/grievances/{id}
Response: 200 OK
```

**Download Receipt**
```bash
GET /api/grievances/{id}/receipt.pdf
Response: 200 OK (application/pdf)
```

**Update Status**
```bash
PATCH /api/grievances/{id}
{
  "external_status": "Under Review",
  "external_status_note": "Processing your request"
}
```

### Status

**Health Check**
```bash
GET /
Response: {"ok": true, "service": "Grievance Management API", "version": "0.1.0"}
```

**System Status**
```bash
GET /api/status
Response: {"status": "ok", "database": "connected", ...}
```

## Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + CORS middleware
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/
│   │   ├── grievances.py    # Grievance endpoints
│   │   └── status.py        # Status endpoints
│   └── utils/
│       ├── id.py            # ULID generator
│       └── pdf.py           # PDF receipt generation
├── tests/
│   ├── test_api.py          # 26 general API tests
│   └── test_typebot_integration.py  # 15 Typebot tests
├── Dockerfile
└── requirements.txt

frontend-typebot/
├── typebot-export-grievance-intake-qwdn4no.json         # Production
├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development
└── public/
    └── typebot-grievance-flow.html  # Embed example
```

### Environment Variables

**Backend** (`.env`):
```bash
DATABASE_URL=postgresql://grievance:grievance@db:5432/grievance
REDIS_URL=redis://redis:6379/0
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

**Typebot** (configured in `docker-compose.yml`):
- Database: `postgresql://typebot:typebot@typebot-db:5432/typebot`
- Encryption: `ENCRYPTION_SECRET` (required for webhooks)
- SMTP: MailHog on port 1025
- Storage: MinIO S3

### Key Features

**Attachment Handling**:
- Supports single or multiple files
- Validation: max 10MB per file, 25MB total, max 5 files
- Stores URLs from Typebot's S3 storage
- Converts Pydantic `AttachmentIn` objects or dicts

**ID Generation**:
- ULID format: `GRV-01ABC123...` (26 characters)
- Sortable, unique, URL-safe

**PDF Receipts**:
- Auto-generated with grievance details
- Includes QR code for tracking
- Downloadable via `/api/grievances/{id}/receipt.pdf`

**Anti-Spam**:
- Honeypot field
- Timing validation (min 3 seconds)
- Math challenge for suspicious submissions

## Troubleshooting

### Typebot "Test" Button Error

**Symptom**: "Error! Could not reach server" when clicking Test button

**Cause**: Content Security Policy (CSP) blocks `http://` in preview mode

**Solution**: Use **"Publish"** button instead:
1. Click "Publish" (not "Test")
2. Access bot via public URL
3. Webhooks work correctly in published mode

### CORS Errors

**Symptom**: "No 'Access-Control-Allow-Origin' header"

**Status**: ✅ Fixed - Custom CORS middleware accepts all origins

**Details**: 
- Handles `null` origin (file:// protocol)
- Supports OPTIONS preflight requests
- Works with both server-side and client-side webhooks

### Network Connectivity

**Symptom**: Typebot can't reach API

**Solution**: Ensure `grievance_net` network exists:
```bash
docker network create grievance_net
docker compose up -d
```

**Verify**:
```bash
docker network inspect grievance_net
# Should show: api, typebot-builder, typebot-viewer
```

### Database Issues

**Reset databases**:
```bash
docker compose down -v  # Warning: deletes all data
docker compose up -d
```

**Access PostgreSQL**:
```bash
# Grievance DB
docker exec -it grievancemodule-db-1 psql -U grievance -d grievance

# Typebot DB
docker exec -it grievancemodule-typebot-db-1 psql -U typebot -d typebot
```

## Production Deployment

### Prerequisites

1. Set up HTTPS (required for Typebot)
2. Configure domain names
3. Update environment variables
4. Set strong secrets

### Configuration

**Environment Variables**:
```bash
# API
DATABASE_URL=postgresql://user:pass@db-host:5432/grievance
MINIO_ENDPOINT=s3.example.com

# Typebot
NEXTAUTH_URL=https://builder.example.com
NEXT_PUBLIC_VIEWER_URL=https://bot.example.com
ENCRYPTION_SECRET=<64-char-random-string>
ADMIN_EMAIL=admin@example.com
DISABLE_SIGNUP=true

# SMTP (real email service)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=<api-key>
```

**Security**:
- [ ] Change default passwords
- [ ] Enable SSL/TLS for PostgreSQL
- [ ] Configure proper SMTP credentials
- [ ] Set up backup strategy
- [ ] Enable API rate limiting
- [ ] Configure firewall rules

### Monitoring

**Health Checks**:
```bash
# API
curl https://api.example.com/

# Typebot
curl https://bot.example.com/
```

**Logs**:
```bash
docker compose logs -f api
docker compose logs -f typebot-viewer
```

## License

See `LICENSE` file for details.

## Contributing

1. Run tests before submitting PRs
2. Follow existing code style
3. Update tests for new features
4. Document API changes
