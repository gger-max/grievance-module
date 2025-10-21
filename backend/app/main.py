from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import grievances
from .database import init_db

app = FastAPI(title="Grievance FrontEnd API", version="0.1.0")

# Allow embedding/testing; tighten in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js
        "http://localhost:8081",  # Typebot Builder (optional)
        "http://localhost:8082",  # Typebot Viewer
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(grievances.router, prefix="/api", tags=["grievances"])

@app.get("/")
def root():
    return {"ok": True, "service": "Grievance FrontEnd API"}