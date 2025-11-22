"""
EventPlan Pydantic Schema
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class EquipmentItem(BaseModel):
    current_product_id: Optional[str] = None
    item_code: str
    name: str
    product_group_name: Optional[str] = None
    qty: float
    unit_type: Optional[str] = None
    weight_total: Optional[float] = None
    replacement_charge: Optional[float] = None
    notes: Optional[str] = None
    source: Optional[str] = None  # ai, fallback, manual


class CrewItem(BaseModel):
    role: str
    qty: int
    hours_in: Optional[float] = None
    hours_show: Optional[float] = None
    hours_out: Optional[float] = None
    bill_rate: Optional[float] = None
    notes: Optional[str] = None


class RoomPlan(BaseModel):
    room_id: str
    name: str
    equipment: List[EquipmentItem]
    crew: List[CrewItem]


class TruckingPlan(BaseModel):
    estimated_trucks: int
    weight_total_lbs: Optional[float] = None
    weight_by_room: Optional[Dict[str, float]] = None
    notes: Optional[str] = None


class PlanMetadata(BaseModel):
    model_used: Optional[str] = None
    generation_time_sec: Optional[float] = None
    retrieval_context_count: Optional[int] = None


class EventPlan(BaseModel):
    event_id: str
    event_name: str
    summary: str
    assumptions: List[str]
    rooms: List[RoomPlan]
    trucking: TruckingPlan
    metadata: PlanMetadata

