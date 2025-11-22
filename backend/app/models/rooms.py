"""
Room model
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)  # GS, Breakout, Panel, Workshop, Expo, Other
    capacity = Column(Integer)
    days_active = Column(JSON)
    layout = Column(String)  # Theater, Classroom, Rounds, U-Shape, Square, Custom
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="rooms")
    requirements = relationship("RoomRequirement", back_populates="room", uselist=False, cascade="all, delete-orphan")
    equipment_lines = relationship("EquipmentLine", back_populates="room")
    crew_lines = relationship("CrewLine", back_populates="room")


class RoomRequirement(Base):
    __tablename__ = "room_requirements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    audio = Column(JSON)
    video = Column(JSON)
    lighting = Column(JSON)
    staging = Column(JSON)
    power = Column(JSON)
    schedule = Column(JSON)
    other_notes = Column(Text)
    
    # Relationships
    room = relationship("Room", back_populates="requirements")

