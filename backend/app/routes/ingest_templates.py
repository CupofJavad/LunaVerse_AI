"""
Template/SOP ingestion routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.historic_events import TemplateDocument
from app.routes.auth import get_current_user
from app.models.users import User
from app.services.embeddings import generate_embedding
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()


class TemplateItem(BaseModel):
    title: str
    doc_type: str = "sop"
    body: str


class TemplateBatch(BaseModel):
    templates: List[TemplateItem]


@router.post("/templates")
async def ingest_templates(
    batch: TemplateBatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload SOP templates"""
    templates_ingested = 0
    embeddings_generated = 0
    
    for template in batch.templates:
        doc = TemplateDocument(
            id=uuid.uuid4(),
            title=template.title,
            body=template.body,
            doc_type=template.doc_type
        )
        
        # Generate embedding
        text_for_embedding = f"{template.title} {template.body}"
        doc.embedding = generate_embedding(text_for_embedding)
        embeddings_generated += 1
        
        db.add(doc)
        templates_ingested += 1
    
    db.commit()
    
    return {
        "templates_ingested": templates_ingested,
        "embeddings_generated": embeddings_generated
    }

