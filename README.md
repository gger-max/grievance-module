<div align="center"># Grievance Management System.



# 🎯 Grievance Management SystemMonorepo for the **Vaka Sosiale** GRM. It captures grievances via Typebot, processes and classifies them through a FastAPI middleware, stores data in PostgreSQL/MinIO, and integrates with Vaka Sosiale for analytics and feedback.<p align="center">



### _Modern, scalable grievance tracking for Vaka Sosiale_  <img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture Overview" width="720">



[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)<p align="center"></p>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)## Repository layout

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)

[![Tests](https://img.shields.io/badge/Tests-41%20passing-success.svg?style=flat)](backend/tests/)grievance-module/# 



---├── backend/              # FastAPI app, tests, Dockerfile# 

├── frontend-typebot/     # Typebot export, embed snippets, docs# 

<img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture" width="800">├── infra/                # docker-compose, .env.example, local run# 

├── ops/                  # CI/CD workflows and helper scripts# 

**Capture grievances via Typebot chatbot** · **Process through FastAPI middleware** · **Store in PostgreSQL/MinIO** · **Integrate with analytics**├── docs/                 # report docs, images, diagrams# 

├── .github/workflows/    # GitHub Actions# 

[Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Docs](#-api-endpoints) • [Testing](#-testing) • [Deployment](#-production-deployment)├── .gitignore# 

├── .gitattributes

</div>├── LICENSE## Quick start (local)

├── README.md

---└── SECURITY.md



## 📋 Table of Contents```bash

# 1) Start infra (DB/Redis/MinIO) + API + Typebot* (optional)

- [Quick Start](#-quick-start)

- [Architecture](#-architecture)cd infra

- [Testing](#-testing)

- [API Endpoints](#-api-endpoints)## Quick Start (Local)cp .env.example .env

- [Typebot Configuration](#-typebot-configuration)

- [Development](#-development)# edit values, then:

- [Troubleshooting](#-troubleshooting)

- [Production Deployment](#-production-deployment)bashdocker compose up -d



---# 1) Create external Docker network for API-Typebot communication



## 🚀 Quick Startdocker network create grievance_net# 2) Visit:



Get up and running in 3 simple steps:# API docs:          http://localhost:8000/docs



```bash# 2) Start all services (DB/Redis/MinIO/API/Typebot)# Typebot Builder*:  http://localhost:8081

# Step 1: Create Docker network for service communication

docker network create grievance_netdocker compose up -d --build# Typebot Viewer*:   http://localhost:8082



# Step 2: Start all services# MinIO Console:     http://localhost:9001

docker compose up -d --build# 3) Visit:

# API docs:          http://localhost:8000/docs

# Step 3: Access the services# Typebot Builder:   http://localhost:8081

```# Typebot Viewer:    http://localhost:8082

# MinIO Console:     http://localhost:9001

### 🌐 Service URLs# MailHog (email):   http://localhost:8025

```

| Service | URL | Description |

|---------|-----|-------------|## Architecture

| 📚 **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |

| 🤖 **Typebot Builder** | http://localhost:8081 | Design bot flows |### Services

| 💬 **Typebot Viewer** | http://localhost:8082 | Public bot interface |

| 📦 **MinIO Console** | http://localhost:9001 | S3 storage management |- **FastAPI Backend** (`backend/`): REST API for grievance management

| 📧 **MailHog** | http://localhost:8025 | Email testing UI |  - Endpoints: `/api/grievances`, `/api/status`

  - Features: CRUD operations, PDF receipt generation, attachment handling

---  - Storage: PostgreSQL + MinIO (S3-compatible)

  - Tests: 41 passing tests (26 general + 15 Typebot integration)

## 🏗 Architecture

- **Typebot** (`frontend-typebot/`): No-code chatbot for grievance intake

### Service Overview  - Builder (port 8081): Design and configure bot flows

  - Viewer (port 8082): Public-facing bot interface

<table>  - Two export versions:

<tr>    - `typebot-export-grievance-intake-qwdn4no.json`: Production (server-side webhooks)

<td width="50%">    - `typebot-export-grievance-intake-LOCALHOST-TEST.json`: Development (browser webhooks)



#### 🔥 **FastAPI Backend**- **PostgreSQL**: Two databases

- **Location:** `backend/`  - `grievance` (port 5432): Main grievance data

- **Endpoints:** `/api/grievances`, `/api/status`  - `typebot` (port 5433): Typebot configuration

- **Features:**

  - ✅ CRUD operations- **MinIO** (ports 9000/9001): S3-compatible object storage for attachments

  - ✅ PDF receipt generation

  - ✅ File attachment handling- **Redis** (port 6379): Caching and session storage

  - ✅ Custom CORS middleware

- **Storage:** PostgreSQL + MinIO- **MailHog** (ports 1025/8025): Email testing (SMTP + web UI)

- **Tests:** 41 passing (26 general + 15 Typebot)

### Networking

</td>

<td width="50%">The system uses two Docker networks:



#### 🤖 **Typebot Chatbot**1. **`default`** (auto-created): Internal service communication

- **Location:** `frontend-typebot/`2. **`grievance_net`** (external): Enables Typebot → API communication

- **Ports:** 8081 (Builder), 8082 (Viewer)   - API is accessible as `grievance-api:8000` from Typebot services

- **Modes:**

  - 🔵 **Production:** Server-side webhooks## Testing

  - 🟢 **Development:** Browser webhooks

- **Features:**### Run Backend Tests

  - No-code bot designer

  - Webhook integration```bash

  - File upload support# All tests (41 total)

  - Multi-language supportdocker exec grievancemodule-api-1 pytest



</td># Typebot integration tests only (15 tests)

</tr>docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py

</table>

# With coverage

### 💾 Data Layerdocker exec grievancemodule-api-1 pytest --cov=app

```

| Service | Port | Purpose |

|---------|------|---------|### Test Typebot Integration

| **PostgreSQL** (grievance) | 5432 | Main grievance data |

| **PostgreSQL** (typebot) | 5433 | Typebot configuration |**Option 1: Published Bot (Recommended)**

| **MinIO** | 9000/9001 | S3-compatible file storage |1. Open Typebot Builder: http://localhost:8081

| **Redis** | 6379 | Caching & sessions |2. Import `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

| **MailHog** | 1025/8025 | Email testing (SMTP + UI) |3. Click **"Publish"** (not "Test" - CSP restrictions apply to preview mode)

4. Access published bot URL

### 🌐 Network Architecture5. Submit a grievance - webhook executes server-side



```mermaid**Option 2: Browser Testing**

graph LR1. Open `test-browser-webhook.html` in browser

    A[User Browser] -->|HTTP| B[Typebot Viewer]2. Click "Test Webhook"

    B -->|grievance_net| C[FastAPI]3. Simulates client-side webhook execution with CORS

    C -->|default| D[PostgreSQL]

    C -->|default| E[MinIO]### Test Coverage

    C -->|default| F[Redis]

    G[Typebot Builder] -->|grievance_net| C**Typebot Integration Tests** (`test_typebot_integration.py`):

```- ✅ Field mapping (Typebot → API schema)

- ✅ Complainant information handling

**Two Docker Networks:**- ✅ Location data (island, district, village)

- 🔵 **`default`** (auto-created): Internal service communication- ✅ Category types

- 🟢 **`grievance_net`** (external): Typebot ↔ API communication- ✅ Attachment handling (single & multiple files)

  - API accessible as `grievance-api:8000` from Typebot- ✅ Anonymous submissions

- ✅ Named submissions with full details

---- ✅ Household registration flow

- ✅ Status lookup by grievance ID

## 🧪 Testing- ✅ PDF receipt generation

- ✅ Email notifications

### Run Backend Tests- ✅ Error handling and validation



```bash## Typebot Configuration

# Run all 41 tests

docker exec grievancemodule-api-1 pytest### Production Setup (Server-side webhooks)



# Run Typebot integration tests only (15 tests)File: `typebot-export-grievance-intake-qwdn4no.json`

docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py -v

```json

# Run with coverage report{

docker exec grievancemodule-api-1 pytest --cov=app --cov-report=html  "isExecutedOnClient": false,

```  "webhook": {

    "url": "http://grievance-api:8000/api/grievances",

### 🤖 Test Typebot Integration    "method": "POST",

    "headers": [{"key": "Content-Type", "value": "application/json"}]

#### **Option 1: Published Bot** ⭐ _Recommended_  }

}

1. Open Typebot Builder: http://localhost:8081```

2. Import `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

3. Click **"Publish"** button (⚠️ don't use "Test" - CSP restrictions)- Webhooks execute from Typebot Viewer container

4. Access the published bot URL- Uses Docker internal network (`grievance_net`)

5. Submit a test grievance- API accessible as `grievance-api:8000`



#### **Option 2: Browser Testing**### Development Setup (Browser webhooks)



1. Open `test-browser-webhook.html` in your browserFile: `typebot-export-grievance-intake-LOCALHOST-TEST.json`

2. Click **"Test Webhook"** button

3. Verify successful creation```json

{

### ✅ Test Coverage  "isExecutedOnClient": true,

  "webhook": {

<details>    "url": "http://localhost:8000/api/grievances"

<summary><b>Typebot Integration Tests</b> (15 tests in <code>test_typebot_integration.py</code>)</summary>  }

}

#### Core Functionality```

- ✅ Field mapping (Typebot schema → API schema)

- ✅ Complainant information (name, email, phone, gender)- Webhooks execute in user's browser

- ✅ Location data (island, district, village)- Requires CORS configuration (already configured)

- ✅ Category types- For testing in Typebot Builder environment

- ✅ Grievance details and descriptions

### CORS Configuration

#### File Handling

- ✅ Single file attachmentThe API uses custom CORS middleware to support:

- ✅ Multiple file attachments- All origins including `null` (for `file://` protocol)

- ✅ Attachment validation- Browser-based webhook execution

- Typebot client-side mode

#### User Flows

- ✅ Anonymous submissions```python

- ✅ Named submissions with full details# backend/app/main.py

- ✅ Household registration flow@app.middleware("http")

- ✅ Status lookup by grievance IDasync def custom_cors_middleware(request: Request, call_next):

    origin = request.headers.get("origin", "*")

#### Features    # Handles OPTIONS preflight and adds CORS headers to all responses

- ✅ PDF receipt generation```

- ✅ Email notifications

- ✅ Error handling and validation## API Endpoints

- ✅ Anti-spam measures

### Grievances

</details>

**Create Grievance**

---```bash

POST /api/grievances

## 📡 API EndpointsContent-Type: application/json



### 📝 Grievances{

  "is_anonymous": true,

<details>  "complainant_name": "John Doe",

<summary><b>POST</b> <code>/api/grievances</code> - Create a new grievance</summary>  "complainant_email": "john@example.com",

  "complainant_phone": "+676123456",

```bash  "complainant_gender": "Male",

curl -X POST http://localhost:8000/api/grievances \  "is_hh_registered": false,

  -H "Content-Type: application/json" \  "hh_id": "HH123",

  -d '{  "hh_address": "Main Street",

    "is_anonymous": false,  "island": "Tongatapu",

    "complainant_name": "John Doe",  "district": "Nuku'alofa",

    "complainant_email": "john@example.com",  "village": "Kolofo'ou",

    "complainant_phone": "+676123456",  "category_type": "Registration",

    "complainant_gender": "Male",  "details": "Issue description...",

    "is_hh_registered": true,  "attachments": [

    "hh_id": "HH12345",    {

    "hh_address": "Main Street, Kolofo'\''ou",      "name": "photo.jpg",

    "island": "Tongatapu",      "url": "https://...",

    "district": "Nuku'\''alofa",      "size": 1024,

    "village": "Kolofo'\''ou",      "type": "image/jpeg"

    "category_type": "Registration",    }

    "details": "Need assistance with registration renewal",  ]

    "attachments": [}

      {

        "name": "document.pdf",Response: 201 Created

        "url": "https://storage.example.com/file.pdf",{

        "size": 102400,  "id": "GRV-01ABC123...",

        "type": "application/pdf"  "created_at": "2025-10-21T12:00:00Z",

      }  ...

    ]}

  }'```

```

**Get Grievance**

**Response:** `201 Created````bash

```jsonGET /api/grievances/{id}

{Response: 200 OK

  "id": "GRV-01K83WMY346N2S1KA7FK3W26RP",```

  "created_at": "2025-10-21T12:00:00Z",

  "updated_at": "2025-10-21T12:00:00Z",**Download Receipt**

  "is_anonymous": false,```bash

  "complainant_name": "John Doe",GET /api/grievances/{id}/receipt.pdf

  ...Response: 200 OK (application/pdf)

}```

```

**Update Status**

</details>```bash

PATCH /api/grievances/{id}

<details>{

<summary><b>GET</b> <code>/api/grievances/{id}</code> - Get grievance details</summary>  "external_status": "Under Review",

  "external_status_note": "Processing your request"

```bash}

curl http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP```

```

### Status

**Response:** `200 OK`

**Health Check**

</details>```bash

GET /

<details>Response: {"ok": true, "service": "Grievance Management API", "version": "0.1.0"}

<summary><b>GET</b> <code>/api/grievances/{id}/receipt.pdf</code> - Download PDF receipt</summary>```



```bash**System Status**

curl -O http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP/receipt.pdf```bash

```GET /api/status

Response: {"status": "ok", "database": "connected", ...}

**Response:** `200 OK` (PDF file)```



</details>## Development



<details>### Project Structure

<summary><b>PATCH</b> <code>/api/grievances/{id}</code> - Update status</summary>

```

```bashbackend/

curl -X PATCH http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP \├── app/

  -H "Content-Type: application/json" \│   ├── __init__.py

  -d '{│   ├── main.py              # FastAPI app + CORS middleware

    "external_status": "Under Review",│   ├── database.py          # SQLAlchemy setup

    "external_status_note": "Processing your request"│   ├── models.py            # Database models

  }'│   ├── schemas.py           # Pydantic schemas

```│   ├── routers/

│   │   ├── grievances.py    # Grievance endpoints

</details>│   │   └── status.py        # Status endpoints

│   └── utils/

### 🏥 Health & Status│       ├── id.py            # ULID generator

│       └── pdf.py           # PDF receipt generation

| Endpoint | Method | Description |├── tests/

|----------|--------|-------------|│   ├── test_api.py          # 26 general API tests

| `/` | GET | Health check |│   └── test_typebot_integration.py  # 15 Typebot tests

| `/api/status` | GET | System status |├── Dockerfile

└── requirements.txt

---

frontend-typebot/

## 🤖 Typebot Configuration├── typebot-export-grievance-intake-qwdn4no.json         # Production

├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development

### 🔵 Production Setup (Server-side webhooks)└── public/

    └── typebot-grievance-flow.html  # Embed example

**File:** `typebot-export-grievance-intake-qwdn4no.json````



```json### Environment Variables

{

  "isExecutedOnClient": false,**Backend** (`.env`):

  "webhook": {```bash

    "url": "http://grievance-api:8000/api/grievances",DATABASE_URL=postgresql://grievance:grievance@db:5432/grievance

    "method": "POST",REDIS_URL=redis://redis:6379/0

    "headers": [MINIO_ENDPOINT=minio:9000

      {"key": "Content-Type", "value": "application/json"}MINIO_ACCESS_KEY=minioadmin

    ]MINIO_SECRET_KEY=minioadmin

  }```

}

```**Typebot** (configured in `docker-compose.yml`):

- Database: `postgresql://typebot:typebot@typebot-db:5432/typebot`

✅ **Use this for:**- Encryption: `ENCRYPTION_SECRET` (required for webhooks)

- Production deployments- SMTP: MailHog on port 1025

- Published bots- Storage: MinIO S3

- Server-side execution (more secure)

### Key Features

### 🟢 Development Setup (Browser webhooks)

**Attachment Handling**:

**File:** `typebot-export-grievance-intake-LOCALHOST-TEST.json`- Supports single or multiple files

- Validation: max 10MB per file, 25MB total, max 5 files

```json- Stores URLs from Typebot's S3 storage

{- Converts Pydantic `AttachmentIn` objects or dicts

  "isExecutedOnClient": true,

  "webhook": {**ID Generation**:

    "url": "http://localhost:8000/api/grievances"- ULID format: `GRV-01ABC123...` (26 characters)

  }- Sortable, unique, URL-safe

}

```**PDF Receipts**:

- Auto-generated with grievance details

✅ **Use this for:**- Includes QR code for tracking

- Local development- Downloadable via `/api/grievances/{id}/receipt.pdf`

- Browser testing

- Debugging webhook payloads**Anti-Spam**:

- Honeypot field

### 🛡 CORS Configuration- Timing validation (min 3 seconds)

- Math challenge for suspicious submissions

Custom middleware automatically handles:

- ✅ All origins including `null` (file:// protocol)## Troubleshooting

- ✅ OPTIONS preflight requests

- ✅ Browser-based webhook execution### Typebot "Test" Button Error

- ✅ Typebot client-side mode

**Symptom**: "Error! Could not reach server" when clicking Test button

```python

# Middleware in backend/app/main.py**Cause**: Content Security Policy (CSP) blocks `http://` in preview mode

@app.middleware("http")

async def custom_cors_middleware(request: Request, call_next):**Solution**: Use **"Publish"** button instead:

    origin = request.headers.get("origin", "*")1. Click "Publish" (not "Test")

    # Automatically adds appropriate CORS headers2. Access bot via public URL

```3. Webhooks work correctly in published mode



---### CORS Errors



## 💻 Development**Symptom**: "No 'Access-Control-Allow-Origin' header"



### 📁 Project Structure**Status**: ✅ Fixed - Custom CORS middleware accepts all origins



```**Details**: 

grievance-module/- Handles `null` origin (file:// protocol)

│- Supports OPTIONS preflight requests

├── 📂 backend/- Works with both server-side and client-side webhooks

│   ├── 📂 app/

│   │   ├── main.py              # FastAPI app + CORS middleware### Network Connectivity

│   │   ├── database.py          # SQLAlchemy configuration

│   │   ├── models.py            # Database ORM models**Symptom**: Typebot can't reach API

│   │   ├── schemas.py           # Pydantic validation schemas

│   │   ├── 📂 routers/**Solution**: Ensure `grievance_net` network exists:

│   │   │   ├── grievances.py    # Grievance CRUD endpoints```bash

│   │   │   └── status.py        # System status endpointsdocker network create grievance_net

│   │   └── 📂 utils/docker compose up -d

│   │       ├── id.py            # ULID generator (GRV-01ABC...)```

│   │       └── pdf.py           # PDF receipt generator

│   ├── 📂 tests/**Verify**:

│   │   ├── test_api.py                    # 26 general API tests```bash

│   │   └── test_typebot_integration.py    # 15 Typebot testsdocker network inspect grievance_net

│   ├── Dockerfile# Should show: api, typebot-builder, typebot-viewer

│   └── requirements.txt```

│

├── 📂 frontend-typebot/### Database Issues

│   ├── typebot-export-grievance-intake-qwdn4no.json         # Production

│   ├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development**Reset databases**:

│   └── 📂 public/```bash

│       └── typebot-grievance-flow.html    # Embed exampledocker compose down -v  # Warning: deletes all data

│docker compose up -d

├── 📂 docs/                      # Documentation & diagrams```

├── 📂 ops/                       # CI/CD workflows

├── docker-compose.yml            # Service orchestration**Access PostgreSQL**:

└── README.md                     # You are here!```bash

```# Grievance DB

docker exec -it grievancemodule-db-1 psql -U grievance -d grievance

### 🔧 Environment Variables

# Typebot DB

<details>docker exec -it grievancemodule-typebot-db-1 psql -U typebot -d typebot

<summary><b>Backend Configuration</b> (<code>.env</code>)</summary>```



```bash## Production Deployment

# Database

DATABASE_URL=postgresql://grievance:grievance@db:5432/grievance### Prerequisites



# Cache1. Set up HTTPS (required for Typebot)

REDIS_URL=redis://redis:6379/02. Configure domain names

3. Update environment variables

# Object Storage4. Set strong secrets

MINIO_ENDPOINT=minio:9000

MINIO_ACCESS_KEY=minioadmin### Configuration

MINIO_SECRET_KEY=minioadmin

MINIO_BUCKET=grievances**Environment Variables**:

```bash

# API# API

DEBUG=TrueDATABASE_URL=postgresql://user:pass@db-host:5432/grievance

API_VERSION=0.1.0MINIO_ENDPOINT=s3.example.com

```

# Typebot

</details>NEXTAUTH_URL=https://builder.example.com

NEXT_PUBLIC_VIEWER_URL=https://bot.example.com

<details>ENCRYPTION_SECRET=<64-char-random-string>

<summary><b>Typebot Configuration</b> (in <code>docker-compose.yml</code>)</summary>ADMIN_EMAIL=admin@example.com

DISABLE_SIGNUP=true

```yaml

# Core Settings# SMTP (real email service)

DATABASE_URL: postgresql://typebot:typebot@typebot-db:5432/typebotSMTP_HOST=smtp.sendgrid.net

ENCRYPTION_SECRET: <64-character-random-string>SMTP_PORT=587

NEXTAUTH_URL: http://localhost:8081SMTP_USERNAME=apikey

NEXT_PUBLIC_VIEWER_URL: http://localhost:8082SMTP_PASSWORD=<api-key>

```

# Email (MailHog for testing)

SMTP_HOST: mailhog**Security**:

SMTP_PORT: 1025- [ ] Change default passwords

SMTP_USERNAME: x- [ ] Enable SSL/TLS for PostgreSQL

SMTP_PASSWORD: x- [ ] Configure proper SMTP credentials

NEXT_PUBLIC_SMTP_FROM: noreply@typebot.local- [ ] Set up backup strategy

- [ ] Enable API rate limiting

# Storage (MinIO)- [ ] Configure firewall rules

S3_ACCESS_KEY: minioadmin

S3_SECRET_KEY: minioadmin### Monitoring

S3_BUCKET: typebot

S3_ENDPOINT: minio**Health Checks**:

S3_PORT: 9000```bash

NEXT_PUBLIC_S3_ENDPOINT: http://localhost:9000# API

```curl https://api.example.com/



</details># Typebot

curl https://bot.example.com/

### ✨ Key Features```



#### 📎 Attachment Handling**Logs**:

- Multiple file uploads (max 5 files)```bash

- Size validation (10MB per file, 25MB total)docker compose logs -f api

- Supported formats: `.jpg`, `.png`, `.pdf`, `.docx`, `.xlsx`docker compose logs -f typebot-viewer

- Stores URLs from MinIO S3 storage```

- Handles both Pydantic objects and raw dicts

## License

#### 🆔 ID Generation

- **Format:** `GRV-01ABC123...` (26 characters)See `LICENSE` file for details.

- **Technology:** ULID (Universally Unique Lexicographically Sortable Identifier)

- **Benefits:** Sortable, unique, URL-safe, timestamp-embedded## Contributing



#### 📄 PDF Receipt Generation1. Run tests before submitting PRs

- Auto-generated with grievance details2. Follow existing code style

- Includes QR code for easy tracking3. Update tests for new features

- Professional formatting4. Document API changes

- Downloadable via `/api/grievances/{id}/receipt.pdf`

#### 🛡 Anti-Spam Protection
- 🍯 Honeypot field (invisible to humans)
- ⏱️ Timing validation (minimum 3 seconds)
- 🧮 Math challenge for suspicious submissions
- 🚫 Rate limiting (configurable)

---

## 🔧 Troubleshooting

### ⚠️ Typebot "Test" Button Error

<table>
<tr>
<td width="30%"><b>Symptom</b></td>
<td><code>Error! Could not reach server. Check your connection. {}</code></td>
</tr>
<tr>
<td><b>Cause</b></td>
<td>Content Security Policy (CSP) blocks HTTP in preview mode</td>
</tr>
<tr>
<td><b>Solution</b></td>
<td>
✅ Use <b>"Publish"</b> button instead of "Test"<br>
1. Click "Publish" in Typebot Builder<br>
2. Access bot via the public URL<br>
3. Webhooks work correctly in published mode
</td>
</tr>
</table>

### ✅ CORS Errors (FIXED)

**Status:** ✅ **Resolved** - Custom CORS middleware accepts all origins

- ✅ Handles `null` origin (file:// protocol)
- ✅ Supports OPTIONS preflight requests
- ✅ Works with server-side and client-side webhooks

### 🌐 Network Connectivity Issues

**Problem:** Typebot can't reach API

```bash
# Solution: Ensure grievance_net network exists
docker network create grievance_net
docker compose up -d

# Verify network configuration
docker network inspect grievance_net
# Should show: api, typebot-builder, typebot-viewer
```

### 🗄 Database Issues

<details>
<summary><b>Reset all data</b> (⚠️ destructive)</summary>

```bash
docker compose down -v  # Removes all volumes
docker compose up -d --build
```

</details>

<details>
<summary><b>Access PostgreSQL</b></summary>

```bash
# Grievance database
docker exec -it grievancemodule-db-1 psql -U grievance -d grievance

# Typebot database
docker exec -it grievancemodule-typebot-db-1 psql -U typebot -d typebot
```

</details>

<details>
<summary><b>Check service logs</b></summary>

```bash
# API logs
docker compose logs -f api

# Typebot Viewer logs
docker compose logs -f typebot-viewer

# All services
docker compose logs -f
```

</details>

---

## 🚀 Production Deployment

### ✅ Prerequisites Checklist

- [ ] Set up HTTPS/SSL certificates (required for Typebot)
- [ ] Configure domain names (e.g., api.example.com, bot.example.com)
- [ ] Set up managed PostgreSQL database
- [ ] Configure S3-compatible storage (AWS S3, DigitalOcean Spaces, etc.)
- [ ] Set up email service (SendGrid, AWS SES, etc.)
- [ ] Generate strong secrets and passwords
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting

### ⚙️ Production Configuration

<details>
<summary><b>Environment Variables</b></summary>

```bash
# API
DATABASE_URL=postgresql://user:strongpass@db-host:5432/grievance
REDIS_URL=redis://redis-host:6379/0
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=<aws-access-key>
MINIO_SECRET_KEY=<aws-secret-key>
DEBUG=False

# Typebot
NEXTAUTH_URL=https://builder.example.com
NEXT_PUBLIC_VIEWER_URL=https://bot.example.com
ENCRYPTION_SECRET=<64-char-random-string>
ADMIN_EMAIL=admin@example.com
DISABLE_SIGNUP=true

# SMTP (Real email service)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=<sendgrid-api-key>
SMTP_SECURE=true
```

</details>

### 🔒 Security Checklist

- [ ] Change all default passwords
- [ ] Enable SSL/TLS for PostgreSQL connections
- [ ] Configure proper SMTP credentials
- [ ] Set up automated database backups
- [ ] Enable API rate limiting
- [ ] Configure firewall rules (allow only necessary ports)
- [ ] Set up SSL certificates for all domains
- [ ] Enable HTTPS redirect
- [ ] Configure CORS for specific domains only
- [ ] Review and update security headers

### 📊 Monitoring

#### Health Checks

```bash
# API health
curl https://api.example.com/
# Expected: {"ok": true, "service": "Grievance Management API", "version": "0.1.0"}

# Typebot health
curl https://bot.example.com/
# Expected: 200 OK
```

#### Logging

```bash
# Production logs
docker compose -f docker-compose.prod.yml logs -f --tail=100 api

# Error monitoring
docker compose logs api | grep ERROR

# Access logs
docker compose logs api | grep POST
```

### 📈 Performance Optimization

- Enable database connection pooling
- Configure Redis caching
- Set up CDN for static assets
- Enable gzip compression
- Implement pagination for large datasets
- Add database indexes for frequently queried fields

---

## 📄 License

See [`LICENSE`](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Run tests** before submitting PRs
   ```bash
   docker exec grievancemodule-api-1 pytest
   ```
2. **Follow existing code style** (PEP 8 for Python)
3. **Update tests** for new features
4. **Document API changes** in this README
5. **Add meaningful commit messages**

---

<div align="center">

### 🌟 Built with

FastAPI · PostgreSQL · Typebot · MinIO · Redis · Docker

**Made with ❤️ for Vaka Sosiale**

[Report Bug](https://github.com/gger-max/grievance-module/issues) · [Request Feature](https://github.com/gger-max/grievance-module/issues)

</div>
