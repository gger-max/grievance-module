from fastapi import APIRouter, Depends, HTTPException, Response, Query, Request, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Any, Dict, Union
import json
import re
import uuid
import os
from pathlib import Path

from ..database import get_db
from .. import models, schemas
from ..schemas import GrievanceCreate, GrievancePublic, AttachmentIn
from ..utils.id import new_grievance_id
from ..utils.pdf import build_receipt_pdf
from ..utils.email import send_grievance_confirmation_email
from ..utils.minio import minio_client
from ..services.llm_categorizer import categorize_grievance

router = APIRouter(prefix="/grievances", tags=["grievances"])

# Compile regex once at module level for better performance
# Accept only ULID format (26 character alphanumeric)
GRIEVANCE_ID_PATTERN = re.compile(r"^GRV-[A-Z0-9]{26}$")

# Constants
MAX_DETAILS_LENGTH = 10000
DEFAULT_EXPORT_HOURS = 24
MAX_EXPORT_HOURS = 7 * 24

# Constants
MAX_DETAILS_LENGTH = 10000
DEFAULT_EXPORT_HOURS = 24
MAX_EXPORT_HOURS = 7 * 24


@router.post("/upload-file", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and return its URL."""
    try:
        # Read file content
        content = await file.read()

        # Validate file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(content) > max_size:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")

        # Validate file type
        allowed_types = [
            'image/jpeg', 'image/png', 'image/gif', 'image/webp',
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]

        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"File type {file.content_type} not allowed.")

        # Upload to MinIO
        result = minio_client.upload_file(content, file.filename, file.content_type)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def _now_utc() -> datetime:
    """Get current UTC time with timezone info."""
    return datetime.now(timezone.utc)


def _to_iso(dt: Optional[datetime]) -> str:
    """Convert datetime to ISO format string."""
    if not dt:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def _normalize_details(details: Optional[str]) -> Optional[str]:
    """Validate and normalize grievance details text."""
    if not details:
        return None
    
    text = details.strip()
    if not text:
        return None
        
    if len(text) > MAX_DETAILS_LENGTH:
        raise HTTPException(
            status_code=422,
            detail=f"Details too long (max {MAX_DETAILS_LENGTH:,} characters)."
        )
    return text


def _normalize_attachments(raw: Optional[Union[str, List[Any]]]) -> Optional[List[Dict[str, Any]]]:
    """Parse and validate attachments data."""
    if not raw:
        return None
    
    try:
        # If already parsed by Pydantic as AttachmentIn objects, convert them
        if isinstance(raw, list) and len(raw) > 0 and isinstance(raw[0], AttachmentIn):
            return [item.model_dump() for item in raw]
        
        # Parse JSON string if needed
        data = json.loads(raw) if isinstance(raw, str) else raw
        
        if not isinstance(data, list):
            # If it's a single file object, wrap it in a list
            data = [data]
        
        # Validate each attachment using Pydantic model
        validated_attachments = []
        for item in data:
            # If already an AttachmentIn object, just dump it
            if isinstance(item, AttachmentIn):
                validated_attachments.append(item.model_dump())
            elif isinstance(item, str):
                # Handle string URLs directly
                att = AttachmentIn(url=item)
                validated_attachments.append(att.model_dump())
            else:
                # Otherwise validate and convert, with defaults for missing fields
                try:
                    att = AttachmentIn(**(item or {}))
                    validated_attachments.append(att.model_dump())
                except Exception as e:
                    # Log the error but continue processing other attachments
                    import sys
                    print(f"Warning: Skipping invalid attachment: {e}", file=sys.stderr, flush=True)
                    continue
        
        return validated_attachments if validated_attachments else None
    except json.JSONDecodeError as e:
        # If JSON parsing fails, log and return None (treat as no attachments)
        import sys
        print(f"Warning: Failed to parse attachments JSON: {e}", file=sys.stderr, flush=True)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid attachments payload: {str(e)}"
        )


def _row_to_dict(row: models.Grievance) -> Dict[str, Any]:
    """Convert SQLAlchemy model to dictionary (optimized with direct attribute access)."""
    return {
        "id": row.id,
        "created_at": _to_iso(row.created_at),
        "updated_at": _to_iso(row.updated_at or row.created_at),
        "external_status": row.external_status,
        "external_status_note": row.external_status_note,
        "is_anonymous": row.is_anonymous,
        "complainant_name": row.complainant_name,
        "complainant_email": row.complainant_email,
        "complainant_phone": row.complainant_phone,
        "complainant_gender": row.complainant_gender,
        "is_hh_registered": row.is_hh_registered,
        "hh_id": row.hh_id,
        "hh_address": row.hh_address,
        "island": row.island,
        "district": row.district,
        "village": row.village,
        "category_type": row.category_type,
        "details": row.details,
        "attachments": row.attachments,
    }


def _row_to_public(row: models.Grievance) -> GrievancePublic:
    """Convert database row to public schema."""
    return GrievancePublic(**_row_to_dict(row))

def _auto_categorize(details: str) -> Optional[str]:
    """
    Automatically categorize grievance using LLM.
    
    Args:
        details: Grievance details text
        
    Returns:
        Formatted category string (e.g., "2.3 HH member not registered") or None if categorization fails
    """
    if not details or not details.strip():
        return None
    
    try:
        result = categorize_grievance(details)
        
        # Format as "subcategory subcategory_name" or "category. category_name"
        if result.get('subcategory') and result.get('subcategory_name'):
            return f"{result['subcategory']} {result['subcategory_name']}"
        elif result.get('category') and result.get('category_name'):
            return f"{result['category']}. {result['category_name']}"
        
        return None
    except Exception as e:
        # Log the error but don't fail the grievance creation
        import sys
        print(f"Warning: Auto-categorization failed: {e}", file=sys.stderr, flush=True)
        return None

@router.post("/", status_code=201)
async def create_grievance(
    request: Request,
    payload: GrievanceCreate,
    db: Session = Depends(get_db)
):
    """Create a new grievance entry."""

    # Always generate ID server-side for security and consistency
    gid = new_grievance_id()
    details = _normalize_details(payload.details)
    attachments = _normalize_attachments(payload.attachments)
    
    # Get raw request body to check if category_type was explicitly provided
    raw_body = await request.body()
    raw_data = {}
    try:
        import json
        raw_data = json.loads(raw_body.decode('utf-8'))
    except:
        pass
    
    # Auto-categorize ONLY if category_type field was NOT provided in request
    # If empty string was sent, respect that and don't auto-categorize
    category_type = payload.category_type
    if 'category_type' not in raw_data and not category_type and details:
        category_type = _auto_categorize(details)

    # Create grievance object with direct attribute access
    obj = models.Grievance(
        id=gid,
        is_anonymous=payload.is_anonymous,
        complainant_name=payload.complainant_name,
        complainant_email=payload.complainant_email,
        complainant_phone=payload.complainant_phone,
        complainant_gender=payload.complainant_gender,
        is_hh_registered=payload.is_hh_registered,
        hh_id=payload.hh_id,
        hh_address=payload.hh_address,
        island=payload.island,
        district=payload.district,
        village=payload.village,
        category_type=category_type,
        details=details,
        attachments=attachments,
    )
    
    db.add(obj)
    db.commit()
    db.refresh(obj)
    
    # Verify it was saved by querying it back
    import sys
    verify = db.get(models.Grievance, gid)
    if verify:
        print(f"✅ Verified: Grievance {gid} saved to DB", file=sys.stderr, flush=True)
    else:
        print(f"❌ ERROR: Grievance {gid} NOT found after commit!", file=sys.stderr, flush=True)

    # Send confirmation email if not anonymous and email is provided
    if not payload.is_anonymous and payload.complainant_email:
        send_grievance_confirmation_email(
            to_email=payload.complainant_email,
            grievance_id=gid,
            complainant_name=payload.complainant_name,
            details=details,
        )

    # Return JSONResponse with custom header
    public_data = _row_to_dict(obj)
    print(f"=== RETURNING ID: {gid} ===", file=sys.stderr, flush=True)
    
    # Add tracking_id at root level for easier Typebot access
    public_data["tracking_id"] = gid
    
    return JSONResponse(
        status_code=201,
        content=public_data,
        headers={"X-Grievance-ID": gid}
    )

@router.put("/{gid}/status", response_model=schemas.GrievancePublic)
def update_grievance_status(
    gid: str,
    payload: schemas.GrievanceStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update grievance status, notes, household ID, category, or location."""
    # Validate ID format
    if not GRIEVANCE_ID_PATTERN.fullmatch(gid):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid grievance ID format: {gid}"
        )
    
    # Fetch grievance
    grievance = db.query(models.Grievance).filter(models.Grievance.id == gid).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
    
    # Update timestamp
    ts = payload.external_updated_at or _now_utc()
    
    # Apply updates conditionally
    if payload.external_status is not None:
        grievance.external_status = payload.external_status
    
    if payload.external_status_note is not None:
        grievance.external_status_note = payload.external_status_note
    
    if payload.external_updated_at is not None:
        grievance.external_updated_at = ts
    
    if payload.category_type is not None:
        grievance.category_type = payload.category_type.strip() or None
    
    # Handle household ID with Odoo lookup
    if payload.hh_id:
        grievance.hh_id = payload.hh_id
        hh_info = get_household_info_from_odoo(payload.hh_id)
        if hh_info:
            grievance.island = hh_info.get("island")
            grievance.district = hh_info.get("district")
            grievance.village = hh_info.get("village")
    
    try:
        db.commit()
        db.refresh(grievance)
    except Exception:
        db.rollback()
        raise
    
    return grievance

