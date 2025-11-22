"""
CSV export routes
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.base import get_db
from app.models.events import Event
from app.models.event_plans import EventPlan, EquipmentLine, CrewLine
from app.models.rooms import Room
from app.routes.auth import get_current_user
from app.models.users import User
import csv
import io
from datetime import datetime

router = APIRouter()


@router.get("/equipment-csv/{event_id}")
async def export_equipment_csv(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export equipment CSV for an event"""
    event_plan = db.query(EventPlan).filter(EventPlan.event_id == event_id).order_by(EventPlan.created_at.desc()).first()
    
    if not event_plan:
        raise HTTPException(status_code=404, detail="Event plan not found")
    
    event = db.query(Event).filter(Event.id == event_id).first()
    
    # Build CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Room", "Group", "Item Code", "Product Name", "Product Group",
        "Qty", "Unit Type", "Rental Price", "Replacement Charge",
        "Weight Total (lbs)", "Current Product ID", "Notes", "Source"
    ])
    
    # Data rows
    for room in db.query(Room).filter(Room.event_id == event_id).all():
        for eq_line in db.query(EquipmentLine).filter(
            EquipmentLine.event_plan_id == event_plan.id,
            EquipmentLine.room_id == room.id
        ).all():
            writer.writerow([
                room.name,
                eq_line.opportunity_group_name or "",
                eq_line.item_code or "",
                eq_line.name or "",
                eq_line.product_group_name or "",
                eq_line.qty or 0,
                eq_line.unit_type or "",
                eq_line.rental_price or 0,
                eq_line.replacement_charge or 0,
                eq_line.weight_total or 0,
                str(eq_line.current_product_id) if eq_line.current_product_id else "",
                eq_line.notes or "",
                eq_line.source or "ai"
            ])
    
    output.seek(0)
    filename = f"{event.event_name.replace(' ', '_')}_equipment_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/crew-csv/{event_id}")
async def export_crew_csv(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export crew CSV for an event"""
    event_plan = db.query(EventPlan).filter(EventPlan.event_id == event_id).order_by(EventPlan.created_at.desc()).first()
    
    if not event_plan:
        raise HTTPException(status_code=404, detail="Event plan not found")
    
    event = db.query(Event).filter(Event.id == event_id).first()
    
    # Build CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Room", "Role", "Qty", "Hours In", "Hours Show", "Hours Out",
        "Total Hours", "Bill Rate", "Total Bill", "Notes"
    ])
    
    # Data rows
    for room in db.query(Room).filter(Room.event_id == event_id).all():
        for crew_line in db.query(CrewLine).filter(
            CrewLine.event_plan_id == event_plan.id,
            CrewLine.room_id == room.id
        ).all():
            total_hours = (crew_line.hours_in or 0) + (crew_line.hours_show or 0) + (crew_line.hours_out or 0)
            
            writer.writerow([
                room.name,
                crew_line.role or "",
                crew_line.qty or 0,
                crew_line.hours_in or 0,
                crew_line.hours_show or 0,
                crew_line.hours_out or 0,
                total_hours,
                crew_line.bill_rate or 0,
                crew_line.total_bill or 0,
                crew_line.notes or ""
            ])
    
    output.seek(0)
    filename = f"{event.event_name.replace(' ', '_')}_crew_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/summary/{event_id}")
async def export_summary(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export plan summary as plain text"""
    event_plan = db.query(EventPlan).filter(EventPlan.event_id == event_id).order_by(EventPlan.created_at.desc()).first()
    
    if not event_plan:
        raise HTTPException(status_code=404, detail="Event plan not found")
    
    event = db.query(Event).filter(Event.id == event_id).first()
    
    # Build summary text
    lines = [
        f"Event: {event.event_name}",
        f"Client: {event.client_name}",
        f"Dates: {event.start_date} – {event.end_date}",
        f"Venue: {event.venue}, {event.city}, {event.state}, {event.country}",
        "",
        "SUMMARY",
        "-------",
        event_plan.summary or "",
        "",
        "ASSUMPTIONS",
        "-----------"
    ]
    
    for assumption in (event_plan.assumptions or []):
        lines.append(f"- {assumption}")
    
    lines.extend([
        "",
        "TRUCKING",
        "--------"
    ])
    
    trucking = event_plan.trucking or {}
    lines.append(f"Estimated Trucks: {trucking.get('estimated_trucks', 0)}")
    lines.append(f"Total Weight (lbs): {trucking.get('weight_total_lbs', 0)}")
    
    if trucking.get("weight_by_room"):
        lines.append("")
        lines.append("Weight by Room:")
        for room_name, weight in trucking["weight_by_room"].items():
            lines.append(f"- {room_name}: {weight} lbs")
    
    lines.extend([
        "",
        "ROOMS",
        "-----"
    ])
    
    for room in db.query(Room).filter(Room.event_id == event_id).all():
        eq_count = db.query(EquipmentLine).filter(
            EquipmentLine.event_plan_id == event_plan.id,
            EquipmentLine.room_id == room.id
        ).count()
        crew_count = db.query(CrewLine).filter(
            CrewLine.event_plan_id == event_plan.id,
            CrewLine.room_id == room.id
        ).count()
        
        lines.extend([
            f"Room: {room.name}",
            f"Equipment Lines: {eq_count}",
            f"Crew Lines: {crew_count}",
            ""
        ])
    
    content = "\n".join(lines)
    filename = f"{event.event_name.replace(' ', '_')}_summary_{datetime.now().strftime('%Y-%m-%d')}.txt"
    
    return StreamingResponse(
        iter([content]),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

