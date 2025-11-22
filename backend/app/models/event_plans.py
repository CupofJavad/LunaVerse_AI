"""
Event Plan models
"""
from sqlalchemy import Column, String, Numeric, Integer, DateTime, JSON, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class EventPlan(Base):
    __tablename__ = "event_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    summary = Column(Text)
    assumptions = Column(JSON)
    trucking = Column(JSON)
    metadata = Column(JSON)
    weight_total_lbs = Column(Numeric)
    weight_by_room = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="event_plans")
    equipment_lines = relationship("EquipmentLine", back_populates="event_plan", cascade="all, delete-orphan")
    crew_lines = relationship("CrewLine", back_populates="event_plan", cascade="all, delete-orphan")


class EquipmentLine(Base):
    __tablename__ = "equipment_lines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_plan_id = Column(UUID(as_uuid=True), ForeignKey("event_plans.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    
    opportunity_group_name = Column(String)
    opportunity_group_order = Column(Integer)
    
    current_product_id = Column(UUID(as_uuid=True), ForeignKey("current_products.id"))
    current_stock_level_id = Column(UUID(as_uuid=True), ForeignKey("current_stock_levels.id"))
    
    item_code = Column(String)
    name = Column(String)
    product_group_name = Column(String)
    category = Column(String)
    qty = Column(Numeric)
    unit_type = Column(String)
    rental_price = Column(Numeric)
    replacement_charge = Column(Numeric)
    weight_total = Column(Numeric)
    
    is_accessory = Column(Boolean, default=False)
    parent_equipment_line_id = Column(UUID(as_uuid=True))
    
    notes = Column(Text)
    source = Column(String)  # ai, fallback, manual
    
    # Relationships
    event_plan = relationship("EventPlan", back_populates="equipment_lines")
    room = relationship("Room", back_populates="equipment_lines")
    current_product = relationship("CurrentProduct", back_populates="equipment_lines")
    current_stock_level = relationship("CurrentStockLevel", back_populates="equipment_lines")


class CrewLine(Base):
    __tablename__ = "crew_lines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_plan_id = Column(UUID(as_uuid=True), ForeignKey("event_plans.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    role = Column(String)
    qty = Column(Integer)
    hours_in = Column(Numeric)
    hours_show = Column(Numeric)
    hours_out = Column(Numeric)
    bill_rate = Column(Numeric)
    total_bill = Column(Numeric)
    notes = Column(Text)
    
    # Relationships
    event_plan = relationship("EventPlan", back_populates="crew_lines")
    room = relationship("Room", back_populates="crew_lines")