def get_household_info_from_odoo(hh_id: str) -> dict:
    # Replace this stub with a real Odoo API call if needed
    fake_lookup = {
        "HH123": {"island": "Maiana", "district": "North", "village": "Tabontebike"},
        "HH456": {"island": "Abemama", "district": "West", "village": "Kariatebike"},
    }
    return fake_lookup.get(hh_id, {})

@router.get("/export", response_model=List[GrievancePublic])
def export_recent(
    since_hours: int = Query(
        default=DEFAULT_EXPORT_HOURS,
        ge=1,
        le=MAX_EXPORT_HOURS,
        description="How many past hours to export"
    ),
    db: Session = Depends(get_db),
):
    """Export grievances created within the specified time window."""
    cutoff = _now_utc() - timedelta(hours=since_hours)
    
    rows = (
        db.query(models.Grievance)
        .filter(models.Grievance.created_at >= cutoff)
        .order_by(models.Grievance.created_at.desc())
        .all()
    )
    
    return [_row_to_public(r) for r in rows]

@router.get("/{gid}", response_model=GrievancePublic)
def get_grievance(gid: str, db: Session = Depends(get_db)):
    row = db.get(models.Grievance, gid)
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return _row_to_public(row)

@router.get("/{gid}/receipt.pdf", response_class=Response)
def receipt(gid: str, db: Session = Depends(get_db)):
    """Generate and download a PDF receipt for a grievance."""
    row = db.get(models.Grievance, gid)
    if not row:
        raise HTTPException(status_code=404, detail="Grievance not found")
    
    # Build PDF with essential data including attachments and complainant info
    pdf = build_receipt_pdf({
        "id": row.id,
        "created_at": _to_iso(row.created_at),
        "is_anonymous": row.is_anonymous,
        "complainant_name": row.complainant_name,
        "complainant_email": row.complainant_email,
        "complainant_phone": row.complainant_phone,
        "complainant_gender": row.complainant_gender,
        "hh_id": row.hh_id,
        "hh_address": row.hh_address,
        "details": row.details or "N/A",
        "category_type": row.category_type or "Unspecified",
        "attachments": row.attachments,
    })
    
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{gid}.pdf"'
        }
    )

