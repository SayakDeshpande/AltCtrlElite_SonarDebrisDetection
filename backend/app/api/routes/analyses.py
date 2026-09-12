from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.analysis import Analysis, AnalysisStatus
from app.services.analysis_service import complete_analysis
from app.services.file_storage import delete_stored_file, store_uploaded_file
from app.services.report_service import build_analysis_report
from app.schemas.analysis import AnalysisDetail, AnalysisFailureRequest, AnalysisRead
from app.schemas.detection import (
    DetectionRead,
    DetectionSubmission,
    DetectionSubmissionResponse,
)
from app.schemas.report import AnalysisReport


router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisRead, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> AnalysisRead:
    """Store an uploaded sonar image and create its queued analysis record."""
    stored_file = await store_uploaded_file(file)

    original_filename = Path(file.filename or "upload").name
    if original_filename in {"", ".", ".."}:
        original_filename = "upload"

    analysis = Analysis(
        original_filename=original_filename,
        content_type=file.content_type,
        stored_file_path=stored_file.relative_path,
        file_size_bytes=stored_file.file_size_bytes,
        status=AnalysisStatus.QUEUED,
    )

    try:
        db.add(analysis)
        db.flush()
        db.refresh(analysis)
        response = AnalysisRead.model_validate(analysis)
    except SQLAlchemyError:
        db.rollback()
        delete_stored_file(stored_file)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create analysis.",
        ) from None

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        delete_stored_file(stored_file)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create analysis.",
        ) from None

    return response


@router.post("/{analysis_id}/start", response_model=AnalysisDetail)
def start_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db),
) -> AnalysisDetail:
    """Transition a queued analysis to processing."""
    statement = (
        select(Analysis)
        .options(selectinload(Analysis.detections))
        .where(Analysis.id == analysis_id)
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

    if analysis.status != AnalysisStatus.QUEUED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only queued analyses can be started.",
        )

    analysis.status = AnalysisStatus.PROCESSING
    analysis.started_at = datetime.now(timezone.utc)

    try:
        db.flush()
        db.refresh(analysis)
        response = AnalysisDetail.model_validate(analysis)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to start analysis.",
        ) from None

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to start analysis.",
        ) from None

    return response


@router.post("/{analysis_id}/fail", response_model=AnalysisDetail)
def fail_analysis(
    analysis_id: UUID,
    failure: AnalysisFailureRequest,
    db: Session = Depends(get_db),
) -> AnalysisDetail:
    """Transition a processing analysis to failed."""
    statement = (
        select(Analysis)
        .options(selectinload(Analysis.detections))
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

    if analysis.status != AnalysisStatus.PROCESSING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only processing analyses can be failed.",
        )

    completed_at = datetime.now(timezone.utc)
    analysis.status = AnalysisStatus.FAILED
    analysis.error_message = failure.error_message
    analysis.completed_at = completed_at
    analysis.processing_time_ms = (
        max(0, int((completed_at - analysis.started_at).total_seconds() * 1000))
        if analysis.started_at is not None
        else None
    )

    try:
        db.flush()
        db.refresh(analysis)
        response = AnalysisDetail.model_validate(analysis)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fail analysis.",
        ) from None

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fail analysis.",
        ) from None

    return response


@router.get("/{analysis_id}/report", response_model=AnalysisReport)
def get_analysis_report(
    analysis_id: UUID,
    db: Session = Depends(get_db),
) -> AnalysisReport:
    """Build a report from one persisted analysis and its detections."""
    statement = (
        select(Analysis)
        .options(selectinload(Analysis.detections))
        .where(Analysis.id == analysis_id)
    )

    try:
        analysis = db.scalar(statement)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve analysis report.",
        ) from None

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )

    return build_analysis_report(analysis)


@router.get("/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db),
) -> Analysis:
    """Return an analysis and all detections submitted for it."""
    statement = (
        select(Analysis)
        .options(selectinload(Analysis.detections))
        .where(Analysis.id == analysis_id)
    )

    try:
        analysis = db.scalar(statement)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve analysis.",
        ) from None

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )

    return analysis


@router.post(
    "/{analysis_id}/detections",
    response_model=DetectionSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_detections(
    analysis_id: UUID,
    submission: DetectionSubmission,
    db: Session = Depends(get_db),
) -> DetectionSubmissionResponse:
    """Store detections submitted by the external YOLO component."""
    return complete_analysis(db, analysis_id, submission.detections)
