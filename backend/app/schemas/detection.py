from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DetectionCreate(BaseModel):
    object_type: str = Field(min_length=1)
    confidence_pct: float = Field(ge=0, le=100)
    bbox_x: int = Field(ge=0)
    bbox_y: int = Field(ge=0)
    bbox_width_px: int = Field(gt=0)
    bbox_height_px: int = Field(gt=0)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("object_type")
    @classmethod
    def object_type_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("object_type must not be blank")
        return value


class DetectionSubmission(BaseModel):
    detections: list[DetectionCreate]


class DetectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    analysis_id: UUID
    object_type: str
    confidence_pct: float
    bbox_x: int
    bbox_y: int
    bbox_width_px: int
    bbox_height_px: int
    latitude: float | None
    longitude: float | None
    created_at: datetime


class DetectionSubmissionResponse(BaseModel):
    analysis_id: UUID
    inserted_count: int
    detections: list[DetectionRead]
