from pydantic import BaseModel, Field, EmailStr, validator, field_validator
from typing import Optional, List, Union
from datetime import datetime
import re

GRIEVANCE_ID_RE = re.compile(r"^GRV-[A-Z0-9]{26}$")

class AttachmentIn(BaseModel):
    name: Optional[str] = ""
    url: Optional[str] = ""
    size: Optional[int] = 0
    type: Optional[str] = ""

class GrievanceCreate(BaseModel):
    is_anonymous: bool = Field(default=True)

    # Optional complainant info (only when not anonymous)
    complainant_name: Optional[str] = None
    complainant_email: Optional[EmailStr] = None
    complainant_phone: Optional[str] = None
    complainant_gender: Optional[str] = None

    # Household / address (optional)
    is_hh_registered: Optional[bool] = None
    hh_id: Optional[str] = None
    hh_address: Optional[str] = None

    # Location / classification (optional)
    island: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None

    category_type: Optional[str] = None

    # Core content
    details: Optional[str] = None

    # Friendly string from Typebot (not required by backend)
    grievance_details_attachment_friendly: Optional[str] = None

    # Can arrive as a native array or a JSON-encoded string
    attachments: Optional[Union[List[AttachmentIn], str]] = None

class GrievancePublic(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    external_status: Optional[str] = None
    external_status_note: Optional[str] = None
    is_anonymous: bool

    # Echo back selected optional fields
    complainant_name: Optional[str] = None
    complainant_email: Optional[EmailStr] = None
    complainant_phone: Optional[str] = None
    complainant_gender: Optional[str] = None
    is_hh_registered: Optional[bool] = None
    hh_id: Optional[str] = None
    hh_address: Optional[str] = None

    island: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None

    category_type: Optional[str] = None

    details: Optional[str] = None

    attachments: Optional[List[AttachmentIn]] = None

class GrievanceExport(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    external_status: Optional[str] = None
    external_status_note: Optional[str] = None
    is_anonymous: bool

    complainant_name: Optional[str] = None
    complainant_email: Optional[EmailStr] = None
    complainant_phone: Optional[str] = None
    complainant_gender: Optional[str] = None

    is_hh_registered: Optional[bool] = None
    hh_id: Optional[str] = None
    hh_address: Optional[str] = None

    island: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None

    category_type: Optional[str] = None

    details: Optional[str] = None

    attachments: Optional[List[AttachmentIn]] = None

class StatusUpdate(BaseModel):
    status: str
    note: Optional[str] = None
    updated_at: Optional[str] = None
    
class GrievanceStatusUpdate(BaseModel):
    external_status: Optional[str] = None
    external_status_note: Optional[str] = None
    external_updated_at: Optional[datetime] = None
    hh_id: Optional[str] = None
    category_type: Optional[str] = None
    
    @field_validator("external_updated_at", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

class GrievanceBatchUpdateItem(BaseModel):
    gid: str = Field(..., description="Grievance ID like GRV-01K75H29FXZKT9QS3YQY1Z3GQ8")
    external_status: Optional[str] = None
    external_status_note: Optional[str] = None
    external_updated_at: Optional[datetime] = None
    hh_id: Optional[str] = None
    category_type: Optional[str] = None
    # (optional passthroughs if Odoo sends locations directly)
    island: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None

    @validator("gid")
    def _gid_format(cls, v):
        if not GRIEVANCE_ID_RE.match(v):
            raise ValueError(f"Invalid grievance ID format: {v}")
        return v
        
    @field_validator("external_updated_at", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v
        

class GrievanceBatchUpdateRequest(BaseModel):
    updates: List[GrievanceBatchUpdateItem]

class GrievanceBatchUpdateResult(BaseModel):
    gid: str
    ok: bool
    updated_fields: List[str] = []
    error: Optional[str] = None

class GrievanceBatchUpdateResponse(BaseModel):
    results: List[GrievanceBatchUpdateResult]
