"""
EventSpec Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date


class AudioSpec(BaseModel):
    inputs_needed: Optional[int] = None
    mics: Optional[List[str]] = None
    playback: Optional[bool] = None
    pa_coverage: Optional[str] = None


class ScreenSpec(BaseModel):
    size_in: Optional[int] = None
    count: Optional[int] = None
    placement: Optional[str] = None


class ProjectorSpec(BaseModel):
    lumens: Optional[int] = None
    count: Optional[int] = None
    lens: Optional[str] = None


class LEDWallSpec(BaseModel):
    width_ft: Optional[float] = None
    height_ft: Optional[float] = None
    pitch_mm: Optional[float] = None


class VideoSpec(BaseModel):
    screens: Optional[List[ScreenSpec]] = None
    projectors: Optional[List[ProjectorSpec]] = None
    primary_display_type: Optional[str] = None  # LED Wall, Projector, TV/Monitor, None
    led_wall: Optional[LEDWallSpec] = None
    recording: Optional[bool] = None
    livestream: Optional[bool] = None
    cameras: Optional[float] = None


class LightingSpec(BaseModel):
    basic_wash: Optional[bool] = None
    uplights: Optional[int] = None
    moving_heads: Optional[int] = None
    console_required: Optional[bool] = None


class PipeAndDrapeSpec(BaseModel):
    height_ft: Optional[float] = None
    linear_ft: Optional[float] = None


class StagingSpec(BaseModel):
    stage_width_ft: Optional[float] = None
    stage_depth_ft: Optional[float] = None
    stage_height_ft: Optional[float] = None
    skirting: Optional[bool] = None
    pipe_and_drape: Optional[PipeAndDrapeSpec] = None


class PowerSpec(BaseModel):
    dedicated_circuits: Optional[int] = None
    venue_power_notes: Optional[str] = None


class ScheduleSpec(BaseModel):
    load_in: Optional[str] = None
    rehearsal: Optional[str] = None
    show_start: Optional[str] = None
    show_end: Optional[str] = None
    load_out: Optional[str] = None


class RoomSpec(BaseModel):
    name: str
    type: str  # GS, Breakout, Panel, Workshop, Expo, Other
    capacity: int
    days_active: List[str]  # List of date strings
    layout: Optional[str] = None  # Theater, Classroom, Rounds, U-Shape, Square, Custom
    audio: AudioSpec
    video: VideoSpec
    lighting: LightingSpec
    staging: StagingSpec
    power: PowerSpec
    schedule: ScheduleSpec
    additional_notes: Optional[str] = None


class EventSpec(BaseModel):
    event_name: str
    client_name: str
    start_date: date
    end_date: date
    venue: str
    city: str
    state: str
    country: str
    timezone: str
    expected_attendance: Optional[int] = None
    schedule_notes: Optional[str] = None
    rooms: List[RoomSpec]
    general_notes: Optional[str] = None

