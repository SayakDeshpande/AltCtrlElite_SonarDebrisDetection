from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.analysis import AnalysisStatus


class ReportDetection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    object_type: str
    confidence_pct: float
    bbox_x: int
    bbox_y: int
    bbox_width_px: int
    bbox_height_px: int
    latitude: float | None
    longitude: float | None


class AnalysisReport(BaseModel):
    analysis_id: UUID
    original_filename: str
    status: AnalysisStatus
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    processing_time_ms: int | None
    detections: list[ReportDetection]
