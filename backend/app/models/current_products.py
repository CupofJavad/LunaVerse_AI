"""
Current RMS Product models
"""
from sqlalchemy import Column, String, Numeric, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class CurrentProduct(Base):
    __tablename__ = "current_products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_product_id = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(Text)
    product_group_name = Column(String, index=True)
    product_group_desc = Column(Text)
    is_bulk_stock = Column(Boolean)
    is_serialised_stock = Column(Boolean)
    is_non_stock = Column(Boolean)
    rental_price = Column(Numeric)
    rental_charge_period_name = Column(String)
    rental_rate_definition_name = Column(String)
    rental_revenue_group = Column(String)
    sale_price = Column(Numeric)
    sale_revenue_group = Column(String)
    replacement_charge = Column(Numeric)
    weight = Column(Numeric)
    power = Column(Numeric)
    barcode = Column(String)
    icon_url = Column(String)
    raw_json = Column(JSON)
    embedding = Column(JSON)  # Store as JSON array, vector type handled by pgvector if available
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    stock_levels = relationship("CurrentStockLevel", back_populates="product", cascade="all, delete-orphan")
    equipment_lines = relationship("EquipmentLine", back_populates="current_product")


class CurrentStockLevel(Base):
    __tablename__ = "current_stock_levels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_product_id = Column(UUID(as_uuid=True), ForeignKey("current_products.id", ondelete="CASCADE"), nullable=False)
    current_stock_level_id = Column(String)
    is_serialised = Column(Boolean)
    asset_number = Column(String)
    store_name = Column(String)
    quantity = Column(Integer)
    status = Column(String)
    custom_fields = Column(JSON)
    raw_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    product = relationship("CurrentProduct", back_populates="stock_levels")
    equipment_lines = relationship("EquipmentLine", back_populates="current_stock_level")

