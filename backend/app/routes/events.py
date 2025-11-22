"""
Event management routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.db.base import get_db
from app.models.events import Event
from app.models.rooms import Room, RoomRequirement
from app.schemas.event_spec import EventSpec
from app.routes.auth import get_current_user
from app.models.users import User
from datetime import datetime
import uuid

router = APIRouter()


@router.post("")
async def create_event(event_spec: EventSpec, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new event from EventSpec"""
    # Create event record
    event = Event(
        id=uuid.uuid4(),
        user_id=current_user.id,
        event_name=event_spec.event_name,
        client_name=event_spec.client_name,
        start_date=event_spec.start_date,
        end_date=event_spec.end_date,
        venue=event_spec.venue,
        city=event_spec.city,
        state=event_spec.state,
        country=event_spec.country,
        timezone=event_spec.timezone,
        expected_attendance=event_spec.expected_attendance
    )
    db.add(event)
    db.flush()
    
    # Create rooms and requirements
    for room_spec in event_spec.rooms:
        room = Room(
            id=uuid.uuid4(),
            event_id=event.id,
            name=room_spec.name,
            type=room_spec.type,
            capacity=room_spec.capacity,
            days_active=room_spec.days_active,
            layout=room_spec.layout
        )
        db.add(room)
        db.flush()
        
        # Create room requirements
        req = RoomRequirement(
            id=uuid.uuid4(),
            room_id=room.id,
            audio=room_spec.audio.dict() if room_spec.audio else None,
            video=room_spec.video.dict() if room_spec.video else None,
            lighting=room_spec.lighting.dict() if room_spec.lighting else None,
            staging=room_spec.staging.dict() if room_spec.staging else None,
            power=room_spec.power.dict() if room_spec.power else None,
            schedule=room_spec.schedule.dict() if room_spec.schedule else None,
            other_notes=room_spec.additional_notes
        )
        db.add(req)
    
    db.commit()
    
    return {"event_id": str(event.id), "status": "created"}


@router.get("/{event_id}")
async def get_event(event_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Reconstruct EventSpec from database
    rooms = []
    for room in event.rooms:
        req = room.requirements
        rooms.append({
            "name": room.name,
            "type": room.type,
            "capacity": room.capacity,
            "days_active": room.days_active,
            "layout": room.layout,
            "audio": req.audio if req else {},
            "video": req.video if req else {},
            "lighting": req.lighting if req else {},
            "staging": req.staging if req else {},
            "power": req.power if req else {},
            "schedule": req.schedule if req else {},
            "additional_notes": req.other_notes if req else None
        })
    
    event_spec = {
        "event_name": event.event_name,
        "client_name": event.client_name,
        "start_date": event.start_date.isoformat(),
        "end_date": event.end_date.isoformat(),
        "venue": event.venue,
        "city": event.city,
        "state": event.state,
        "country": event.country,
        "timezone": event.timezone,
        "expected_attendance": event.expected_attendance,
        "rooms": rooms
    }
    
    return {"event": event_spec}


@router.get("")
async def list_events(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List events with pagination"""
    query = db.query(Event)
    
    if search:
        query = query.filter(
            Event.event_name.ilike(f"%{search}%") |
            Event.client_name.ilike(f"%{search}%")
        )
    
    total = query.count()
    events = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "events": [
            {
                "id": str(e.id),
                "event_name": e.event_name,
                "client_name": e.client_name,
                "start_date": e.start_date.isoformat(),
                "end_date": e.end_date.isoformat(),
                "venue": e.venue,
                "city": e.city,
                "state": e.state
            }
            for e in events
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

