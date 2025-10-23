from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index
from sqlalchemy.sql import func
from .database import Base

# Use JSON type which works with both PostgreSQL and SQLite
# PostgreSQL will automatically use JSONB when available
JSONType = JSON


class Grievance(Base):
    """Grievance model representing user complaints and feedback."""
    __tablename__ = "grievance"

    # Primary key and timestamps
    id = Column(String, primary_key=True, index=True)  # ULID with prefix
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Core grievance information
    is_anonymous = Column(Boolean, nullable=False, default=True, index=True)

    # Complainant information (only if not anonymous)
    complainant_name = Column(String, nullable=True)
    complainant_email = Column(String, nullable=True, index=True)
    complainant_phone = Column(String, nullable=True)
    complainant_gender = Column(String, nullable=True)

    # Household registration
    is_hh_registered = Column(Boolean, nullable=True)
    hh_id = Column(String, nullable=True, index=True)
    hh_address = Column(String, nullable=True)

    # Location information
    island = Column(String, nullable=True, index=True)
    district = Column(String, nullable=True)
    village = Column(String, nullable=True)

    # Classification
    category_type = Column(String, nullable=True, index=True)

    # Complaint details
    details = Column(Text, nullable=True)

    # Attachments (JSON array)
    attachments = Column(JSONType, nullable=True)

    # External system synchronization
    external_status = Column(String, nullable=True, index=True)
    external_status_note = Column(Text, nullable=True)
    external_updated_at = Column(DateTime(timezone=True), nullable=True)

    # Composite indexes for common queries
    __table_args__ = (
        Index('ix_grievance_created_status', 'created_at', 'external_status'),
        Index('ix_grievance_hh_island', 'hh_id', 'island'),
    )