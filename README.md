Monorepo for the **Vaka Sosiale** GRM. It captures grievances via Typebot, processes and classifies them through a FastAPI middleware, stores data in PostgreSQL/MinIO, and integrates with Vaka Sosiale for analytics and feedback.

<p align="center">
  <img src="docs/images/figure-10-grm-architecture.png" alt="GRM System Architecture Overview" width="720">
</p>

## Repository layout
# grievance-module/
# ├─ backend/ # FastAPI app, tests, Dockerfile
# ├─ frontend-typebot/ # Typebot export, embed snippets, docs
# ├─ infra/ # docker-compose, .env.example, local run
# ├─ ops/ # CI/CD workflows and helper scripts
# ├─ docs/ # report docs, images, diagrams
# ├─ .github/workflows/ # GitHub Actions
# ├─ .gitignore
# ├─ .gitattributes
# ├─ LICENSE
# ├─ README.md
# └─ SECURITY.md

## Quick start (local)

```bash
# 1) Start infra (DB/Redis/MinIO) + API + Typebot* (optional)
cd infra
cp .env.example .env
# edit values, then:
docker compose up -d

# 2) Visit:
# API docs:          http://localhost:8000/docs
# Typebot Builder*:  http://localhost:8081
# Typebot Viewer*:   http://localhost:8082
# MinIO Console:     http://localhost:9001