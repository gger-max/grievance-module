<div align="center"><div align="center"><div align="center"># Grievance Management System.



# 🎯 Grievance Management System



### _Modern, scalable grievance tracking for Vaka Sosiale_#



<br>



### Grievance Management System Monorepo for the **Vaka Sosiale** GRM. It captures grievances via Typebot, processes and classifies them through a FastAPI middleware, stores data in PostgreSQL/MinIO, and integrates with Vaka Sosiale for analytics and feedback.<p align="center">

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)

[![Tests](https://img.shields.io/badge/Tests-41%20passing-success.svg?style=flat)](backend/tests/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)


<p align="center"><img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture Overview" width="720">
</p>

</div>


## 📋 Table of Contents<br>

- [🚀 Quick Start](#-quick-start)

- [🏗 Architecture](#-architecture)

- [🧪 Testing](#-testing)

- [📡 API Endpoints](#-api-endpoints)

- [🤖 Typebot Configuration](#-typebot-configuration)

- [💻 Development](#-development)

- [🔧 Troubleshooting](#-troubleshooting) 

- [🚀 Production Deployment](#-production-deployment)

---

## 🚀 Quick Start


Get up and running in 3 simple steps:

</div>
```bash

# Step 1: Create Docker network for service communication

docker network create grievance_net

# Step 2: Start all services

docker compose up -d --build

# Step 3: Access the services ✨## 📋 Table of Contents<img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture" width="800">├── infra/                # docker-compose, .env.example, local run# 

```
### 🌐 Service URLs

- [🚀 Quick Start](#-quick-start)├── ops/                  # CI/CD workflows and helper scripts# 

| Service | URL | Description |

|---------|-----|-------------|- [🏗 Architecture](#-architecture)

| 📚 **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |

| 🤖 **Typebot Builder** | http://localhost:8081 | Design bot flows |- [🧪 Testing](#-testing)

| 💬 **Typebot Viewer** | http://localhost:8082 | Public bot interface |

| 📦 **MinIO Console** | http://localhost:9001 | S3 storage management |- [📡 API Endpoints](#-api-endpoints)

| 📧 **MailHog** | http://localhost:8025 | Email testing UI |

- [🤖 Typebot Configuration](#-typebot-configuration)├── .github/workflows/    # GitHub Actions# 

---

- [💻 Development](#-development)

## 🏗 Architecture

- [🔧 Troubleshooting](#-troubleshooting)[Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Docs](#-api-endpoints) • [Testing](#-testing) • [Deployment](#-production-deployment)├── .gitignore# 

### Service Overview

- [🚀 Production Deployment](#-production-deployment)

<table>

<tr>├── .gitattributes

<td width="50%" valign="top">

---

#### 🔥 **FastAPI Backend**

</div>├── LICENSE## Quick start (local)

**Location:** `backend/`

## 🚀 Quick Start

**Endpoints:** 

- `/api/grievances` - CRUD operations├── README.md

- `/api/status` - System health

Get up and running in 3 simple steps:

**Features:**

- ✅ RESTful API with FastAPI---└── SECURITY.md

- ✅ PDF receipt generation

- ✅ File attachment handling```bash

- ✅ Custom CORS middleware

- ✅ ULID-based IDs# Step 1: Create Docker network for service communication



**Stack:**docker network create grievance_net

- PostgreSQL (data)

- MinIO (files)## 📋 Table of Contents```bash

- Redis (cache)

# Step 2: Start all services

**Tests:** 🎯 41 passing

- 26 general API testsdocker compose up -d --build# 1) Start infra (DB/Redis/MinIO) + API + Typebot* (optional)

- 15 Typebot integration tests



</td>

<td width="50%" valign="top"># Step 3: Access the services ✨- [Quick Start](#-quick-start)



#### 🤖 **Typebot Chatbot**```



**Location:** `frontend-typebot/`- [Architecture](#-architecture)cd infra



**Ports:** ### 🌐 Service URLs

- 8081 (Builder)

- 8082 (Viewer)- [Testing](#-testing)



**Modes:**| Service | URL | Description |

- 🔵 **Production:** Server-side webhooks

- 🟢 **Development:** Browser webhooks|---------|-----|-------------|- [API Endpoints](#-api-endpoints)## Quick Start (Local)cp .env.example .env



**Features:**| 📚 **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |

- 🎨 No-code bot designer

- 🔗 Webhook integration| 🤖 **Typebot Builder** | http://localhost:8081 | Design bot flows |- [Typebot Configuration](#-typebot-configuration)

- 📎 File upload support

- 🌍 Multi-language support| 💬 **Typebot Viewer** | http://localhost:8082 | Public bot interface |

- 📧 Email notifications

- 🛡️ Anti-spam protection| 📦 **MinIO Console** | http://localhost:9001 | S3 storage management |- [Development](#-development)# edit values, then:



**Integration:**| 📧 **MailHog** | http://localhost:8025 | Email testing UI |

- Connects via `grievance_net`

- Seamless API communication- [Troubleshooting](#-troubleshooting)

- Two export configurations

---

</td>

</tr>- [Production Deployment](#-production-deployment)bashdocker compose up -d

</table>

## 🏗 Architecture

### 💾 Data & Infrastructure



| Service | Port(s) | Purpose | Technology |

|---------|---------|---------|------------|### Service Overview

| **PostgreSQL** (grievance) | 5432 | Main grievance data | PostgreSQL 16 |

| **PostgreSQL** (typebot) | 5433 | Typebot configuration | PostgreSQL 16 |---# 1) Create external Docker network for API-Typebot communication

| **MinIO** | 9000 / 9001 | S3-compatible file storage | MinIO latest |

| **Redis** | 6379 | Caching & sessions | Redis 7 |<table>

| **MailHog** | 1025 / 8025 | Email testing (SMTP + UI) | MailHog latest |

<tr>

### 🌐 Network Architecture

<td width="50%" valign="top">

```

┌─────────────────┐## 🚀 Quick Startdocker network create grievance_net# 2) Visit:

│  User Browser   │

└────────┬────────┘#### 🔥 **FastAPI Backend**

         │ HTTP

         ▼

┌─────────────────┐     grievance_net      ┌──────────────┐

│ Typebot Viewer  ├────────────────────────►│   FastAPI    │**Location:** `backend/`

│   (port 8082)   │                         │  (port 8000) │

└─────────────────┘                         └──────┬───────┘Get up and running in 3 simple steps:# API docs:          http://localhost:8000/docs

                                                   │ default network

                    ┌──────────────────────────────┼────────────┐**Endpoints:** 

                    ▼                              ▼            ▼

            ┌──────────────┐            ┌────────────┐  ┌───────────┐- `/api/grievances` - CRUD operations

            │  PostgreSQL  │            │   MinIO    │  │   Redis   │

            │  (port 5432) │            │ (port 9000)│  │ (port 6379)│- `/api/status` - System health

            └──────────────┘            └────────────┘  └───────────┘

``````bash# 2) Start all services (DB/Redis/MinIO/API/Typebot)# Typebot Builder*:  http://localhost:8081



**Network Details:****Features:**

- 🔵 **`default`** (auto-created): Internal service communication (DB, Redis, MinIO)

- 🟢 **`grievance_net`** (external): Typebot ↔ API communication- ✅ RESTful API with FastAPI# Step 1: Create Docker network for service communication

  - API accessible as `grievance-api:8000` from Typebot services

- ✅ PDF receipt generation

---

- ✅ File attachment handlingdocker network create grievance_netdocker compose up -d --build# Typebot Viewer*:   http://localhost:8082

## 🧪 Testing

- ✅ Custom CORS middleware

### Run Backend Tests

- ✅ ULID-based IDs

```bash

# Run all 41 tests

docker exec grievancemodule-api-1 pytest

**Stack:**# Step 2: Start all services# MinIO Console:     http://localhost:9001

# Run Typebot integration tests only (15 tests)

docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py -v- PostgreSQL (data)



# Run with coverage report- MinIO (files)docker compose up -d --build# 3) Visit:

docker exec grievancemodule-api-1 pytest --cov=app --cov-report=html

- Redis (cache)

# View coverage

open backend/htmlcov/index.html  # macOS/Linux# API docs:          http://localhost:8000/docs

start backend/htmlcov/index.html  # Windows

```**Tests:** 🎯 41 passing



### 🤖 Test Typebot Integration- 26 general API tests# Step 3: Access the services# Typebot Builder:   http://localhost:8081



#### **Method 1: Published Bot** ⭐ _Recommended_- 15 Typebot integration tests



1. Open Typebot Builder: http://localhost:8081```# Typebot Viewer:    http://localhost:8082

2. Import: `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

3. Click **"Publish"** button (⚠️ not "Test" - CSP restrictions)</td>

4. Open the published bot URL in a new tab

5. Complete the flow and submit a test grievance<td width="50%" valign="top"># MinIO Console:     http://localhost:9001

6. Verify: Check API response and database entry



#### **Method 2: Browser Testing**

#### 🤖 **Typebot Chatbot**### 🌐 Service URLs# MailHog (email):   http://localhost:8025

1. Open `test-browser-webhook.html` in your browser

2. Click **"Test Webhook"** button

3. Check console for success message

4. Verify grievance created with API call**Location:** `frontend-typebot/````



### ✅ Test Coverage Summary



<details>**Ports:** | Service | URL | Description |

<summary><b>📊 Typebot Integration Tests</b> (15 tests in <code>test_typebot_integration.py</code>)</summary>

- 8081 (Builder)

<br>

- 8082 (Viewer)|---------|-----|-------------|## Architecture

#### ✅ Core Functionality (5 tests)

- Field mapping (Typebot schema → API schema)

- Complainant information (name, email, phone, gender)

- Location data (island, district, village)**Modes:**| 📚 **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |

- Category types

- Grievance details and descriptions- 🔵 **Production:** Server-side webhooks



#### ✅ File Handling (3 tests)- 🟢 **Development:** Browser webhooks| 🤖 **Typebot Builder** | http://localhost:8081 | Design bot flows |### Services

- Single file attachment

- Multiple file attachments

- Attachment validation & size limits

**Features:**| 💬 **Typebot Viewer** | http://localhost:8082 | Public bot interface |

#### ✅ User Flows (4 tests)

- Anonymous submissions- 🎨 No-code bot designer

- Named submissions with full details

- Household registration flow- 🔗 Webhook integration| 📦 **MinIO Console** | http://localhost:9001 | S3 storage management |- **FastAPI Backend** (`backend/`): REST API for grievance management

- Status lookup by grievance ID

- 📎 File upload support

#### ✅ Features (3 tests)

- PDF receipt generation- 🌍 Multi-language support| 📧 **MailHog** | http://localhost:8025 | Email testing UI |  - Endpoints: `/api/grievances`, `/api/status`

- Email notifications

- Error handling & validation- 📧 Email notifications



</details>- 🛡️ Anti-spam protection  - Features: CRUD operations, PDF receipt generation, attachment handling



---



## 📡 API Endpoints**Integration:**---  - Storage: PostgreSQL + MinIO (S3-compatible)



### 📝 Grievances- Connects via `grievance_net`



<details>- Seamless API communication  - Tests: 41 passing tests (26 general + 15 Typebot integration)

<summary><b>POST</b> <code>/api/grievances</code> - Create a new grievance</summary>

- Two export configurations

<br>

## 🏗 Architecture

**Request:**

```bash</td>

curl -X POST http://localhost:8000/api/grievances \

  -H "Content-Type: application/json" \</tr>- **Typebot** (`frontend-typebot/`): No-code chatbot for grievance intake

  -d '{

    "is_anonymous": false,</table>

    "complainant_name": "John Doe",

    "complainant_email": "john@example.com",### Service Overview  - Builder (port 8081): Design and configure bot flows

    "complainant_phone": "+676123456",

    "complainant_gender": "Male",### 💾 Data & Infrastructure

    "is_hh_registered": true,

    "hh_id": "HH12345",  - Viewer (port 8082): Public-facing bot interface

    "hh_address": "Main Street, Kolofo'\''ou",

    "island": "Tongatapu",| Service | Port(s) | Purpose | Technology |

    "district": "Nuku'\''alofa",

    "village": "Kolofo'\''ou",|---------|---------|---------|------------|<table>  - Two export versions:

    "category_type": "Registration",

    "details": "Need assistance with registration renewal",| **PostgreSQL** (grievance) | 5432 | Main grievance data | PostgreSQL 16 |

    "attachments": [

      {| **PostgreSQL** (typebot) | 5433 | Typebot configuration | PostgreSQL 16 |<tr>    - `typebot-export-grievance-intake-qwdn4no.json`: Production (server-side webhooks)

        "name": "document.pdf",

        "url": "https://storage.example.com/file.pdf",| **MinIO** | 9000 / 9001 | S3-compatible file storage | MinIO latest |

        "size": 102400,

        "type": "application/pdf"| **Redis** | 6379 | Caching & sessions | Redis 7 |<td width="50%">    - `typebot-export-grievance-intake-LOCALHOST-TEST.json`: Development (browser webhooks)

      }

    ]| **MailHog** | 1025 / 8025 | Email testing (SMTP + UI) | MailHog latest |

  }'

```



**Response:** `201 Created`### 🌐 Network Architecture

```json

{#### 🔥 **FastAPI Backend**- **PostgreSQL**: Two databases

  "id": "GRV-01K83WMY346N2S1KA7FK3W26RP",

  "created_at": "2025-10-21T12:00:00Z",```

  "updated_at": "2025-10-21T12:00:00Z",

  "is_anonymous": false,┌─────────────────┐- **Location:** `backend/`  - `grievance` (port 5432): Main grievance data

  "complainant_name": "John Doe",

  "complainant_email": "john@example.com",│  User Browser   │

  "island": "Tongatapu",

  "district": "Nuku'alofa",└────────┬────────┘- **Endpoints:** `/api/grievances`, `/api/status`  - `typebot` (port 5433): Typebot configuration

  "details": "Need assistance with registration renewal",

  ...         │ HTTP

}

```         ▼- **Features:**



</details>┌─────────────────┐     grievance_net      ┌──────────────┐



<details>│ Typebot Viewer  ├────────────────────────►│   FastAPI    │  - ✅ CRUD operations- **MinIO** (ports 9000/9001): S3-compatible object storage for attachments

<summary><b>GET</b> <code>/api/grievances/{id}</code> - Get grievance by ID</summary>

│   (port 8082)   │                         │  (port 8000) │

<br>

└─────────────────┘                         └──────┬───────┘  - ✅ PDF receipt generation

```bash

curl http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP                                                   │ default network

```

                    ┌──────────────────────────────┼────────────┐  - ✅ File attachment handling- **Redis** (port 6379): Caching and session storage

**Response:** `200 OK` (full grievance object)

                    ▼                              ▼            ▼

</details>

            ┌──────────────┐            ┌────────────┐  ┌───────────┐  - ✅ Custom CORS middleware

<details>

<summary><b>GET</b> <code>/api/grievances/{id}/receipt.pdf</code> - Download PDF receipt</summary>            │  PostgreSQL  │            │   MinIO    │  │   Redis   │



<br>            │  (port 5432) │            │ (port 9000)│  │ (port 6379)│- **Storage:** PostgreSQL + MinIO- **MailHog** (ports 1025/8025): Email testing (SMTP + web UI)



```bash            └──────────────┘            └────────────┘  └───────────┘

curl -O http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP/receipt.pdf

``````- **Tests:** 41 passing (26 general + 15 Typebot)



**Response:** `200 OK` (PDF file with QR code)



</details>**Network Details:**### Networking



<details>- 🔵 **`default`** (auto-created): Internal service communication (DB, Redis, MinIO)

<summary><b>PATCH</b> <code>/api/grievances/{id}</code> - Update grievance status</summary>

- 🟢 **`grievance_net`** (external): Typebot ↔ API communication</td>

<br>

  - API accessible as `grievance-api:8000` from Typebot services

```bash

curl -X PATCH http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP \<td width="50%">The system uses two Docker networks:

  -H "Content-Type: application/json" \

  -d '{---

    "external_status": "Under Review",

    "external_status_note": "Processing your request"

  }'

```## 🧪 Testing



**Response:** `200 OK` (updated grievance)#### 🤖 **Typebot Chatbot**1. **`default`** (auto-created): Internal service communication



</details>### Run Backend Tests



### 🏥 Health & Status- **Location:** `frontend-typebot/`2. **`grievance_net`** (external): Enables Typebot → API communication



| Endpoint | Method | Description | Response |```bash

|----------|--------|-------------|----------|

| `/` | GET | API health check | `{"ok": true, "service": "Grievance Management API"}` |# Run all 41 tests- **Ports:** 8081 (Builder), 8082 (Viewer)   - API is accessible as `grievance-api:8000` from Typebot services

| `/api/status` | GET | System status | `{"status": "ok", "database": "connected", ...}` |

docker exec grievancemodule-api-1 pytest

---

- **Modes:**

## 🤖 Typebot Configuration

# Run Typebot integration tests only (15 tests)

### 🔵 Production Setup (Server-side webhooks)

docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py -v  - 🔵 **Production:** Server-side webhooks## Testing

**File:** `typebot-export-grievance-intake-qwdn4no.json`



```json

{# Run with coverage report  - 🟢 **Development:** Browser webhooks

  "isExecutedOnClient": false,

  "webhook": {docker exec grievancemodule-api-1 pytest --cov=app --cov-report=html

    "url": "http://grievance-api:8000/api/grievances",

    "method": "POST",- **Features:**### Run Backend Tests

    "headers": [

      {"key": "Content-Type", "value": "application/json"}# View coverage

    ]

  }open backend/htmlcov/index.html  # macOS/Linux  - No-code bot designer

}

```start backend/htmlcov/index.html  # Windows



**✅ Use this for:**```  - Webhook integration```bash

- Production deployments

- Published bots

- Server-side execution (more secure)

- Docker internal network communication### 🤖 Test Typebot Integration  - File upload support# All tests (41 total)



### 🟢 Development Setup (Browser webhooks)



**File:** `typebot-export-grievance-intake-LOCALHOST-TEST.json`#### **Method 1: Published Bot** ⭐ _Recommended_  - Multi-language supportdocker exec grievancemodule-api-1 pytest



```json

{

  "isExecutedOnClient": true,1. Open Typebot Builder: http://localhost:8081

  "webhook": {

    "url": "http://localhost:8000/api/grievances"2. Import: `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

  }

}3. Click **"Publish"** button (⚠️ not "Test" - CSP restrictions)</td># Typebot integration tests only (15 tests)

```

4. Open the published bot URL in a new tab

**✅ Use this for:**

- Local development5. Complete the flow and submit a test grievance</tr>docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py

- Browser testing

- Debugging webhook payloads6. Verify: Check API response and database entry

- Client-side execution

</table>

### 🛡 CORS Configuration

#### **Method 2: Browser Testing**

The API uses **custom CORS middleware** to support all integration scenarios:

# With coverage

**Automatically handles:**

- ✅ All origins including `null` (file:// protocol)1. Open `test-browser-webhook.html` in your browser

- ✅ OPTIONS preflight requests

- ✅ Browser-based webhook execution2. Click **"Test Webhook"** button### 💾 Data Layerdocker exec grievancemodule-api-1 pytest --cov=app

- ✅ Typebot client-side mode

- ✅ Cross-origin requests3. Check console for success message



**Implementation:**4. Verify grievance created with API call```

```python

# backend/app/main.py

@app.middleware("http")

async def custom_cors_middleware(request: Request, call_next):### ✅ Test Coverage Summary| Service | Port | Purpose |

    origin = request.headers.get("origin", "*")

    if request.method == "OPTIONS":

        return Response(status_code=200, headers={

            "Access-Control-Allow-Origin": origin,<details>|---------|------|---------|### Test Typebot Integration

            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",

            "Access-Control-Allow-Headers": "*",<summary><b>📊 Typebot Integration Tests</b> (15 tests in <code>test_typebot_integration.py</code>)</summary>

        })

    | **PostgreSQL** (grievance) | 5432 | Main grievance data |

    response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = origin<br>

    return response

```| **PostgreSQL** (typebot) | 5433 | Typebot configuration |**Option 1: Published Bot (Recommended)**



---#### ✅ Core Functionality (5 tests)



## 💻 Development- Field mapping (Typebot schema → API schema)| **MinIO** | 9000/9001 | S3-compatible file storage |1. Open Typebot Builder: http://localhost:8081



### 📁 Project Structure- Complainant information (name, email, phone, gender)



```- Location data (island, district, village)| **Redis** | 6379 | Caching & sessions |2. Import `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

grievance-module/

│- Category types

├── 📂 backend/                           # FastAPI Application

│   ├── 📂 app/- Grievance details and descriptions| **MailHog** | 1025/8025 | Email testing (SMTP + UI) |3. Click **"Publish"** (not "Test" - CSP restrictions apply to preview mode)

│   │   ├── main.py                      # FastAPI app + CORS middleware

│   │   ├── database.py                  # SQLAlchemy configuration

│   │   ├── models.py                    # Database ORM models

│   │   ├── schemas.py                   # Pydantic validation schemas#### ✅ File Handling (3 tests)4. Access published bot URL

│   │   ├── 📂 routers/

│   │   │   ├── grievances.py           # Grievance CRUD endpoints- Single file attachment

│   │   │   └── status.py               # System status endpoints

│   │   └── 📂 utils/- Multiple file attachments### 🌐 Network Architecture5. Submit a grievance - webhook executes server-side

│   │       ├── id.py                    # ULID generator (GRV-01ABC...)

│   │       └── pdf.py                   # PDF receipt generator (with QR)- Attachment validation & size limits

│   ├── 📂 tests/

│   │   ├── test_api.py                  # 26 general API tests

│   │   └── test_typebot_integration.py  # 15 Typebot integration tests

│   ├── Dockerfile                       # Multi-stage Docker build#### ✅ User Flows (4 tests)

│   ├── requirements.txt                 # Python dependencies

│   └── .env                            # Environment configuration- Anonymous submissions```mermaid**Option 2: Browser Testing**

│

├── 📂 frontend-typebot/                  # Typebot Configuration- Named submissions with full details

│   ├── typebot-export-grievance-intake-qwdn4no.json         # Production

│   ├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development- Household registration flowgraph LR1. Open `test-browser-webhook.html` in browser

│   ├── 📂 public/

│   │   └── typebot-grievance-flow.html  # Embed example- Status lookup by grievance ID

│   └── test-browser-webhook.html        # Browser testing tool

│    A[User Browser] -->|HTTP| B[Typebot Viewer]2. Click "Test Webhook"

├── 📂 docs/                              # Documentation & Diagrams

│   └── 📂 images/#### ✅ Features (3 tests)

│       └── figure-10-grm-architecture.png

│- PDF receipt generation    B -->|grievance_net| C[FastAPI]3. Simulates client-side webhook execution with CORS

├── 📂 ops/                               # CI/CD & Operations

│   └── 📂 github-actions/- Email notifications

│       ├── ci.yml                       # Continuous Integration

│       └── docker-api.yml               # Docker build & push- Error handling & validation    C -->|default| D[PostgreSQL]

│

├── docker-compose.yml                    # Service orchestration

├── README.md                             # This file

└── LICENSE                               # Project license</details>    C -->|default| E[MinIO]### Test Coverage

```



### 🔧 Environment Variables

---    C -->|default| F[Redis]

<details>

<summary><b>Backend Configuration</b> (<code>.env</code>)</summary>



<br>## 📡 API Endpoints    G[Typebot Builder] -->|grievance_net| C**Typebot Integration Tests** (`test_typebot_integration.py`):



```bash

# Database

DATABASE_URL=postgresql://grievance:grievance@db:5432/grievance### 📝 Grievances```- ✅ Field mapping (Typebot → API schema)



# Cache

REDIS_URL=redis://redis:6379/0

<details>- ✅ Complainant information handling

# Object Storage (MinIO/S3)

MINIO_ENDPOINT=minio:9000<summary><b>POST</b> <code>/api/grievances</code> - Create a new grievance</summary>

MINIO_ACCESS_KEY=minioadmin

MINIO_SECRET_KEY=minioadmin**Two Docker Networks:**- ✅ Location data (island, district, village)

MINIO_BUCKET=grievances

MINIO_SECURE=false<br>



# API Configuration- 🔵 **`default`** (auto-created): Internal service communication- ✅ Category types

DEBUG=true

API_VERSION=0.1.0**Request:**

SECRET_KEY=your-secret-key-here

```bash- 🟢 **`grievance_net`** (external): Typebot ↔ API communication- ✅ Attachment handling (single & multiple files)

# CORS (optional - custom middleware handles all origins)

ALLOWED_ORIGINS=*curl -X POST http://localhost:8000/api/grievances \

```

  -H "Content-Type: application/json" \  - API accessible as `grievance-api:8000` from Typebot- ✅ Anonymous submissions

</details>

  -d '{

<details>

<summary><b>Typebot Configuration</b> (in <code>docker-compose.yml</code>)</summary>    "is_anonymous": false,- ✅ Named submissions with full details



<br>    "complainant_name": "John Doe",



```yaml    "complainant_email": "john@example.com",---- ✅ Household registration flow

# Core Settings

DATABASE_URL: postgresql://typebot:typebot@typebot-db:5432/typebot    "complainant_phone": "+676123456",

ENCRYPTION_SECRET: <64-character-random-string-required-for-webhooks>

NEXTAUTH_URL: http://localhost:8081    "complainant_gender": "Male",- ✅ Status lookup by grievance ID

NEXT_PUBLIC_VIEWER_URL: http://localhost:8082

NEXTAUTH_URL_INTERNAL: http://typebot-builder:3000    "is_hh_registered": true,

ADMIN_EMAIL: admin@example.com

DISABLE_SIGNUP: false    "hh_id": "HH12345",## 🧪 Testing- ✅ PDF receipt generation



# Email (MailHog for local testing)    "hh_address": "Main Street, Kolofo'\''ou",

SMTP_HOST: mailhog

SMTP_PORT: 1025    "island": "Tongatapu",- ✅ Email notifications

SMTP_USERNAME: x

SMTP_PASSWORD: x    "district": "Nuku'\''alofa",

SMTP_SECURE: false

NEXT_PUBLIC_SMTP_FROM: noreply@typebot.local    "village": "Kolofo'\''ou",### Run Backend Tests- ✅ Error handling and validation



# Storage (MinIO S3-compatible)    "category_type": "Registration",

S3_ACCESS_KEY: minioadmin

S3_SECRET_KEY: minioadmin    "details": "Need assistance with registration renewal",

S3_BUCKET: typebot

S3_ENDPOINT: minio    "attachments": [

S3_PORT: 9000

S3_SSL: false      {```bash## Typebot Configuration

NEXT_PUBLIC_S3_ENDPOINT: http://localhost:9000

```        "name": "document.pdf",



</details>        "url": "https://storage.example.com/file.pdf",# Run all 41 tests



### ✨ Key Features        "size": 102400,



#### 📎 **Attachment Handling**        "type": "application/pdf"docker exec grievancemodule-api-1 pytest### Production Setup (Server-side webhooks)

- 📤 Multiple file uploads (max 5 files)

- ⚖️ Size validation (10MB per file, 25MB total)      }

- 📄 Supported formats: `.jpg`, `.png`, `.pdf`, `.docx`, `.xlsx`, `.img`

- 🗄️ Stores file URLs from MinIO S3 storage    ]

- 🔄 Handles both Pydantic `AttachmentIn` objects and raw dicts

  }'

#### 🆔 **Smart ID Generation**

- **Format:** `GRV-01ABC123...` (26 characters)```# Run Typebot integration tests only (15 tests)File: `typebot-export-grievance-intake-qwdn4no.json`

- **Technology:** ULID (Universally Unique Lexicographically Sortable Identifier)

- **Benefits:** 

  - ✅ Sortable by timestamp

  - ✅ Globally unique**Response:** `201 Created`docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py -v

  - ✅ URL-safe

  - ✅ Case-insensitive```json

  - ✅ Timestamp embedded

{```json

#### 📄 **PDF Receipt Generation**

- 🎨 Professional formatting with branding  "id": "GRV-01K83WMY346N2S1KA7FK3W26RP",

- 📊 Includes all grievance details

- 🔲 QR code for easy tracking  "created_at": "2025-10-21T12:00:00Z",# Run with coverage report{

- 📥 Downloadable via `/api/grievances/{id}/receipt.pdf`

- 📧 Email-ready format  "updated_at": "2025-10-21T12:00:00Z",



#### 🛡 **Anti-Spam Protection**  "is_anonymous": false,docker exec grievancemodule-api-1 pytest --cov=app --cov-report=html  "isExecutedOnClient": false,

- 🍯 **Honeypot field** (invisible to humans, catches bots)

- ⏱️ **Timing validation** (minimum 3 seconds to complete form)  "complainant_name": "John Doe",

- 🧮 **Math challenge** for suspicious submissions (1 + 2 = ?)

- 🚫 **Rate limiting** (configurable per IP)  "complainant_email": "john@example.com",```  "webhook": {



---  "island": "Tongatapu",



## 🔧 Troubleshooting  "district": "Nuku'alofa",    "url": "http://grievance-api:8000/api/grievances",



### ⚠️ Common Issues  "details": "Need assistance with registration renewal",



<table>  ...### 🤖 Test Typebot Integration    "method": "POST",

<tr>

<th width="35%">Issue</th>}

<th width="65%">Solution</th>

</tr>```    "headers": [{"key": "Content-Type", "value": "application/json"}]



<tr>

<td><b>Typebot "Test" Button Error</b><br><code>Error! Could not reach server</code></td>

<td></details>#### **Option 1: Published Bot** ⭐ _Recommended_  }

✅ <b>Use "Publish" instead of "Test"</b><br>

1. Click "Publish" in Typebot Builder<br>

2. Access bot via the published URL<br>

3. Webhooks work correctly in published mode<br><details>}

<br>

<i>Reason: Content Security Policy (CSP) blocks HTTP in preview mode</i><summary><b>GET</b> <code>/api/grievances/{id}</code> - Get grievance by ID</summary>

</td>

</tr>1. Open Typebot Builder: http://localhost:8081```



<tr><br>

<td><b>CORS Errors</b><br><code>No 'Access-Control-Allow-Origin' header</code></td>

<td>2. Import `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

✅ <b>Already Fixed!</b> Custom CORS middleware handles all origins<br>

- Supports <code>null</code> origin (file:// protocol)<br>```bash

- Handles OPTIONS preflight requests<br>

- Works with server-side and client-side webhookscurl http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP3. Click **"Publish"** button (⚠️ don't use "Test" - CSP restrictions)- Webhooks execute from Typebot Viewer container

</td>

</tr>```



<tr>4. Access the published bot URL- Uses Docker internal network (`grievance_net`)

<td><b>Network Connectivity</b><br>Typebot can't reach API</td>

<td>**Response:** `200 OK` (full grievance object)

<b>Ensure network exists:</b><br>

<code>docker network create grievance_net</code><br>5. Submit a test grievance- API accessible as `grievance-api:8000`

<code>docker compose up -d</code><br>

<br></details>

<b>Verify configuration:</b><br>

<code>docker network inspect grievance_net</code><br>

Should show: api, typebot-builder, typebot-viewer

</td><details>

</tr>

<summary><b>GET</b> <code>/api/grievances/{id}/receipt.pdf</code> - Download PDF receipt</summary>#### **Option 2: Browser Testing**### Development Setup (Browser webhooks)

<tr>

<td><b>Service won't start</b><br>Port already in use</td>

<td>

<b>Check ports:</b><br><br>

<code>netstat -ano | findstr :8000</code> (Windows)<br>

<code>lsof -i :8000</code> (macOS/Linux)<br>

<br>

<b>Or change ports in docker-compose.yml</b>```bash1. Open `test-browser-webhook.html` in your browserFile: `typebot-export-grievance-intake-LOCALHOST-TEST.json`

</td>

</tr>curl -O http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP/receipt.pdf

</table>

```2. Click **"Test Webhook"** button

### 🗄 Database Management



<details>

<summary><b>Reset all data</b> (⚠️ destructive operation)</summary>**Response:** `200 OK` (PDF file with QR code)3. Verify successful creation```json



<br>



```bash</details>{

# Stop and remove all containers, networks, and volumes

docker compose down -v



# Rebuild and start fresh<details>### ✅ Test Coverage  "isExecutedOnClient": true,

docker compose up -d --build

```<summary><b>PATCH</b> <code>/api/grievances/{id}</code> - Update grievance status</summary>



</details>  "webhook": {



<details><br>

<summary><b>Access PostgreSQL databases</b></summary>

<details>    "url": "http://localhost:8000/api/grievances"

<br>

```bash

```bash

# Access grievance databasecurl -X PATCH http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP \<summary><b>Typebot Integration Tests</b> (15 tests in <code>test_typebot_integration.py</code>)</summary>  }

docker exec -it grievancemodule-db-1 psql -U grievance -d grievance

  -H "Content-Type: application/json" \

# Access Typebot database

docker exec -it grievancemodule-typebot-db-1 psql -U typebot -d typebot  -d '{}



# Useful SQL commands:    "external_status": "Under Review",

# \dt              - List tables

# \d+ table_name   - Describe table    "external_status_note": "Processing your request"#### Core Functionality```

# SELECT * FROM grievances LIMIT 10;

```  }'



</details>```- ✅ Field mapping (Typebot schema → API schema)



<details>

<summary><b>View service logs</b></summary>

**Response:** `200 OK` (updated grievance)- ✅ Complainant information (name, email, phone, gender)- Webhooks execute in user's browser

<br>



```bash

# API logs</details>- ✅ Location data (island, district, village)- Requires CORS configuration (already configured)

docker compose logs -f api



# Typebot Viewer logs

docker compose logs -f typebot-viewer### 🏥 Health & Status- ✅ Category types- For testing in Typebot Builder environment



# All services

docker compose logs -f

| Endpoint | Method | Description | Response |- ✅ Grievance details and descriptions

# Last 100 lines

docker compose logs --tail=100 api|----------|--------|-------------|----------|



# Filter for errors| `/` | GET | API health check | `{"ok": true, "service": "Grievance Management API"}` |### CORS Configuration

docker compose logs api | grep ERROR

```| `/api/status` | GET | System status | `{"status": "ok", "database": "connected", ...}` |



</details>#### File Handling



<details>---

<summary><b>Restart individual services</b></summary>

- ✅ Single file attachmentThe API uses custom CORS middleware to support:

<br>

## 🤖 Typebot Configuration

```bash

# Restart API- ✅ Multiple file attachments- All origins including `null` (for `file://` protocol)

docker compose restart api

### 🔵 Production Setup (Server-side webhooks)

# Restart Typebot services

docker compose restart typebot-builder typebot-viewer- ✅ Attachment validation- Browser-based webhook execution



# Restart database**File:** `typebot-export-grievance-intake-qwdn4no.json`

docker compose restart db

```- Typebot client-side mode



</details>```json



---{#### User Flows



## 🚀 Production Deployment  "isExecutedOnClient": false,



### ✅ Prerequisites Checklist  "webhook": {- ✅ Anonymous submissions```python



- [ ] **HTTPS/SSL certificates** (required for Typebot)    "url": "http://grievance-api:8000/api/grievances",

- [ ] **Domain names** configured (e.g., api.example.com, bot.example.com)

- [ ] **Managed PostgreSQL** database set up    "method": "POST",- ✅ Named submissions with full details# backend/app/main.py

- [ ] **S3-compatible storage** (AWS S3, DigitalOcean Spaces, etc.)

- [ ] **Email service** (SendGrid, AWS SES, Mailgun)    "headers": [

- [ ] **Strong secrets** generated for all services

- [ ] **Firewall rules** configured (allow only necessary ports)      {"key": "Content-Type", "value": "application/json"}- ✅ Household registration flow@app.middleware("http")

- [ ] **Monitoring & alerting** system in place

- [ ] **Backup strategy** implemented    ]

- [ ] **CI/CD pipeline** configured

  }- ✅ Status lookup by grievance IDasync def custom_cors_middleware(request: Request, call_next):

### ⚙️ Production Configuration

}

<details>

<summary><b>Environment Variables</b></summary>```    origin = request.headers.get("origin", "*")



<br>



```bash**✅ Use this for:**#### Features    # Handles OPTIONS preflight and adds CORS headers to all responses

####################

# API Configuration- Production deployments

####################

- Published bots- ✅ PDF receipt generation```

# Database (use managed PostgreSQL)

DATABASE_URL=postgresql://user:strong_password@db-host.example.com:5432/grievance?sslmode=require- Server-side execution (more secure)



# Cache (use managed Redis)- Docker internal network communication- ✅ Email notifications

REDIS_URL=redis://redis-host.example.com:6379/0?ssl=true



# Object Storage (use AWS S3 or similar)

MINIO_ENDPOINT=s3.amazonaws.com### 🟢 Development Setup (Browser webhooks)- ✅ Error handling and validation## API Endpoints

MINIO_ACCESS_KEY=<aws-access-key-id>

MINIO_SECRET_KEY=<aws-secret-access-key>

MINIO_BUCKET=prod-grievances

MINIO_SECURE=true**File:** `typebot-export-grievance-intake-LOCALHOST-TEST.json`- ✅ Anti-spam measures



# API Settings

DEBUG=false

API_VERSION=0.1.0```json### Grievances

SECRET_KEY=<64-character-random-string>

{

# CORS (restrict to specific domains in production)

ALLOWED_ORIGINS=https://bot.example.com,https://builder.example.com  "isExecutedOnClient": true,</details>



####################  "webhook": {

# Typebot Configuration

####################    "url": "http://localhost:8000/api/grievances"**Create Grievance**



# Core Settings  }

DATABASE_URL=postgresql://typebot:strong_password@typebot-db.example.com:5432/typebot?sslmode=require

ENCRYPTION_SECRET=<64-character-random-string>}---```bash

NEXTAUTH_URL=https://builder.example.com

NEXT_PUBLIC_VIEWER_URL=https://bot.example.com```

ADMIN_EMAIL=admin@example.com

DISABLE_SIGNUP=true  # Disable public signups in productionPOST /api/grievances



# SMTP (use real email service)**✅ Use this for:**

SMTP_HOST=smtp.sendgrid.net

SMTP_PORT=587- Local development## 📡 API EndpointsContent-Type: application/json

SMTP_USERNAME=apikey

SMTP_PASSWORD=<sendgrid-api-key>- Browser testing

SMTP_SECURE=true

NEXT_PUBLIC_SMTP_FROM=noreply@example.com- Debugging webhook payloads



# Storage- Client-side execution

S3_ACCESS_KEY=<aws-access-key-id>

S3_SECRET_KEY=<aws-secret-access-key>### 📝 Grievances{

S3_BUCKET=prod-typebot

S3_ENDPOINT=s3.amazonaws.com### 🛡 CORS Configuration

S3_SSL=true

NEXT_PUBLIC_S3_ENDPOINT=https://cdn.example.com  "is_anonymous": true,

```

The API uses **custom CORS middleware** to support all integration scenarios:

</details>

<details>  "complainant_name": "John Doe",

### 🔒 Security Checklist

**Automatically handles:**

**Before going live:**

- ✅ All origins including `null` (file:// protocol)<summary><b>POST</b> <code>/api/grievances</code> - Create a new grievance</summary>  "complainant_email": "john@example.com",

- [ ] Change all default passwords

- [ ] Enable SSL/TLS for all connections (PostgreSQL, Redis)- ✅ OPTIONS preflight requests

- [ ] Configure proper SMTP credentials

- [ ] Set up automated database backups (daily minimum)- ✅ Browser-based webhook execution  "complainant_phone": "+676123456",

- [ ] Enable API rate limiting (e.g., 100 requests/minute)

- [ ] Configure firewall rules (allow only 80, 443, and admin access)- ✅ Typebot client-side mode

- [ ] Set up SSL certificates for all domains (Let's Encrypt or commercial)

- [ ] Enable HTTPS redirect (HTTP → HTTPS)- ✅ Cross-origin requests```bash  "complainant_gender": "Male",

- [ ] Configure CORS for specific production domains only

- [ ] Review and update security headers (CSP, HSTS, X-Frame-Options)

- [ ] Set up intrusion detection (fail2ban or similar)

- [ ] Enable container security scanning**Implementation:**curl -X POST http://localhost:8000/api/grievances \  "is_hh_registered": false,

- [ ] Implement log monitoring and alerting

- [ ] Set up DDoS protection (Cloudflare or AWS Shield)```python

- [ ] Review and harden Docker security

# backend/app/main.py  -H "Content-Type: application/json" \  "hh_id": "HH123",

### 📊 Monitoring & Health Checks

@app.middleware("http")

#### Health Endpoints

async def custom_cors_middleware(request: Request, call_next):  -d '{  "hh_address": "Main Street",

```bash

# API health check    origin = request.headers.get("origin", "*")

curl https://api.example.com/

# Expected: {"ok": true, "service": "Grievance Management API", "version": "0.1.0"}        "is_anonymous": false,  "island": "Tongatapu",



# System status    if request.method == "OPTIONS":

curl https://api.example.com/api/status

# Expected: {"status": "ok", "database": "connected", "redis": "connected"}        return Response(status_code=200, headers={    "complainant_name": "John Doe",  "district": "Nuku'alofa",



# Typebot health            "Access-Control-Allow-Origin": origin,

curl https://bot.example.com/

# Expected: 200 OK            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",    "complainant_email": "john@example.com",  "village": "Kolofo'ou",

```

            "Access-Control-Allow-Headers": "*",

#### Logging & Monitoring

        })    "complainant_phone": "+676123456",  "category_type": "Registration",

```bash

# Production logs (if using Docker Compose)    

docker compose -f docker-compose.prod.yml logs -f --tail=100 api

    response = await call_next(request)    "complainant_gender": "Male",  "details": "Issue description...",

# Error monitoring

docker compose logs api | grep ERROR    response.headers["Access-Control-Allow-Origin"] = origin



# Access logs (track API usage)    return response    "is_hh_registered": true,  "attachments": [

docker compose logs api | grep POST

```

# Performance monitoring

docker stats grievancemodule-api-1    "hh_id": "HH12345",    {

```

---

**Recommended monitoring tools:**

- 📊 **Application Performance Monitoring:** New Relic, Datadog, or Sentry    "hh_address": "Main Street, Kolofo'\''ou",      "name": "photo.jpg",

- 🚨 **Alerting:** PagerDuty or Opsgenie

- 📈 **Metrics:** Prometheus + Grafana## 💻 Development

- 📝 **Log aggregation:** ELK Stack (Elasticsearch, Logstash, Kibana) or Loki

    "island": "Tongatapu",      "url": "https://...",

### 📈 Performance Optimization

### 📁 Project Structure

**For production workloads:**

    "district": "Nuku'\''alofa",      "size": 1024,

1. **Database Optimization**

   - Enable connection pooling (SQLAlchemy default: 5-10 connections)```

   - Add indexes for frequently queried fields (`id`, `created_at`, `island`, `district`)

   - Regular VACUUM and ANALYZE operationsgrievance-module/    "village": "Kolofo'\''ou",      "type": "image/jpeg"

   - Consider read replicas for high traffic

│

2. **Caching Strategy**

   - Configure Redis for session storage and API response caching├── 📂 backend/                           # FastAPI Application    "category_type": "Registration",    }

   - Cache static content (PDF receipts after generation)

   - Implement cache invalidation strategy│   ├── 📂 app/



3. **CDN & Static Assets**│   │   ├── main.py                      # FastAPI app + CORS middleware    "details": "Need assistance with registration renewal",  ]

   - Serve static files through CDN (CloudFront, Cloudflare)

   - Enable gzip/brotli compression│   │   ├── database.py                  # SQLAlchemy configuration

   - Optimize images and assets

│   │   ├── models.py                    # Database ORM models    "attachments": [}

4. **API Optimization**

   - Implement pagination for large datasets (default: 50 items per page)│   │   ├── schemas.py                   # Pydantic validation schemas

   - Use database query optimization (select only needed fields)

   - Enable async workers for long-running tasks (PDF generation, emails)│   │   ├── 📂 routers/      {



5. **Infrastructure**│   │   │   ├── grievances.py           # Grievance CRUD endpoints

   - Use container orchestration (Kubernetes or AWS ECS) for auto-scaling

   - Configure horizontal pod autoscaling based on CPU/memory│   │   │   └── status.py               # System status endpoints        "name": "document.pdf",Response: 201 Created

   - Set up load balancing for high availability

│   │   └── 📂 utils/

---

│   │       ├── id.py                    # ULID generator (GRV-01ABC...)        "url": "https://storage.example.com/file.pdf",{

## 📄 License

│   │       └── pdf.py                   # PDF receipt generator (with QR)

This project is licensed under the terms specified in the [`LICENSE`](LICENSE) file.

│   ├── 📂 tests/        "size": 102400,  "id": "GRV-01ABC123...",

---

│   │   ├── test_api.py                  # 26 general API tests

## 🤝 Contributing

│   │   └── test_typebot_integration.py  # 15 Typebot integration tests        "type": "application/pdf"  "created_at": "2025-10-21T12:00:00Z",

We welcome contributions! Please follow these guidelines:

│   ├── Dockerfile                       # Multi-stage Docker build

### Development Workflow

│   ├── requirements.txt                 # Python dependencies      }  ...

1. **Fork & Clone** the repository

2. **Create a feature branch:** `git checkout -b feature/amazing-feature`│   └── .env                            # Environment configuration

3. **Make your changes** with clear, descriptive commits

4. **Run tests:** `docker exec grievancemodule-api-1 pytest`│    ]}

5. **Ensure all tests pass** (41/41 should be green ✅)

6. **Submit a Pull Request** with a clear description├── 📂 frontend-typebot/                  # Typebot Configuration



### Code Standards│   ├── typebot-export-grievance-intake-qwdn4no.json         # Production  }'```



- ✅ Follow **PEP 8** style guide for Python│   ├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development

- ✅ Write **meaningful commit messages**

- ✅ Add **tests for new features** (maintain or increase coverage)│   ├── 📂 public/```

- ✅ Update **documentation** for API changes

- ✅ Use **type hints** for Python code│   │   └── typebot-grievance-flow.html  # Embed example

- ✅ Keep functions **small and focused**

│   └── test-browser-webhook.html        # Browser testing tool**Get Grievance**

### Pull Request Checklist

│

- [ ] Tests pass (`pytest`)

- [ ] Code follows style guidelines├── 📂 docs/                              # Documentation & Diagrams**Response:** `201 Created````bash

- [ ] Documentation updated

- [ ] No new warnings or errors│   └── 📂 images/

- [ ] Commits are clean and descriptive

│       └── figure-10-grm-architecture.png```jsonGET /api/grievances/{id}

---

│

<div align="center">

├── 📂 ops/                               # CI/CD & Operations{Response: 200 OK

### 🌟 Built With

│   └── 📂 github-actions/

[FastAPI](https://fastapi.tiangolo.com) · [PostgreSQL](https://www.postgresql.org) · [Typebot](https://typebot.io) · [MinIO](https://min.io) · [Redis](https://redis.io) · [Docker](https://www.docker.com)

│       ├── ci.yml                       # Continuous Integration  "id": "GRV-01K83WMY346N2S1KA7FK3W26RP",```

<br>

│       └── docker-api.yml               # Docker build & push

**Made with ❤️ for Vaka Sosiale**

│  "created_at": "2025-10-21T12:00:00Z",

<br>

├── docker-compose.yml                    # Service orchestration

[![Report Bug](https://img.shields.io/badge/🐛-Report%20Bug-red?style=for-the-badge)](https://github.com/gger-max/grievance-module/issues)

[![Request Feature](https://img.shields.io/badge/✨-Request%20Feature-blue?style=for-the-badge)](https://github.com/gger-max/grievance-module/issues)├── README.md                             # This file  "updated_at": "2025-10-21T12:00:00Z",**Download Receipt**

[![Documentation](https://img.shields.io/badge/📚-Documentation-green?style=for-the-badge)](http://localhost:8000/docs)

└── LICENSE                               # Project license

</div>

```  "is_anonymous": false,```bash



### 🔧 Environment Variables  "complainant_name": "John Doe",GET /api/grievances/{id}/receipt.pdf



<details>  ...Response: 200 OK (application/pdf)

<summary><b>Backend Configuration</b> (<code>.env</code>)</summary>

}```

<br>

```

```bash

# Database**Update Status**

DATABASE_URL=postgresql://grievance:grievance@db:5432/grievance

</details>```bash

# Cache

REDIS_URL=redis://redis:6379/0PATCH /api/grievances/{id}



# Object Storage (MinIO/S3)<details>{

MINIO_ENDPOINT=minio:9000

MINIO_ACCESS_KEY=minioadmin<summary><b>GET</b> <code>/api/grievances/{id}</code> - Get grievance details</summary>  "external_status": "Under Review",

MINIO_SECRET_KEY=minioadmin

MINIO_BUCKET=grievances  "external_status_note": "Processing your request"

MINIO_SECURE=false

```bash}

# API Configuration

DEBUG=truecurl http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP```

API_VERSION=0.1.0

SECRET_KEY=your-secret-key-here```



# CORS (optional - custom middleware handles all origins)### Status

ALLOWED_ORIGINS=*

```**Response:** `200 OK`



</details>**Health Check**



<details></details>```bash

<summary><b>Typebot Configuration</b> (in <code>docker-compose.yml</code>)</summary>

GET /

<br>

<details>Response: {"ok": true, "service": "Grievance Management API", "version": "0.1.0"}

```yaml

# Core Settings<summary><b>GET</b> <code>/api/grievances/{id}/receipt.pdf</code> - Download PDF receipt</summary>```

DATABASE_URL: postgresql://typebot:typebot@typebot-db:5432/typebot

ENCRYPTION_SECRET: <64-character-random-string-required-for-webhooks>

NEXTAUTH_URL: http://localhost:8081

NEXT_PUBLIC_VIEWER_URL: http://localhost:8082```bash**System Status**

NEXTAUTH_URL_INTERNAL: http://typebot-builder:3000

ADMIN_EMAIL: admin@example.comcurl -O http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP/receipt.pdf```bash

DISABLE_SIGNUP: false

```GET /api/status

# Email (MailHog for local testing)

SMTP_HOST: mailhogResponse: {"status": "ok", "database": "connected", ...}

SMTP_PORT: 1025

SMTP_USERNAME: x**Response:** `200 OK` (PDF file)```

SMTP_PASSWORD: x

SMTP_SECURE: false

NEXT_PUBLIC_SMTP_FROM: noreply@typebot.local

</details>## Development

# Storage (MinIO S3-compatible)

S3_ACCESS_KEY: minioadmin

S3_SECRET_KEY: minioadmin

S3_BUCKET: typebot<details>### Project Structure

S3_ENDPOINT: minio

S3_PORT: 9000<summary><b>PATCH</b> <code>/api/grievances/{id}</code> - Update status</summary>

S3_SSL: false

NEXT_PUBLIC_S3_ENDPOINT: http://localhost:9000```

```

```bashbackend/

</details>

curl -X PATCH http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP \├── app/

### ✨ Key Features

  -H "Content-Type: application/json" \│   ├── __init__.py

#### 📎 **Attachment Handling**

- 📤 Multiple file uploads (max 5 files)  -d '{│   ├── main.py              # FastAPI app + CORS middleware

- ⚖️ Size validation (10MB per file, 25MB total)

- 📄 Supported formats: `.jpg`, `.png`, `.pdf`, `.docx`, `.xlsx`, `.img`    "external_status": "Under Review",│   ├── database.py          # SQLAlchemy setup

- 🗄️ Stores file URLs from MinIO S3 storage

- 🔄 Handles both Pydantic `AttachmentIn` objects and raw dicts    "external_status_note": "Processing your request"│   ├── models.py            # Database models



#### 🆔 **Smart ID Generation**  }'│   ├── schemas.py           # Pydantic schemas

- **Format:** `GRV-01ABC123...` (26 characters)

- **Technology:** ULID (Universally Unique Lexicographically Sortable Identifier)```│   ├── routers/

- **Benefits:** 

  - ✅ Sortable by timestamp│   │   ├── grievances.py    # Grievance endpoints

  - ✅ Globally unique

  - ✅ URL-safe</details>│   │   └── status.py        # Status endpoints

  - ✅ Case-insensitive

  - ✅ Timestamp embedded│   └── utils/



#### 📄 **PDF Receipt Generation**### 🏥 Health & Status│       ├── id.py            # ULID generator

- 🎨 Professional formatting with branding

- 📊 Includes all grievance details│       └── pdf.py           # PDF receipt generation

- 🔲 QR code for easy tracking

- 📥 Downloadable via `/api/grievances/{id}/receipt.pdf`| Endpoint | Method | Description |├── tests/

- 📧 Email-ready format

|----------|--------|-------------|│   ├── test_api.py          # 26 general API tests

#### 🛡 **Anti-Spam Protection**

- 🍯 **Honeypot field** (invisible to humans, catches bots)| `/` | GET | Health check |│   └── test_typebot_integration.py  # 15 Typebot tests

- ⏱️ **Timing validation** (minimum 3 seconds to complete form)

- 🧮 **Math challenge** for suspicious submissions (1 + 2 = ?)| `/api/status` | GET | System status |├── Dockerfile

- 🚫 **Rate limiting** (configurable per IP)

└── requirements.txt

---

---

## 🔧 Troubleshooting

frontend-typebot/

### ⚠️ Common Issues

## 🤖 Typebot Configuration├── typebot-export-grievance-intake-qwdn4no.json         # Production

<table>

<tr>├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development

<th width="35%">Issue</th>

<th width="65%">Solution</th>### 🔵 Production Setup (Server-side webhooks)└── public/

</tr>

    └── typebot-grievance-flow.html  # Embed example

<tr>

<td><b>Typebot "Test" Button Error</b><br><code>Error! Could not reach server</code></td>**File:** `typebot-export-grievance-intake-qwdn4no.json````

<td>

✅ <b>Use "Publish" instead of "Test"</b><br>

1. Click "Publish" in Typebot Builder<br>

2. Access bot via the published URL<br>```json### Environment Variables

3. Webhooks work correctly in published mode<br>

<br>{

<i>Reason: Content Security Policy (CSP) blocks HTTP in preview mode</i>

</td>  "isExecutedOnClient": false,**Backend** (`.env`):

</tr>

  "webhook": {```bash

<tr>

<td><b>CORS Errors</b><br><code>No 'Access-Control-Allow-Origin' header</code></td>    "url": "http://grievance-api:8000/api/grievances",DATABASE_URL=postgresql://grievance:grievance@db:5432/grievance

<td>

✅ <b>Already Fixed!</b> Custom CORS middleware handles all origins<br>    "method": "POST",REDIS_URL=redis://redis:6379/0

- Supports <code>null</code> origin (file:// protocol)<br>

- Handles OPTIONS preflight requests<br>    "headers": [MINIO_ENDPOINT=minio:9000

- Works with server-side and client-side webhooks

</td>      {"key": "Content-Type", "value": "application/json"}MINIO_ACCESS_KEY=minioadmin

</tr>

    ]MINIO_SECRET_KEY=minioadmin

<tr>

<td><b>Network Connectivity</b><br>Typebot can't reach API</td>  }```

<td>

<b>Ensure network exists:</b><br>}

<code>docker network create grievance_net</code><br>

<code>docker compose up -d</code><br>```**Typebot** (configured in `docker-compose.yml`):

<br>

<b>Verify configuration:</b><br>- Database: `postgresql://typebot:typebot@typebot-db:5432/typebot`

<code>docker network inspect grievance_net</code><br>

Should show: api, typebot-builder, typebot-viewer✅ **Use this for:**- Encryption: `ENCRYPTION_SECRET` (required for webhooks)

</td>

</tr>- Production deployments- SMTP: MailHog on port 1025



<tr>- Published bots- Storage: MinIO S3

<td><b>Service won't start</b><br>Port already in use</td>

<td>- Server-side execution (more secure)

<b>Check ports:</b><br>

<code>netstat -ano | findstr :8000</code> (Windows)<br>### Key Features

<code>lsof -i :8000</code> (macOS/Linux)<br>

<br>### 🟢 Development Setup (Browser webhooks)

<b>Or change ports in docker-compose.yml</b>

</td>**Attachment Handling**:

</tr>

</table>**File:** `typebot-export-grievance-intake-LOCALHOST-TEST.json`- Supports single or multiple files



### 🗄 Database Management- Validation: max 10MB per file, 25MB total, max 5 files



<details>```json- Stores URLs from Typebot's S3 storage

<summary><b>Reset all data</b> (⚠️ destructive operation)</summary>

{- Converts Pydantic `AttachmentIn` objects or dicts

<br>

  "isExecutedOnClient": true,

```bash

# Stop and remove all containers, networks, and volumes  "webhook": {**ID Generation**:

docker compose down -v

    "url": "http://localhost:8000/api/grievances"- ULID format: `GRV-01ABC123...` (26 characters)

# Rebuild and start fresh

docker compose up -d --build  }- Sortable, unique, URL-safe

```

}

</details>

```**PDF Receipts**:

<details>

<summary><b>Access PostgreSQL databases</b></summary>- Auto-generated with grievance details



<br>✅ **Use this for:**- Includes QR code for tracking



```bash- Local development- Downloadable via `/api/grievances/{id}/receipt.pdf`

# Access grievance database

docker exec -it grievancemodule-db-1 psql -U grievance -d grievance- Browser testing



# Access Typebot database- Debugging webhook payloads**Anti-Spam**:

docker exec -it grievancemodule-typebot-db-1 psql -U typebot -d typebot

- Honeypot field

# Useful SQL commands:

# \dt              - List tables### 🛡 CORS Configuration- Timing validation (min 3 seconds)

# \d+ table_name   - Describe table

# SELECT * FROM grievances LIMIT 10;- Math challenge for suspicious submissions

```

Custom middleware automatically handles:

</details>

- ✅ All origins including `null` (file:// protocol)## Troubleshooting

<details>

<summary><b>View service logs</b></summary>- ✅ OPTIONS preflight requests



<br>- ✅ Browser-based webhook execution### Typebot "Test" Button Error



```bash- ✅ Typebot client-side mode

# API logs

docker compose logs -f api**Symptom**: "Error! Could not reach server" when clicking Test button



# Typebot Viewer logs```python

docker compose logs -f typebot-viewer

# Middleware in backend/app/main.py**Cause**: Content Security Policy (CSP) blocks `http://` in preview mode

# All services

docker compose logs -f@app.middleware("http")



# Last 100 linesasync def custom_cors_middleware(request: Request, call_next):**Solution**: Use **"Publish"** button instead:

docker compose logs --tail=100 api

    origin = request.headers.get("origin", "*")1. Click "Publish" (not "Test")

# Filter for errors

docker compose logs api | grep ERROR    # Automatically adds appropriate CORS headers2. Access bot via public URL

```

```3. Webhooks work correctly in published mode

</details>



<details>

<summary><b>Restart individual services</b></summary>---### CORS Errors



<br>



```bash## 💻 Development**Symptom**: "No 'Access-Control-Allow-Origin' header"

# Restart API

docker compose restart api



# Restart Typebot services### 📁 Project Structure**Status**: ✅ Fixed - Custom CORS middleware accepts all origins

docker compose restart typebot-builder typebot-viewer



# Restart database

docker compose restart db```**Details**: 

```

grievance-module/- Handles `null` origin (file:// protocol)

</details>

│- Supports OPTIONS preflight requests

---

├── 📂 backend/- Works with both server-side and client-side webhooks

## 🚀 Production Deployment

│   ├── 📂 app/

### ✅ Prerequisites Checklist

│   │   ├── main.py              # FastAPI app + CORS middleware### Network Connectivity

- [ ] **HTTPS/SSL certificates** (required for Typebot)

- [ ] **Domain names** configured (e.g., api.example.com, bot.example.com)│   │   ├── database.py          # SQLAlchemy configuration

- [ ] **Managed PostgreSQL** database set up

- [ ] **S3-compatible storage** (AWS S3, DigitalOcean Spaces, etc.)│   │   ├── models.py            # Database ORM models**Symptom**: Typebot can't reach API

- [ ] **Email service** (SendGrid, AWS SES, Mailgun)

- [ ] **Strong secrets** generated for all services│   │   ├── schemas.py           # Pydantic validation schemas

- [ ] **Firewall rules** configured (allow only necessary ports)

- [ ] **Monitoring & alerting** system in place│   │   ├── 📂 routers/**Solution**: Ensure `grievance_net` network exists:

- [ ] **Backup strategy** implemented

- [ ] **CI/CD pipeline** configured│   │   │   ├── grievances.py    # Grievance CRUD endpoints```bash



### ⚙️ Production Configuration│   │   │   └── status.py        # System status endpointsdocker network create grievance_net



<details>│   │   └── 📂 utils/docker compose up -d

<summary><b>Environment Variables</b></summary>

│   │       ├── id.py            # ULID generator (GRV-01ABC...)```

<br>

│   │       └── pdf.py           # PDF receipt generator

```bash

####################│   ├── 📂 tests/**Verify**:

# API Configuration

####################│   │   ├── test_api.py                    # 26 general API tests```bash



# Database (use managed PostgreSQL)│   │   └── test_typebot_integration.py    # 15 Typebot testsdocker network inspect grievance_net

DATABASE_URL=postgresql://user:strong_password@db-host.example.com:5432/grievance?sslmode=require

│   ├── Dockerfile# Should show: api, typebot-builder, typebot-viewer

# Cache (use managed Redis)

REDIS_URL=redis://redis-host.example.com:6379/0?ssl=true│   └── requirements.txt```



# Object Storage (use AWS S3 or similar)│

MINIO_ENDPOINT=s3.amazonaws.com

MINIO_ACCESS_KEY=<aws-access-key-id>├── 📂 frontend-typebot/### Database Issues

MINIO_SECRET_KEY=<aws-secret-access-key>

MINIO_BUCKET=prod-grievances│   ├── typebot-export-grievance-intake-qwdn4no.json         # Production

MINIO_SECURE=true

│   ├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development**Reset databases**:

# API Settings

DEBUG=false│   └── 📂 public/```bash

API_VERSION=0.1.0

SECRET_KEY=<64-character-random-string>│       └── typebot-grievance-flow.html    # Embed exampledocker compose down -v  # Warning: deletes all data



# CORS (restrict to specific domains in production)│docker compose up -d

ALLOWED_ORIGINS=https://bot.example.com,https://builder.example.com

├── 📂 docs/                      # Documentation & diagrams```

####################

# Typebot Configuration├── 📂 ops/                       # CI/CD workflows

####################

├── docker-compose.yml            # Service orchestration**Access PostgreSQL**:

# Core Settings

DATABASE_URL=postgresql://typebot:strong_password@typebot-db.example.com:5432/typebot?sslmode=require└── README.md                     # You are here!```bash

ENCRYPTION_SECRET=<64-character-random-string>

NEXTAUTH_URL=https://builder.example.com```# Grievance DB

NEXT_PUBLIC_VIEWER_URL=https://bot.example.com

ADMIN_EMAIL=admin@example.comdocker exec -it grievancemodule-db-1 psql -U grievance -d grievance

DISABLE_SIGNUP=true  # Disable public signups in production

### 🔧 Environment Variables

# SMTP (use real email service)

SMTP_HOST=smtp.sendgrid.net# Typebot DB

SMTP_PORT=587

SMTP_USERNAME=apikey<details>docker exec -it grievancemodule-typebot-db-1 psql -U typebot -d typebot

SMTP_PASSWORD=<sendgrid-api-key>

SMTP_SECURE=true<summary><b>Backend Configuration</b> (<code>.env</code>)</summary>```

NEXT_PUBLIC_SMTP_FROM=noreply@example.com



# Storage

S3_ACCESS_KEY=<aws-access-key-id>```bash## Production Deployment

S3_SECRET_KEY=<aws-secret-access-key>

S3_BUCKET=prod-typebot# Database

S3_ENDPOINT=s3.amazonaws.com

S3_SSL=trueDATABASE_URL=postgresql://grievance:grievance@db:5432/grievance### Prerequisites

NEXT_PUBLIC_S3_ENDPOINT=https://cdn.example.com

```



</details># Cache1. Set up HTTPS (required for Typebot)



### 🔒 Security ChecklistREDIS_URL=redis://redis:6379/02. Configure domain names



**Before going live:**3. Update environment variables



- [ ] Change all default passwords# Object Storage4. Set strong secrets

- [ ] Enable SSL/TLS for all connections (PostgreSQL, Redis)

- [ ] Configure proper SMTP credentialsMINIO_ENDPOINT=minio:9000

- [ ] Set up automated database backups (daily minimum)

- [ ] Enable API rate limiting (e.g., 100 requests/minute)MINIO_ACCESS_KEY=minioadmin### Configuration

- [ ] Configure firewall rules (allow only 80, 443, and admin access)

- [ ] Set up SSL certificates for all domains (Let's Encrypt or commercial)MINIO_SECRET_KEY=minioadmin

- [ ] Enable HTTPS redirect (HTTP → HTTPS)

- [ ] Configure CORS for specific production domains onlyMINIO_BUCKET=grievances**Environment Variables**:

- [ ] Review and update security headers (CSP, HSTS, X-Frame-Options)

- [ ] Set up intrusion detection (fail2ban or similar)```bash

- [ ] Enable container security scanning

- [ ] Implement log monitoring and alerting# API# API

- [ ] Set up DDoS protection (Cloudflare or AWS Shield)

- [ ] Review and harden Docker securityDEBUG=TrueDATABASE_URL=postgresql://user:pass@db-host:5432/grievance



### 📊 Monitoring & Health ChecksAPI_VERSION=0.1.0MINIO_ENDPOINT=s3.example.com



#### Health Endpoints```



```bash# Typebot

# API health check

curl https://api.example.com/</details>NEXTAUTH_URL=https://builder.example.com

# Expected: {"ok": true, "service": "Grievance Management API", "version": "0.1.0"}

NEXT_PUBLIC_VIEWER_URL=https://bot.example.com

# System status

curl https://api.example.com/api/status<details>ENCRYPTION_SECRET=<64-char-random-string>

# Expected: {"status": "ok", "database": "connected", "redis": "connected"}

<summary><b>Typebot Configuration</b> (in <code>docker-compose.yml</code>)</summary>ADMIN_EMAIL=admin@example.com

# Typebot health

curl https://bot.example.com/DISABLE_SIGNUP=true

# Expected: 200 OK

``````yaml



#### Logging & Monitoring# Core Settings# SMTP (real email service)



```bashDATABASE_URL: postgresql://typebot:typebot@typebot-db:5432/typebotSMTP_HOST=smtp.sendgrid.net

# Production logs (if using Docker Compose)

docker compose -f docker-compose.prod.yml logs -f --tail=100 apiENCRYPTION_SECRET: <64-character-random-string>SMTP_PORT=587



# Error monitoringNEXTAUTH_URL: http://localhost:8081SMTP_USERNAME=apikey

docker compose logs api | grep ERROR

NEXT_PUBLIC_VIEWER_URL: http://localhost:8082SMTP_PASSWORD=<api-key>

# Access logs (track API usage)

docker compose logs api | grep POST```



# Performance monitoring# Email (MailHog for testing)

docker stats grievancemodule-api-1

```SMTP_HOST: mailhog**Security**:



**Recommended monitoring tools:**SMTP_PORT: 1025- [ ] Change default passwords

- 📊 **Application Performance Monitoring:** New Relic, Datadog, or Sentry

- 🚨 **Alerting:** PagerDuty or OpsgenieSMTP_USERNAME: x- [ ] Enable SSL/TLS for PostgreSQL

- 📈 **Metrics:** Prometheus + Grafana

- 📝 **Log aggregation:** ELK Stack (Elasticsearch, Logstash, Kibana) or LokiSMTP_PASSWORD: x- [ ] Configure proper SMTP credentials



### 📈 Performance OptimizationNEXT_PUBLIC_SMTP_FROM: noreply@typebot.local- [ ] Set up backup strategy



**For production workloads:**- [ ] Enable API rate limiting



1. **Database Optimization**# Storage (MinIO)- [ ] Configure firewall rules

   - Enable connection pooling (SQLAlchemy default: 5-10 connections)

   - Add indexes for frequently queried fields (`id`, `created_at`, `island`, `district`)S3_ACCESS_KEY: minioadmin

   - Regular VACUUM and ANALYZE operations

   - Consider read replicas for high trafficS3_SECRET_KEY: minioadmin### Monitoring



2. **Caching Strategy**S3_BUCKET: typebot

   - Configure Redis for session storage and API response caching

   - Cache static content (PDF receipts after generation)S3_ENDPOINT: minio**Health Checks**:

   - Implement cache invalidation strategy

S3_PORT: 9000```bash

3. **CDN & Static Assets**

   - Serve static files through CDN (CloudFront, Cloudflare)NEXT_PUBLIC_S3_ENDPOINT: http://localhost:9000# API

   - Enable gzip/brotli compression

   - Optimize images and assets```curl https://api.example.com/



4. **API Optimization**

   - Implement pagination for large datasets (default: 50 items per page)

   - Use database query optimization (select only needed fields)</details># Typebot

   - Enable async workers for long-running tasks (PDF generation, emails)

curl https://bot.example.com/

5. **Infrastructure**

   - Use container orchestration (Kubernetes or AWS ECS) for auto-scaling### ✨ Key Features```

   - Configure horizontal pod autoscaling based on CPU/memory

   - Set up load balancing for high availability



---#### 📎 Attachment Handling**Logs**:



## 📄 License- Multiple file uploads (max 5 files)```bash



This project is licensed under the terms specified in the [`LICENSE`](LICENSE) file.- Size validation (10MB per file, 25MB total)docker compose logs -f api



---- Supported formats: `.jpg`, `.png`, `.pdf`, `.docx`, `.xlsx`docker compose logs -f typebot-viewer



## 🤝 Contributing- Stores URLs from MinIO S3 storage```



We welcome contributions! Please follow these guidelines:- Handles both Pydantic objects and raw dicts



### Development Workflow## License



1. **Fork & Clone** the repository#### 🆔 ID Generation

2. **Create a feature branch:** `git checkout -b feature/amazing-feature`

3. **Make your changes** with clear, descriptive commits- **Format:** `GRV-01ABC123...` (26 characters)See `LICENSE` file for details.

4. **Run tests:** `docker exec grievancemodule-api-1 pytest`

5. **Ensure all tests pass** (41/41 should be green ✅)- **Technology:** ULID (Universally Unique Lexicographically Sortable Identifier)

6. **Submit a Pull Request** with a clear description

- **Benefits:** Sortable, unique, URL-safe, timestamp-embedded## Contributing

### Code Standards



- ✅ Follow **PEP 8** style guide for Python

- ✅ Write **meaningful commit messages**#### 📄 PDF Receipt Generation1. Run tests before submitting PRs

- ✅ Add **tests for new features** (maintain or increase coverage)

- ✅ Update **documentation** for API changes- Auto-generated with grievance details2. Follow existing code style

- ✅ Use **type hints** for Python code

- ✅ Keep functions **small and focused**- Includes QR code for easy tracking3. Update tests for new features



### Pull Request Checklist- Professional formatting4. Document API changes



- [ ] Tests pass (`pytest`)- Downloadable via `/api/grievances/{id}/receipt.pdf`

- [ ] Code follows style guidelines

- [ ] Documentation updated#### 🛡 Anti-Spam Protection

- [ ] No new warnings or errors- 🍯 Honeypot field (invisible to humans)

- [ ] Commits are clean and descriptive- ⏱️ Timing validation (minimum 3 seconds)

- 🧮 Math challenge for suspicious submissions

---- 🚫 Rate limiting (configurable)



<div align="center">---



### 🌟 Built With## 🔧 Troubleshooting



[FastAPI](https://fastapi.tiangolo.com) · [PostgreSQL](https://www.postgresql.org) · [Typebot](https://typebot.io) · [MinIO](https://min.io) · [Redis](https://redis.io) · [Docker](https://www.docker.com)### ⚠️ Typebot "Test" Button Error



<br><table>

<tr>

**Made with ❤️ for Vaka Sosiale**<td width="30%"><b>Symptom</b></td>

<td><code>Error! Could not reach server. Check your connection. {}</code></td>

<br></tr>

<tr>

[![Report Bug](https://img.shields.io/badge/🐛-Report%20Bug-red?style=for-the-badge)](https://github.com/gger-max/grievance-module/issues)<td><b>Cause</b></td>

[![Request Feature](https://img.shields.io/badge/✨-Request%20Feature-blue?style=for-the-badge)](https://github.com/gger-max/grievance-module/issues)<td>Content Security Policy (CSP) blocks HTTP in preview mode</td>

[![Documentation](https://img.shields.io/badge/📚-Documentation-green?style=for-the-badge)](http://localhost:8000/docs)</tr>

<tr>

</div><td><b>Solution</b></td>

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
