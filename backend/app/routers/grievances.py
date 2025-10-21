from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Any, Dict, Union

from ..database import get_db
from .. import models, schemas
from ..schemas import GrievanceCreate, GrievancePublic, GrievanceExport, AttachmentIn
from ..utils.id import new_grievance_id
from ..utils.pdf import build_receipt_pdf
import json
import re
from typing import List

router = APIRouter(prefix="/api/grievances", tags=["grievances"])

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _to_iso(dt: Optional[datetime]) -> str:
    if not dt:
        return ""
    # Ensure timezone-aware ISO
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

def _normalize_details(details: Optional[str]) -> Optional[str]:
    text = (details or "").strip()
    if text and len(text) > 10000:
        raise HTTPException(status_code=422, detail="Details too long (max 10,000 characters).")
    return text or None

def _normalize_attachments(raw: Optional[Union[str, List[Any]]]) -> Optional[List[Dict[str, Any]]]:
    if not raw:
        return None
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(data, list):
            raise ValueError("attachments must be an array")
        out: List[Dict[str, Any]] = []
        for item in data:
            if item is None:
                item = {}
            att = AttachmentIn(**item)
            # pydantic v2
            out.append(att.model_dump())
        return out
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid attachments payload.")

def _row_to_public(row: "models.Grievance") -> GrievancePublic:
    return GrievancePublic(
        id=row.id,
        created_at=_to_iso(row.created_at),
        updated_at=_to_iso(row.updated_at or row.created_at),
        external_status=getattr(row, "external_status", None),
        external_status_note=getattr(row, "external_status_note", None),
        is_anonymous=row.is_anonymous,
        complainant_name=getattr(row, "complainant_name", None),
        complainant_email=getattr(row, "complainant_email", None),
        complainant_phone=getattr(row, "complainant_phone", None),
        complainant_gender=getattr(row, "complainant_gender", None),
        is_hh_registered=getattr(row, "is_hh_registered", None),
        hh_id=getattr(row, "hh_id", None),
        hh_address=getattr(row, "hh_address", None),
        island=getattr(row, "island", None),
        district=getattr(row, "district", None),
        village=getattr(row, "village", None),
        category_type=getattr(row, "category_type", None),
        details=getattr(row, "details", None),
        attachments=getattr(row, "attachments", None),
    )

def _row_to_export(row: "models.Grievance") -> GrievanceExport:
    return GrievanceExport(
        id=row.id,
        created_at=_to_iso(row.created_at),
        updated_at=_to_iso(row.updated_at or row.created_at),
        external_status=getattr(row, "external_status", None),
        external_status_note=getattr(row, "external_status_note", None),
        is_anonymous=row.is_anonymous,
        complainant_name=getattr(row, "complainant_name", None),
        complainant_email=getattr(row, "complainant_email", None),
        complainant_phone=getattr(row, "complainant_phone", None),
        complainant_gender=getattr(row, "complainant_gender", None),
        is_hh_registered=getattr(row, "is_hh_registered", None),
        hh_id=getattr(row, "hh_id", None),
        hh_address=getattr(row, "hh_address", None),
        island=getattr(row, "island", None),
        district=getattr(row, "district", None),
        village=getattr(row, "village", None),
        category_type=getattr(row, "category_type", None),
        details=getattr(row, "details", None),
        attachments=getattr(row, "attachments", None),
    )

@router.post("/", response_model=GrievancePublic)
def create_grievance(payload: GrievanceCreate, db: Session = Depends(get_db)):
    gid = new_grievance_id()

    details = _normalize_details(getattr(payload, "details", None))
    attachments = _normalize_attachments(getattr(payload, "attachments", None))

    obj = models.Grievance(
        id=gid,
        is_anonymous=getattr(payload, "is_anonymous", True),
        # complainant
        complainant_name=getattr(payload, "complainant_name", None),
        complainant_email=getattr(payload, "complainant_email", None),
        complainant_phone=getattr(payload, "complainant_phone", None),
        complainant_gender=getattr(payload, "complainant_gender", None),
        # household / address
        is_hh_registered=getattr(payload, "is_hh_registered", None),
        hh_id=getattr(payload, "hh_id", None),
        hh_address=getattr(payload, "hh_address", None),
        # location
        island=getattr(payload, "island", None),
        district=getattr(payload, "district", None),
        village=getattr(payload, "village", None),
        # category type
        category_type=getattr(payload, "category_type", None),
        # content
        details=details,
        # files
        attachments=attachments,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return _row_to_public(obj)

@router.put("/{gid}/status", response_model=schemas.GrievancePublic, summary="Update grievance (status / notes / hh_id / category_type / location)")
def update_grievance_status(gid: str, payload: schemas.GrievanceStatusUpdate, db: Session = Depends(get_db)):
    
    # ✅ Strict GID format check: GRV- + 26 uppercase letters/numbers
    if not re.fullmatch(r"GRV-[A-Z0-9]{26}", gid):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid grievance ID format: {gid}"
        )
    
    grievance = db.query(models.Grievance).filter(models.Grievance.id == gid).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
        
    # default timestamp to now (UTC) if not provided
    ts = payload.external_updated_at or datetime.now(timezone.utc)        

    # external fields (optional)
    if payload.external_status is not None:
        grievance.external_status = payload.external_status
    if payload.external_status_note is not None:
        grievance.external_status_note = payload.external_status_note
    if payload.external_updated_at is not None:
        grievance.external_updated_at = ts 
    if payload.category_type is not None:    
        # Optionally treat empty string as clearing the value:
        grievance.category_type = payload.category_type.strip() or None
    
    # ✅ If hh_id is included, update it and location fields
    hh_id = getattr(payload, "hh_id", None)
    if hh_id:
        grievance.hh_id = hh_id    
        # Optional: auto-fill location fields based on household data
        hh_info = get_household_info_from_odoo(payload.hh_id)
        if hh_info:
            grievance.island = hh_info.get("island")
            grievance.district = hh_info.get("district")
            grievance.village = hh_info.get("village")    

    try:
        db.commit()
    except Exception:
        db.rollback()
        # re-raise so FastAPI returns 500 with a clean message;
        # the logs will contain the full traceback you saw in `docker compose logs -f api`
        raise

    db.refresh(grievance)
    return grievance