@router.put("/status-batch", response_model=schemas.GrievanceBatchUpdateResponse)
def update_grievances_status_batch(
    payload: schemas.GrievanceBatchUpdateRequest,
    db: Session = Depends(get_db)
):
    """Batch update multiple grievances' status, notes, household ID, category, or location."""
    results: List[schemas.GrievanceBatchUpdateResult] = []

    for item in payload.updates:
        updated_fields: List[str] = []
        try:
            # Fetch grievance
            grievance = db.query(models.Grievance).filter(
                models.Grievance.id == item.gid
            ).first()
            
            if not grievance:
                results.append(schemas.GrievanceBatchUpdateResult(
                    gid=item.gid,
                    ok=False,
                    error="Grievance not found"
                ))
                continue

            # Apply updates conditionally and track changes
            if item.external_status is not None:
                grievance.external_status = item.external_status
                updated_fields.append("external_status")

            if item.external_status_note is not None:
                grievance.external_status_note = item.external_status_note
                updated_fields.append("external_status_note")

            if item.external_updated_at is not None:
                grievance.external_updated_at = item.external_updated_at
                updated_fields.append("external_updated_at")

            if item.category_type is not None:
                grievance.category_type = item.category_type
                updated_fields.append("category_type")

            if item.hh_id is not None:
                grievance.hh_id = item.hh_id
                updated_fields.append("hh_id")

            # Location overrides from external system
            if item.island is not None:
                grievance.island = item.island
                updated_fields.append("island")
            
            if item.district is not None:
                grievance.district = item.district
                updated_fields.append("district")
            
            if item.village is not None:
                grievance.village = item.village
                updated_fields.append("village")

            db.commit()
            db.refresh(grievance)

            results.append(schemas.GrievanceBatchUpdateResult(
                gid=item.gid,
                ok=True,
                updated_fields=updated_fields
            ))
            
        except Exception as e:
            db.rollback()
            results.append(schemas.GrievanceBatchUpdateResult(
                gid=item.gid,
                ok=False,
                error=str(e)
            ))

    return schemas.GrievanceBatchUpdateResponse(results=results)