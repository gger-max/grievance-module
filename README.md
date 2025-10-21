<div align="center"><div align="center"># Grievance Management System.



# 🎯 Grievance Management System



### _Modern, scalable grievance tracking for Vaka Sosiale_# 🎯 Grievance Management SystemMonorepo for the **Vaka Sosiale** GRM. It captures grievances via Typebot, processes and classifies them through a FastAPI middleware, stores data in PostgreSQL/MinIO, and integrates with Vaka Sosiale for analytics and feedback.<p align="center">



[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)### _Modern, scalable grievance tracking for Vaka Sosiale_  <img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture Overview" width="720">

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)

[![Tests](https://img.shields.io/badge/Tests-41%20passing-success.svg?style=flat)](backend/tests/)



<br>[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)<p align="center"></p>



<img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture" width="800">[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)



<br>[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)## Repository layout



**Capture grievances via Typebot chatbot** · **Process through FastAPI middleware** · **Store in PostgreSQL/MinIO** · **Integrate with analytics**[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)



<br>[![Tests](https://img.shields.io/badge/Tests-41%20passing-success.svg?style=flat)](backend/tests/)grievance-module/# 



[Quick Start](#-quick-start) • [Architecture](#-architecture) • [Testing](#-testing) • [API Docs](#-api-endpoints) • [Deployment](#-production-deployment)



</div>---├── backend/              # FastAPI app, tests, Dockerfile# 



---├── frontend-typebot/     # Typebot export, embed snippets, docs# 



## 📋 Table of Contents<img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture" width="800">├── infra/                # docker-compose, .env.example, local run# 



- [🚀 Quick Start](#-quick-start)├── ops/                  # CI/CD workflows and helper scripts# 

- [🏗 Architecture](#-architecture)

- [🧪 Testing](#-testing)**Capture grievances via Typebot chatbot** · **Process through FastAPI middleware** · **Store in PostgreSQL/MinIO** · **Integrate with analytics**├── docs/                 # report docs, images, diagrams# 

- [📡 API Endpoints](#-api-endpoints)

- [🤖 Typebot Configuration](#-typebot-configuration)├── .github/workflows/    # GitHub Actions# 

- [💻 Development](#-development)

- [🔧 Troubleshooting](#-troubleshooting)[Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Docs](#-api-endpoints) • [Testing](#-testing) • [Deployment](#-production-deployment)├── .gitignore# 

- [🚀 Production Deployment](#-production-deployment)

├── .gitattributes

---

</div>├── LICENSE## Quick start (local)

## 🚀 Quick Start

├── README.md

Get up and running in 3 simple steps:

---└── SECURITY.md

```bash

# Step 1: Create Docker network for service communication

docker network create grievance_net

## 📋 Table of Contents```bash

# Step 2: Start all services

docker compose up -d --build# 1) Start infra (DB/Redis/MinIO) + API + Typebot* (optional)



# Step 3: Access the services ✨- [Quick Start](#-quick-start)

```

- [Architecture](#-architecture)cd infra

### 🌐 Service URLs

- [Testing](#-testing)

| Service | URL | Description |

|---------|-----|-------------|- [API Endpoints](#-api-endpoints)## Quick Start (Local)cp .env.example .env

| 📚 **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |

| 🤖 **Typebot Builder** | http://localhost:8081 | Design bot flows |- [Typebot Configuration](#-typebot-configuration)

| 💬 **Typebot Viewer** | http://localhost:8082 | Public bot interface |

| 📦 **MinIO Console** | http://localhost:9001 | S3 storage management |- [Development](#-development)# edit values, then:

| 📧 **MailHog** | http://localhost:8025 | Email testing UI |

- [Troubleshooting](#-troubleshooting)

---

- [Production Deployment](#-production-deployment)bashdocker compose up -d

## 🏗 Architecture



### Service Overview

---# 1) Create external Docker network for API-Typebot communication

<table>

<tr>

<td width="50%" valign="top">

## 🚀 Quick Startdocker network create grievance_net# 2) Visit:

#### 🔥 **FastAPI Backend**



**Location:** `backend/`

Get up and running in 3 simple steps:# API docs:          http://localhost:8000/docs

**Endpoints:** 

- `/api/grievances` - CRUD operations

- `/api/status` - System health

```bash# 2) Start all services (DB/Redis/MinIO/API/Typebot)# Typebot Builder*:  http://localhost:8081

**Features:**

- ✅ RESTful API with FastAPI# Step 1: Create Docker network for service communication

- ✅ PDF receipt generation

- ✅ File attachment handlingdocker network create grievance_netdocker compose up -d --build# Typebot Viewer*:   http://localhost:8082

- ✅ Custom CORS middleware

- ✅ ULID-based IDs



**Stack:**# Step 2: Start all services# MinIO Console:     http://localhost:9001

- PostgreSQL (data)

- MinIO (files)docker compose up -d --build# 3) Visit:

- Redis (cache)

# API docs:          http://localhost:8000/docs

**Tests:** 🎯 41 passing

- 26 general API tests# Step 3: Access the services# Typebot Builder:   http://localhost:8081

- 15 Typebot integration tests

```# Typebot Viewer:    http://localhost:8082

</td>

<td width="50%" valign="top"># MinIO Console:     http://localhost:9001



#### 🤖 **Typebot Chatbot**### 🌐 Service URLs# MailHog (email):   http://localhost:8025



**Location:** `frontend-typebot/````



**Ports:** | Service | URL | Description |

- 8081 (Builder)

- 8082 (Viewer)|---------|-----|-------------|## Architecture



**Modes:**| 📚 **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |

- 🔵 **Production:** Server-side webhooks

- 🟢 **Development:** Browser webhooks| 🤖 **Typebot Builder** | http://localhost:8081 | Design bot flows |### Services



**Features:**| 💬 **Typebot Viewer** | http://localhost:8082 | Public bot interface |

- 🎨 No-code bot designer

- 🔗 Webhook integration| 📦 **MinIO Console** | http://localhost:9001 | S3 storage management |- **FastAPI Backend** (`backend/`): REST API for grievance management

- 📎 File upload support

- 🌍 Multi-language support| 📧 **MailHog** | http://localhost:8025 | Email testing UI |  - Endpoints: `/api/grievances`, `/api/status`

- 📧 Email notifications

- 🛡️ Anti-spam protection  - Features: CRUD operations, PDF receipt generation, attachment handling



**Integration:**---  - Storage: PostgreSQL + MinIO (S3-compatible)

- Connects via `grievance_net`

- Seamless API communication  - Tests: 41 passing tests (26 general + 15 Typebot integration)

- Two export configurations

## 🏗 Architecture

</td>

</tr>- **Typebot** (`frontend-typebot/`): No-code chatbot for grievance intake

</table>

### Service Overview  - Builder (port 8081): Design and configure bot flows

### 💾 Data & Infrastructure

  - Viewer (port 8082): Public-facing bot interface

| Service | Port(s) | Purpose | Technology |

|---------|---------|---------|------------|<table>  - Two export versions:

| **PostgreSQL** (grievance) | 5432 | Main grievance data | PostgreSQL 16 |

| **PostgreSQL** (typebot) | 5433 | Typebot configuration | PostgreSQL 16 |<tr>    - `typebot-export-grievance-intake-qwdn4no.json`: Production (server-side webhooks)

| **MinIO** | 9000 / 9001 | S3-compatible file storage | MinIO latest |

| **Redis** | 6379 | Caching & sessions | Redis 7 |<td width="50%">    - `typebot-export-grievance-intake-LOCALHOST-TEST.json`: Development (browser webhooks)

| **MailHog** | 1025 / 8025 | Email testing (SMTP + UI) | MailHog latest |



### 🌐 Network Architecture

#### 🔥 **FastAPI Backend**- **PostgreSQL**: Two databases

```

┌─────────────────┐- **Location:** `backend/`  - `grievance` (port 5432): Main grievance data

│  User Browser   │

└────────┬────────┘- **Endpoints:** `/api/grievances`, `/api/status`  - `typebot` (port 5433): Typebot configuration

         │ HTTP

         ▼- **Features:**

┌─────────────────┐     grievance_net      ┌──────────────┐

│ Typebot Viewer  ├────────────────────────►│   FastAPI    │  - ✅ CRUD operations- **MinIO** (ports 9000/9001): S3-compatible object storage for attachments

│   (port 8082)   │                         │  (port 8000) │

└─────────────────┘                         └──────┬───────┘  - ✅ PDF receipt generation

                                                   │ default network

                    ┌──────────────────────────────┼────────────┐  - ✅ File attachment handling- **Redis** (port 6379): Caching and session storage

                    ▼                              ▼            ▼

            ┌──────────────┐            ┌────────────┐  ┌───────────┐  - ✅ Custom CORS middleware

            │  PostgreSQL  │            │   MinIO    │  │   Redis   │

            │  (port 5432) │            │ (port 9000)│  │ (port 6379)│- **Storage:** PostgreSQL + MinIO- **MailHog** (ports 1025/8025): Email testing (SMTP + web UI)

            └──────────────┘            └────────────┘  └───────────┘

```- **Tests:** 41 passing (26 general + 15 Typebot)



**Network Details:**### Networking

- 🔵 **`default`** (auto-created): Internal service communication (DB, Redis, MinIO)

- 🟢 **`grievance_net`** (external): Typebot ↔ API communication</td>

  - API accessible as `grievance-api:8000` from Typebot services

<td width="50%">The system uses two Docker networks:

---



## 🧪 Testing

#### 🤖 **Typebot Chatbot**1. **`default`** (auto-created): Internal service communication

### Run Backend Tests

- **Location:** `frontend-typebot/`2. **`grievance_net`** (external): Enables Typebot → API communication

```bash

# Run all 41 tests- **Ports:** 8081 (Builder), 8082 (Viewer)   - API is accessible as `grievance-api:8000` from Typebot services

docker exec grievancemodule-api-1 pytest

- **Modes:**

# Run Typebot integration tests only (15 tests)

docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py -v  - 🔵 **Production:** Server-side webhooks## Testing



# Run with coverage report  - 🟢 **Development:** Browser webhooks

docker exec grievancemodule-api-1 pytest --cov=app --cov-report=html

- **Features:**### Run Backend Tests

# View coverage

open backend/htmlcov/index.html  # macOS/Linux  - No-code bot designer

start backend/htmlcov/index.html  # Windows

```  - Webhook integration```bash



### 🤖 Test Typebot Integration  - File upload support# All tests (41 total)



#### **Method 1: Published Bot** ⭐ _Recommended_  - Multi-language supportdocker exec grievancemodule-api-1 pytest



1. Open Typebot Builder: http://localhost:8081

2. Import: `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

3. Click **"Publish"** button (⚠️ not "Test" - CSP restrictions)</td># Typebot integration tests only (15 tests)

4. Open the published bot URL in a new tab

5. Complete the flow and submit a test grievance</tr>docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py

6. Verify: Check API response and database entry

</table>

#### **Method 2: Browser Testing**

# With coverage

1. Open `test-browser-webhook.html` in your browser

2. Click **"Test Webhook"** button### 💾 Data Layerdocker exec grievancemodule-api-1 pytest --cov=app

3. Check console for success message

4. Verify grievance created with API call```



### ✅ Test Coverage Summary| Service | Port | Purpose |



<details>|---------|------|---------|### Test Typebot Integration

<summary><b>📊 Typebot Integration Tests</b> (15 tests in <code>test_typebot_integration.py</code>)</summary>

| **PostgreSQL** (grievance) | 5432 | Main grievance data |

<br>

| **PostgreSQL** (typebot) | 5433 | Typebot configuration |**Option 1: Published Bot (Recommended)**

#### ✅ Core Functionality (5 tests)

- Field mapping (Typebot schema → API schema)| **MinIO** | 9000/9001 | S3-compatible file storage |1. Open Typebot Builder: http://localhost:8081

- Complainant information (name, email, phone, gender)

- Location data (island, district, village)| **Redis** | 6379 | Caching & sessions |2. Import `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

- Category types

- Grievance details and descriptions| **MailHog** | 1025/8025 | Email testing (SMTP + UI) |3. Click **"Publish"** (not "Test" - CSP restrictions apply to preview mode)



#### ✅ File Handling (3 tests)4. Access published bot URL

- Single file attachment

- Multiple file attachments### 🌐 Network Architecture5. Submit a grievance - webhook executes server-side

- Attachment validation & size limits



#### ✅ User Flows (4 tests)

- Anonymous submissions```mermaid**Option 2: Browser Testing**

- Named submissions with full details

- Household registration flowgraph LR1. Open `test-browser-webhook.html` in browser

- Status lookup by grievance ID

    A[User Browser] -->|HTTP| B[Typebot Viewer]2. Click "Test Webhook"

#### ✅ Features (3 tests)

- PDF receipt generation    B -->|grievance_net| C[FastAPI]3. Simulates client-side webhook execution with CORS

- Email notifications

- Error handling & validation    C -->|default| D[PostgreSQL]



</details>    C -->|default| E[MinIO]### Test Coverage



---    C -->|default| F[Redis]



## 📡 API Endpoints    G[Typebot Builder] -->|grievance_net| C**Typebot Integration Tests** (`test_typebot_integration.py`):



### 📝 Grievances```- ✅ Field mapping (Typebot → API schema)



<details>- ✅ Complainant information handling

<summary><b>POST</b> <code>/api/grievances</code> - Create a new grievance</summary>

**Two Docker Networks:**- ✅ Location data (island, district, village)

<br>

- 🔵 **`default`** (auto-created): Internal service communication- ✅ Category types

**Request:**

```bash- 🟢 **`grievance_net`** (external): Typebot ↔ API communication- ✅ Attachment handling (single & multiple files)

curl -X POST http://localhost:8000/api/grievances \

  -H "Content-Type: application/json" \  - API accessible as `grievance-api:8000` from Typebot- ✅ Anonymous submissions

  -d '{

    "is_anonymous": false,- ✅ Named submissions with full details

    "complainant_name": "John Doe",

    "complainant_email": "john@example.com",---- ✅ Household registration flow

    "complainant_phone": "+676123456",

    "complainant_gender": "Male",- ✅ Status lookup by grievance ID

    "is_hh_registered": true,

    "hh_id": "HH12345",## 🧪 Testing- ✅ PDF receipt generation

    "hh_address": "Main Street, Kolofo'\''ou",

    "island": "Tongatapu",- ✅ Email notifications

    "district": "Nuku'\''alofa",

    "village": "Kolofo'\''ou",### Run Backend Tests- ✅ Error handling and validation

    "category_type": "Registration",

    "details": "Need assistance with registration renewal",

    "attachments": [

      {```bash## Typebot Configuration

        "name": "document.pdf",

        "url": "https://storage.example.com/file.pdf",# Run all 41 tests

        "size": 102400,

        "type": "application/pdf"docker exec grievancemodule-api-1 pytest### Production Setup (Server-side webhooks)

      }

    ]

  }'

```# Run Typebot integration tests only (15 tests)File: `typebot-export-grievance-intake-qwdn4no.json`



**Response:** `201 Created`docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py -v

```json

{```json

  "id": "GRV-01K83WMY346N2S1KA7FK3W26RP",

  "created_at": "2025-10-21T12:00:00Z",# Run with coverage report{

  "updated_at": "2025-10-21T12:00:00Z",

  "is_anonymous": false,docker exec grievancemodule-api-1 pytest --cov=app --cov-report=html  "isExecutedOnClient": false,

  "complainant_name": "John Doe",

  "complainant_email": "john@example.com",```  "webhook": {

  "island": "Tongatapu",

  "district": "Nuku'alofa",    "url": "http://grievance-api:8000/api/grievances",

  "details": "Need assistance with registration renewal",

  ...### 🤖 Test Typebot Integration    "method": "POST",

}

```    "headers": [{"key": "Content-Type", "value": "application/json"}]



</details>#### **Option 1: Published Bot** ⭐ _Recommended_  }



<details>}

<summary><b>GET</b> <code>/api/grievances/{id}</code> - Get grievance by ID</summary>

1. Open Typebot Builder: http://localhost:8081```

<br>

2. Import `frontend-typebot/typebot-export-grievance-intake-qwdn4no.json`

```bash

curl http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP3. Click **"Publish"** button (⚠️ don't use "Test" - CSP restrictions)- Webhooks execute from Typebot Viewer container

```

4. Access the published bot URL- Uses Docker internal network (`grievance_net`)

**Response:** `200 OK` (full grievance object)

5. Submit a test grievance- API accessible as `grievance-api:8000`

</details>



<details>

<summary><b>GET</b> <code>/api/grievances/{id}/receipt.pdf</code> - Download PDF receipt</summary>#### **Option 2: Browser Testing**### Development Setup (Browser webhooks)



<br>



```bash1. Open `test-browser-webhook.html` in your browserFile: `typebot-export-grievance-intake-LOCALHOST-TEST.json`

curl -O http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP/receipt.pdf

```2. Click **"Test Webhook"** button



**Response:** `200 OK` (PDF file with QR code)3. Verify successful creation```json



</details>{



<details>### ✅ Test Coverage  "isExecutedOnClient": true,

<summary><b>PATCH</b> <code>/api/grievances/{id}</code> - Update grievance status</summary>

  "webhook": {

<br>

<details>    "url": "http://localhost:8000/api/grievances"

```bash

curl -X PATCH http://localhost:8000/api/grievances/GRV-01K83WMY346N2S1KA7FK3W26RP \<summary><b>Typebot Integration Tests</b> (15 tests in <code>test_typebot_integration.py</code>)</summary>  }

  -H "Content-Type: application/json" \

  -d '{}

    "external_status": "Under Review",

    "external_status_note": "Processing your request"#### Core Functionality```

  }'

```- ✅ Field mapping (Typebot schema → API schema)



**Response:** `200 OK` (updated grievance)- ✅ Complainant information (name, email, phone, gender)- Webhooks execute in user's browser



</details>- ✅ Location data (island, district, village)- Requires CORS configuration (already configured)



### 🏥 Health & Status- ✅ Category types- For testing in Typebot Builder environment



| Endpoint | Method | Description | Response |- ✅ Grievance details and descriptions

|----------|--------|-------------|----------|

| `/` | GET | API health check | `{"ok": true, "service": "Grievance Management API"}` |### CORS Configuration

| `/api/status` | GET | System status | `{"status": "ok", "database": "connected", ...}` |

#### File Handling

---

- ✅ Single file attachmentThe API uses custom CORS middleware to support:

## 🤖 Typebot Configuration

- ✅ Multiple file attachments- All origins including `null` (for `file://` protocol)

### 🔵 Production Setup (Server-side webhooks)

- ✅ Attachment validation- Browser-based webhook execution

**File:** `typebot-export-grievance-intake-qwdn4no.json`

- Typebot client-side mode

```json

{#### User Flows

  "isExecutedOnClient": false,

  "webhook": {- ✅ Anonymous submissions```python

    "url": "http://grievance-api:8000/api/grievances",

    "method": "POST",- ✅ Named submissions with full details# backend/app/main.py

    "headers": [

      {"key": "Content-Type", "value": "application/json"}- ✅ Household registration flow@app.middleware("http")

    ]

  }- ✅ Status lookup by grievance IDasync def custom_cors_middleware(request: Request, call_next):

}

```    origin = request.headers.get("origin", "*")



**✅ Use this for:**#### Features    # Handles OPTIONS preflight and adds CORS headers to all responses

- Production deployments

- Published bots- ✅ PDF receipt generation```

- Server-side execution (more secure)

- Docker internal network communication- ✅ Email notifications



### 🟢 Development Setup (Browser webhooks)- ✅ Error handling and validation## API Endpoints



**File:** `typebot-export-grievance-intake-LOCALHOST-TEST.json`- ✅ Anti-spam measures



```json### Grievances

{

  "isExecutedOnClient": true,</details>

  "webhook": {

    "url": "http://localhost:8000/api/grievances"**Create Grievance**

  }

}---```bash

```

POST /api/grievances

**✅ Use this for:**

- Local development## 📡 API EndpointsContent-Type: application/json

- Browser testing

- Debugging webhook payloads

- Client-side execution

### 📝 Grievances{

### 🛡 CORS Configuration

  "is_anonymous": true,

The API uses **custom CORS middleware** to support all integration scenarios:

<details>  "complainant_name": "John Doe",

**Automatically handles:**

- ✅ All origins including `null` (file:// protocol)<summary><b>POST</b> <code>/api/grievances</code> - Create a new grievance</summary>  "complainant_email": "john@example.com",

- ✅ OPTIONS preflight requests

- ✅ Browser-based webhook execution  "complainant_phone": "+676123456",

- ✅ Typebot client-side mode

- ✅ Cross-origin requests```bash  "complainant_gender": "Male",



**Implementation:**curl -X POST http://localhost:8000/api/grievances \  "is_hh_registered": false,

```python

# backend/app/main.py  -H "Content-Type: application/json" \  "hh_id": "HH123",

@app.middleware("http")

async def custom_cors_middleware(request: Request, call_next):  -d '{  "hh_address": "Main Street",

    origin = request.headers.get("origin", "*")

        "is_anonymous": false,  "island": "Tongatapu",

    if request.method == "OPTIONS":

        return Response(status_code=200, headers={    "complainant_name": "John Doe",  "district": "Nuku'alofa",

            "Access-Control-Allow-Origin": origin,

            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",    "complainant_email": "john@example.com",  "village": "Kolofo'ou",

            "Access-Control-Allow-Headers": "*",

        })    "complainant_phone": "+676123456",  "category_type": "Registration",

    

    response = await call_next(request)    "complainant_gender": "Male",  "details": "Issue description...",

    response.headers["Access-Control-Allow-Origin"] = origin

    return response    "is_hh_registered": true,  "attachments": [

```

    "hh_id": "HH12345",    {

---

    "hh_address": "Main Street, Kolofo'\''ou",      "name": "photo.jpg",

## 💻 Development

    "island": "Tongatapu",      "url": "https://...",

### 📁 Project Structure

    "district": "Nuku'\''alofa",      "size": 1024,

```

grievance-module/    "village": "Kolofo'\''ou",      "type": "image/jpeg"

│

├── 📂 backend/                           # FastAPI Application    "category_type": "Registration",    }

│   ├── 📂 app/

│   │   ├── main.py                      # FastAPI app + CORS middleware    "details": "Need assistance with registration renewal",  ]

│   │   ├── database.py                  # SQLAlchemy configuration

│   │   ├── models.py                    # Database ORM models    "attachments": [}

│   │   ├── schemas.py                   # Pydantic validation schemas

│   │   ├── 📂 routers/      {

│   │   │   ├── grievances.py           # Grievance CRUD endpoints

│   │   │   └── status.py               # System status endpoints        "name": "document.pdf",Response: 201 Created

│   │   └── 📂 utils/

│   │       ├── id.py                    # ULID generator (GRV-01ABC...)        "url": "https://storage.example.com/file.pdf",{

│   │       └── pdf.py                   # PDF receipt generator (with QR)

│   ├── 📂 tests/        "size": 102400,  "id": "GRV-01ABC123...",

│   │   ├── test_api.py                  # 26 general API tests

│   │   └── test_typebot_integration.py  # 15 Typebot integration tests        "type": "application/pdf"  "created_at": "2025-10-21T12:00:00Z",

│   ├── Dockerfile                       # Multi-stage Docker build

│   ├── requirements.txt                 # Python dependencies      }  ...

│   └── .env                            # Environment configuration

│    ]}

├── 📂 frontend-typebot/                  # Typebot Configuration

│   ├── typebot-export-grievance-intake-qwdn4no.json         # Production  }'```

│   ├── typebot-export-grievance-intake-LOCALHOST-TEST.json  # Development

│   ├── 📂 public/```

│   │   └── typebot-grievance-flow.html  # Embed example

│   └── test-browser-webhook.html        # Browser testing tool**Get Grievance**

│

├── 📂 docs/                              # Documentation & Diagrams**Response:** `201 Created````bash

│   └── 📂 images/

│       └── figure-10-grm-architecture.png```jsonGET /api/grievances/{id}

│

├── 📂 ops/                               # CI/CD & Operations{Response: 200 OK

│   └── 📂 github-actions/

│       ├── ci.yml                       # Continuous Integration  "id": "GRV-01K83WMY346N2S1KA7FK3W26RP",```

│       └── docker-api.yml               # Docker build & push

│  "created_at": "2025-10-21T12:00:00Z",

├── docker-compose.yml                    # Service orchestration

├── README.md                             # This file  "updated_at": "2025-10-21T12:00:00Z",**Download Receipt**

└── LICENSE                               # Project license

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
