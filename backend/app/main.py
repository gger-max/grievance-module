from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
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
    
    # DEBUG: Capture and log request body for POST requests to grievances endpoint
    if request.method == "POST" and request.url.path == "/api/grievances/":
        import sys
        
        # Read the body
        body_bytes = await request.body()
        
        # Log it
        print("=" * 60, file=sys.stderr, flush=True)
        print("WEBHOOK REQUEST BODY:", file=sys.stderr, flush=True)
        print(body_bytes.decode("utf-8"), file=sys.stderr, flush=True)
        print("=" * 60, file=sys.stderr, flush=True)
        
        # Create a new receive callable that replays the body
        # This needs to track state to send body then EOF
        body_sent = False
        
        async def receive():
            nonlocal body_sent
            if not body_sent:
                body_sent = True
                return {"type": "http.request", "body": body_bytes, "more_body": False}
            # Should not be called again, but return empty if it is
            return {"type": "http.request", "body": b"", "more_body": False}
        
        # IMPORTANT: Replace the request with a new one that has the body available
        request = Request(scope=request.scope, receive=receive)
    
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
    response.headers["Access-Control-Expose-Headers"] = "X-Grievance-ID"
    response.headers["Vary"] = "Origin"
    
    return response

# Register routers
app.include_router(grievances.router, prefix="/api", tags=["grievances"])
app.include_router(status.router, prefix="/api/status", tags=["status"])
app.include_router(categorization.router, prefix="/api/grievances", tags=["categorization"])

# Mount static files directory
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {
        "ok": True,
        "service": "Grievance Management API",
        "version": "0.1.0"
    }