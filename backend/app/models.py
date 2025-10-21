from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .database import Base

class Grievance(Base):
    __tablename__ = "grievance"

    id = Column(String, primary_key=True, index=True)  # ULID with prefix
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    is_anonymous = Column(Boolean, nullable=False, default=True)

    # Complainant info (only if not anonymous)
    complainant_name = Column(String, nullable=True)
    complainant_email = Column(String, nullable=True)
    complainant_phone = Column(String, nullable=True)
    complainant_gender = Column(String, nullable=True)

    # Household registration info
    is_hh_registered = Column(Boolean, nullable=True)
    hh_id = Column(String, nullable=True)
    hh_address = Column(String, nullable=True)

    # Location info
    island = Column(String, nullable=True)
    district = Column(String, nullable=True)
    village = Column(String, nullable=True)

    # Updated field name
    category_type = Column(String, nullable=True)

    # Complaint details
    details = Column(Text, nullable=True)

    # Attachments (JSON array)
    attachments = Column(JSONB, nullable=True)

    # External system sync fields
    external_status = Column(String, nullable=True)
    external_status_note = Column(Text, nullable=True)
    external_updated_at = Column(DateTime(timezone=True), nullable=True)