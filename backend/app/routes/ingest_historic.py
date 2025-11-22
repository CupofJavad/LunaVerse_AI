"""
Historic events ingestion routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.historic_events import HistoricEvent
from app.routes.auth import get_current_user
from app.models.users import User
from app.services.embeddings import generate_embedding
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()


class HistoricEventItem(BaseModel):
    title: str
    body: str


class HistoricEventBatch(BaseModel):
    events: List[HistoricEventItem]


@router.post("/historic-events")
async def ingest_historic_events(
    batch: HistoricEventBatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload historic events"""
    events_ingested = 0
    embeddings_generated = 0
    
    for event in batch.events:
        historic = HistoricEvent(
            id=uuid.uuid4(),
            title=event.title,
            body=event.body
        )
        
        # Generate embedding
        text_for_embedding = f"{event.title} {event.body}"
        historic.embedding = generate_embedding(text_for_embedding)
        embeddings_generated += 1
        
        db.add(historic)
        events_ingested += 1
    
    db.commit()
    
    return {
        "events_ingested": events_ingested,
        "embeddings_generated": embeddings_generated
    }

