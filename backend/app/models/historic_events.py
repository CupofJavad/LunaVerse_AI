"""
Historic Events and Template Documents models for RAG
"""
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.base import Base


class HistoricEvent(Base):
    __tablename__ = "historic_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    body = Column(Text)
    embedding = Column(JSON)  # Store as JSON array
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TemplateDocument(Base):
    __tablename__ = "template_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    body = Column(Text)
    doc_type = Column(String)  # sop, template, etc.
    embedding = Column(JSON)  # Store as JSON array
    created_at = Column(DateTime(timezone=True), server_default=func.now())

