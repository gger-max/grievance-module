<div align="center">

#  Grievance Management System

### _Modern, scalable grievance tracking for Vaka Sosiale_

<br>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/Tests-41%20passing-success.svg?style=flat)](backend/tests/)

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

**Features:** ULID IDs  PDF Receipts  Multi-file attachments  Anti-spam  Custom CORS

##  Testing

```bash
docker exec grievancemodule-api-1 pytest
docker exec grievancemodule-api-1 pytest backend/tests/test_typebot_integration.py -v
```

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/grievances` | Create |
| GET | `/api/grievances/{id}` | Get by ID |
| GET | `/api/grievances/{id}/receipt.pdf` | Download PDF |
| PATCH | `/api/grievances/{id}` | Update |

##  Typebot

**Production:** `typebot-export-grievance-intake-qwdn4no.json` (server-side)  
**Development:** `typebot-export-grievance-intake-LOCALHOST-TEST.json` (browser)

##  Troubleshooting

| Issue | Solution |
|-------|----------|
| Typebot Test Error | Use "Publish" not "Test" |
| CORS Errors | Fixed with custom middleware |
| Network Issues | `docker network create grievance_net` |

##  Deployment

See full docs for production configuration, security checklist, and monitoring setup.

---

<div align="center">

**Built with  for Vaka Sosiale**

FastAPI  PostgreSQL  Typebot  MinIO  Redis  Docker

</div>