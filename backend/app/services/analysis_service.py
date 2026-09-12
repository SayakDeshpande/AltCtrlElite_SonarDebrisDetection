"""Reusable business logic for analysis lifecycle operations."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.analysis import Analysis, AnalysisStatus
from app.models.detection import Detection
from app.schemas.detection import DetectionCreate, DetectionSubmissionResponse


def complete_analysis(
    db: Session,
    analysis_id: UUID,
    detections: list[DetectionCreate],
) -> DetectionSubmissionResponse:
    """Complete a processing analysis with already-adapted detections.

    The analysis row is locked before its state is checked. Detection inserts
    and the analysis completion update are flushed and committed together.
    """
    statement = (
        select(Analysis)
        .where(Analysis.id == analysis_id)
        .with_for_update()
    )

    try:
        analysis = db.scalar(statement)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to look up analysis.",
        ) from None

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )

    if analysis.status == AnalysisStatus.QUEUED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Analysis must be started before detections can be submitted.",
        )

    if analysis.status == AnalysisStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Analysis is already completed; detections cannot be submitted again.",
        )

    if analysis.status == AnalysisStatus.FAILED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Failed analyses cannot accept detections.",
        )

    detection_models = [
        Detection(analysis_id=analysis.id, **detection.model_dump())
        for detection in detections
    ]
    completed_at = datetime.now(timezone.utc)
    analysis.status = AnalysisStatus.COMPLETED
    analysis.completed_at = completed_at
    analysis.processing_time_ms = (
        max(0, int((completed_at - analysis.started_at).total_seconds() * 1000))
        if analysis.started_at is not None
        else None
    )

    try:
        if detection_models:
            db.add_all(detection_models)
        db.flush()
        for detection in detection_models:
            db.refresh(detection)
        response = DetectionSubmissionResponse(
            analysis_id=analysis.id,
            inserted_count=len(detection_models),
            detections=detection_models,
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save detections.",
        ) from None

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save detections.",
        ) from None

    return response
