import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from ipaddress import ip_network, ip_address

from ..database import get_db
from .. import models
from ..schemas import StatusUpdate

router = APIRouter()

ODOO_TOKEN = os.getenv("ODOO_TOKEN", "")
ALLOWED = [ip_network(c.strip()) for c in os.getenv("ODOO_ALLOWED_IPS", "").split(",") if c.strip()]

def _check_auth(request: Request):
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing Bearer token")
    token = auth.split(" ", 1)[1].strip()
    if token != ODOO_TOKEN:
        raise HTTPException(403, "Invalid token")
    if ALLOWED:
        client_ip = ip_address(request.client.host)
        if not any(client_ip in net for net in ALLOWED):
            raise HTTPException(403, "IP not allowed")

@router.put("/{gid}/status")
async def update_status(gid: str, payload: StatusUpdate, request: Request, db: Session = Depends(get_db)):
    _check_auth(request)
    row = db.get(models.Grievance, gid)
    if not row:
        raise HTTPException(404, "Not found")
    row.external_status = payload.status
    row.external_status_note = payload.note
    row.external_updated_at = payload.updated_at or datetime.utcnow()
    db.add(row)
    db.commit()
    return {"ok": True, "id": gid, "status": row.external_status}
