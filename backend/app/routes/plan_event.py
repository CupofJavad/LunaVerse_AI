"""
Plan generation route
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.base import get_db
from app.models.events import Event
from app.models.event_plans import EventPlan, EquipmentLine, CrewLine
from app.models.rooms import Room
from app.schemas.event_spec import EventSpec
from app.schemas.event_plan import EventPlan as EventPlanSchema
from app.routes.auth import get_current_user
from app.models.users import User
from app.services.planner_engine import generate_plan
# Note: We'll create the event inline to avoid circular import
import uuid
import json

router = APIRouter()


@router.post("")
async def plan_event(
    event_spec: EventSpec,
    event_id: UUID = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate an EventPlan from EventSpec.
    
    Workflow:
    1. Validate schema (already done by Pydantic)
    2. Save spec to DB (create event)
    3. Run RAG
    4. Construct prompt
    5. Send to Hugging Face endpoint
    6. Validate returned JSON (repair if needed)
    7. Save EventPlan to DB
    8. Return JSON
    """
    try:
        # Create or get event
        if event_id:
            event = db.query(Event).filter(Event.id == event_id).first()
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")
        else:
            # Create new event inline
            from app.models.rooms import Room, RoomRequirement
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
            event_id = event.id
        
        # Convert event_spec to dict for planner
        event_spec_dict = event_spec.dict()
        event_spec_dict["start_date"] = str(event_spec_dict["start_date"])
        event_spec_dict["end_date"] = str(event_spec_dict["end_date"])
        
        # Generate plan
        plan_dict = await generate_plan(event_spec_dict, str(event.id), db)
        
        # Save EventPlan to database
        event_plan = EventPlan(
            id=uuid.uuid4(),
            event_id=event.id,
            summary=plan_dict.get("summary", ""),
            assumptions=plan_dict.get("assumptions", []),
            trucking=plan_dict.get("trucking", {}),
            metadata=plan_dict.get("metadata", {}),
            weight_total_lbs=plan_dict.get("trucking", {}).get("weight_total_lbs"),
            weight_by_room=plan_dict.get("trucking", {}).get("weight_by_room")
        )
        db.add(event_plan)
        db.flush()
        
        # Save equipment and crew lines
        for room_plan in plan_dict.get("rooms", []):
            room = db.query(Room).filter(Room.event_id == event.id, Room.name == room_plan["name"]).first()
            if not room:
                continue
            
            # Equipment lines
            for eq_item in room_plan.get("equipment", []):
                eq_line = EquipmentLine(
                    id=uuid.uuid4(),
                    event_plan_id=event_plan.id,
                    room_id=room.id,
                    item_code=eq_item.get("item_code"),
                    name=eq_item.get("name"),
                    product_group_name=eq_item.get("product_group_name"),
                    qty=eq_item.get("qty"),
                    unit_type=eq_item.get("unit_type"),
                    replacement_charge=eq_item.get("replacement_charge"),
                    weight_total=eq_item.get("weight_total"),
                    notes=eq_item.get("notes"),
                    source=eq_item.get("source", "ai")
                )
                db.add(eq_line)
            
            # Crew lines
            for crew_item in room_plan.get("crew", []):
                crew_line = CrewLine(
                    id=uuid.uuid4(),
                    event_plan_id=event_plan.id,
                    room_id=room.id,
                    role=crew_item.get("role"),
                    qty=crew_item.get("qty"),
                    hours_in=crew_item.get("hours_in"),
                    hours_show=crew_item.get("hours_show"),
                    hours_out=crew_item.get("hours_out"),
                    bill_rate=crew_item.get("bill_rate"),
                    notes=crew_item.get("notes")
                )
                # Calculate total_bill
                total_hours = (crew_item.get("hours_in", 0) or 0) + \
                             (crew_item.get("hours_show", 0) or 0) + \
                             (crew_item.get("hours_out", 0) or 0)
                crew_line.total_bill = total_hours * (crew_item.get("bill_rate", 0) or 0) * crew_item.get("qty", 0)
                db.add(crew_line)
        
        db.commit()
        
        return plan_dict
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid LLM output: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plan generation failed: {str(e)}"
        )


@router.get("/{event_id}")
async def get_event_plan(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve latest plan for an event"""
    event_plan = db.query(EventPlan).filter(EventPlan.event_id == event_id).order_by(EventPlan.created_at.desc()).first()
    
    if not event_plan:
        raise HTTPException(status_code=404, detail="Event plan not found")
    
    # Reconstruct EventPlan JSON from database
    rooms = []
    for room in db.query(Room).filter(Room.event_id == event_id).all():
        equipment = []
        crew = []
        
        for eq_line in db.query(EquipmentLine).filter(
            EquipmentLine.event_plan_id == event_plan.id,
            EquipmentLine.room_id == room.id
        ).all():
            equipment.append({
                "current_product_id": str(eq_line.current_product_id) if eq_line.current_product_id else None,
                "item_code": eq_line.item_code,
                "name": eq_line.name,
                "product_group_name": eq_line.product_group_name,
                "qty": float(eq_line.qty) if eq_line.qty else 0,
                "unit_type": eq_line.unit_type,
                "weight_total": float(eq_line.weight_total) if eq_line.weight_total else None,
                "replacement_charge": float(eq_line.replacement_charge) if eq_line.replacement_charge else None,
                "notes": eq_line.notes,
                "source": eq_line.source
            })
        
        for crew_line in db.query(CrewLine).filter(
            CrewLine.event_plan_id == event_plan.id,
            CrewLine.room_id == room.id
        ).all():
            crew.append({
                "role": crew_line.role,
                "qty": crew_line.qty,
                "hours_in": float(crew_line.hours_in) if crew_line.hours_in else None,
                "hours_show": float(crew_line.hours_show) if crew_line.hours_show else None,
                "hours_out": float(crew_line.hours_out) if crew_line.hours_out else None,
                "bill_rate": float(crew_line.bill_rate) if crew_line.bill_rate else None,
                "notes": crew_line.notes
            })
        
        rooms.append({
            "room_id": str(room.id),
            "name": room.name,
            "equipment": equipment,
            "crew": crew
        })
    
    event = db.query(Event).filter(Event.id == event_id).first()
    
    return {
        "event_plan": {
            "event_id": str(event_plan.event_id),
            "event_name": event.event_name if event else "",
            "summary": event_plan.summary,
            "assumptions": event_plan.assumptions or [],
            "rooms": rooms,
            "trucking": event_plan.trucking or {},
            "metadata": event_plan.metadata or {}
        }
    }

