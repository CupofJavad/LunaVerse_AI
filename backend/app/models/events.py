"""
Event model
"""
from sqlalchemy import Column, String, Date, Integer, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class Event(Base):
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    event_name = Column(String, nullable=False)
    client_name = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    venue = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    timezone = Column(String, nullable=False)
    expected_attendance = Column(Integer)
    
    current_opportunity_id = Column(String)
    current_organization_id = Column(String)
    current_contact_id = Column(String)
    current_venue_id = Column(String)
    opportunity_status = Column(String)
    
    custom_fields = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    rooms = relationship("Room", back_populates="event", cascade="all, delete-orphan")
    event_plans = relationship("EventPlan", back_populates="event", cascade="all, delete-orphan")

