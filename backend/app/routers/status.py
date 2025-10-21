import os
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ipaddress import ip_network, ip_address, AddressValueError
from typing import List
from dateutil import parser as date_parser

from ..database import get_db
from .. import models
from ..schemas import StatusUpdate

router = APIRouter()

# Load configuration from environment
ODOO_TOKEN = os.getenv("ODOO_TOKEN", "")
ALLOWED_IPS: List = []

# Parse allowed IPs once at startup
allowed_ips_str = os.getenv("ODOO_ALLOWED_IPS", "")
if allowed_ips_str:
    for ip_str in allowed_ips_str.split(","):
        ip_str = ip_str.strip()
        if ip_str:
            try:
                ALLOWED_IPS.append(ip_network(ip_str))
            except (ValueError, AddressValueError):
                # Log warning in production
                pass

def _check_auth(request: Request) -> None:
    """Validate Bearer token and IP whitelist for external API access."""
    # Check Authorization header
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token"
        )
    
    # Validate token
    token = auth.split(" ", 1)[1].strip()
    if token != ODOO_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
    
    # Check IP whitelist if configured
    if ALLOWED_IPS:
        try:
            client_ip = ip_address(request.client.host)
            if not any(client_ip in net for net in ALLOWED_IPS):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="IP not allowed"
                )
        except (ValueError, AddressValueError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid client IP"
            )

@router.put("/{gid}/status")
async def update_status(
    gid: str,
    payload: StatusUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update grievance status (authenticated endpoint for external systems like Odoo)."""
    # Authenticate request
    _check_auth(request)
    
    # Fetch grievance
    row = db.get(models.Grievance, gid)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grievance not found"
        )
    
    # Update fields
    row.external_status = payload.status
    row.external_status_note = payload.note
    
    # Parse and set timestamp
    if payload.updated_at:
        if isinstance(payload.updated_at, str):
            try:
                row.external_updated_at = date_parser.parse(payload.updated_at)
            except (ValueError, TypeError):
                # Fall back to current time if parsing fails
                row.external_updated_at = datetime.now(timezone.utc)
        else:
            row.external_updated_at = payload.updated_at
    else:
        row.external_updated_at = datetime.now(timezone.utc)
    
    # Persist changes
    db.add(row)
    db.commit()
    
    return {
        "ok": True,
        "id": gid,
        "status": row.external_status
    }