def get_household_info_from_odoo(hh_id: str) -> dict:
    # Replace this stub with a real Odoo API call if needed
    # For example, using requests to query /api/household/{hh_id}
    fake_lookup = {
        "HH123": {"island": "Maiana", "district": "North", "village": "Tabontebike"},
        "HH456": {"island": "Abemama", "district": "West", "village": "Kariatebike"},
    }
    return fake_lookup.get(hh_id, {})

@router.get("/{gid}", response_model=GrievancePublic)
def get_grievance(gid: str, db: Session = Depends(get_db)):
    row = db.get(models.Grievance, gid)
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return _row_to_public(row)

@router.get("/export", response_model=List[GrievanceExport])
def export_recent(
    since_hours: Optional[int] = Query(default=24, ge=1, le=7*24, description="How many past hours to export"),
    db: Session = Depends(get_db),
    ):
    cutoff = _now_utc() - timedelta(hours=since_hours or 24)
    rows = (
        db.query(models.Grievance)
        .filter(models.Grievance.created_at >= cutoff)
        .order_by(models.Grievance.created_at.desc())
        .all()
    )
    return [_row_to_export(r) for r in rows]

@router.get("/{gid}/receipt.pdf")
def receipt(gid: str, db: Session = Depends(get_db)):
    row = db.get(models.Grievance, gid)
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    pdf = build_receipt_pdf({
        "id": row.id,
        "created_at": _to_iso(row.created_at),
        "is_anonymous": row.is_anonymous,
        "details": getattr(row, "details", None),
        "category_type": getattr(row, "category_type", None),
    })
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=receipt-{gid}.pdf"}
    )

@router.put("/status-batch", response_model=schemas.GrievanceBatchUpdateResponse, summary="Batch update grievances (status / notes / hh_id / category_type / location)")
def update_grievances_status_batch(payload: schemas.GrievanceBatchUpdateRequest, db: Session = Depends(get_db)):
    results: List[schemas.GrievanceBatchUpdateResult] = []

    for item in payload.updates:
        updated_fields: List[str] = []
        try:
            g = db.query(models.Grievance).filter(models.Grievance.id == item.gid).first()
            if not g:
                results.append(schemas.GrievanceBatchUpdateResult(gid=item.gid, ok=False, error="Grievance not found"))
                continue

            # apply changes when provided
            if item.external_status is not None:
                g.external_status = item.external_status
                updated_fields.append("external_status")

            if item.external_status_note is not None:
                g.external_status_note = item.external_status_note
                updated_fields.append("external_status_note")

            if item.external_updated_at is not None:
                g.external_updated_at = item.external_updated_at
                updated_fields.append("external_updated_at")

            if item.category_type is not None:
                g.category_type = item.category_type
                updated_fields.append("category_type")

            if item.hh_id is not None:
                g.hh_id = item.hh_id
                updated_fields.append("hh_id")

            # optional direct location overrides if Odoo sends them
            if item.island is not None:
                g.island = item.island
                updated_fields.append("island")
            if item.district is not None:
                g.district = item.district
                updated_fields.append("district")
            if item.village is not None:
                g.village = item.village
                updated_fields.append("village")

            db.commit()
            db.refresh(g)

            results.append(schemas.GrievanceBatchUpdateResult(gid=item.gid, ok=True, updated_fields=updated_fields))
        except Exception as e:
            db.rollback()
            results.append(schemas.GrievanceBatchUpdateResult(gid=item.gid, ok=False, error=str(e)))

    return schemas.GrievanceBatchUpdateResponse(results=results)
