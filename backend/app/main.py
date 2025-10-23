from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from .routers import grievances, status, categorization
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed
    pass


app = FastAPI(
    title="Grievance Management API",
    version="0.1.0",
    description="API for managing grievance submissions and tracking",
    lifespan=lifespan
)

# Custom CORS middleware to handle null origins from file:// protocol
@app.middleware("http")
async def custom_cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "*")
    
    # Log the request for debugging
    print(f"Request: {request.method} {request.url.path} from origin: {origin}")
    
    # Handle preflight OPTIONS requests
    if request.method == "OPTIONS":
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": origin if origin else "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "3600",
                "Vary": "Origin",
            }
        )
    
    # Process the actual request
    response = await call_next(request)
    
    # Add CORS headers to response
    response.headers["Access-Control-Allow-Origin"] = origin if origin else "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Vary"] = "Origin"
    
    return response

# Register routers
app.include_router(grievances.router, prefix="/api", tags=["grievances"])
app.include_router(status.router, prefix="/api/status", tags=["status"])
app.include_router(categorization.router, prefix="/api/grievances", tags=["categorization"])


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {
        "ok": True,
        "service": "Grievance Management API",
        "version": "0.1.0"
    }