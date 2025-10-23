from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ConfigDict
from typing import Optional, List, Union, Any
from datetime import datetime
import re

GRIEVANCE_ID_RE = re.compile(r"^GRV-[A-Z0-9]{26}$")

class AttachmentIn(BaseModel):
    name: Optional[str] = ""
    url: Optional[str] = ""
    size: Optional[int] = 0
    type: Optional[str] = ""

class GrievanceCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
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

    # Core content - accepts both "details" and "grievance_details" from Typebot
    details: Optional[str] = None

    # Friendly string from Typebot (not required by backend)
    grievance_details_attachment_friendly: Optional[str] = None

    # Can arrive as a native array or a JSON-encoded string
    attachments: Optional[Union[List[AttachmentIn], str]] = None
    
    @model_validator(mode='before')
    @classmethod
    def accept_grievance_details_alias(cls, data: Any) -> Any:
        """Accept both 'details' and 'grievance_details' field names for Typebot compatibility"""
        if isinstance(data, dict):
            # If 'grievance_details' is provided but 'details' is not, use it
            if 'grievance_details' in data and 'details' not in data:
                data['details'] = data['grievance_details']
        return data

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
    # (optional passthroughs if Odoo sends them)
    island: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None

    @field_validator("gid")
    @classmethod
    def _gid_format(cls, v: str) -> str:
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

class CategorizationRequest(BaseModel):
    details: str = Field(..., description="Grievance details text to categorize", min_length=1)

class CategorizationResponse(BaseModel):
    category: str = Field(..., description="Main category number (e.g., '1', '2')")
    subcategory: Optional[str] = Field(None, description="Subcategory code (e.g., '1.1', '2.3')")
    category_name: str = Field(..., description="Human-readable category name")
    subcategory_name: Optional[str] = Field(None, description="Human-readable subcategory name")
    confidence: str = Field(..., description="Confidence level: high, medium, or low")
    reasoning: str = Field(..., description="Brief explanation for the categorization")
    display: str = Field(..., description="Formatted display string for the category")