from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.analysis import AnalysisStatus
from app.schemas.detection import DetectionRead


class AnalysisFailureRequest(BaseModel):
    error_message: str

    @field_validator("error_message")
    @classmethod
    def error_message_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("error_message must not be blank")
        return value


class AnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    original_filename: str
    content_type: str
    stored_file_path: str
    file_size_bytes: int
    status: AnalysisStatus
    created_at: datetime


class AnalysisDetail(AnalysisRead):
    started_at: datetime | None
    completed_at: datetime | None
    processing_time_ms: int | None
    error_message: str | None
    annotated_file_path: str | None
    detections: list[DetectionRead]
