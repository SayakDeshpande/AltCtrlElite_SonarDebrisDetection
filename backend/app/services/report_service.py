"""Reusable report construction for persisted analyses."""

from app.models.analysis import Analysis
from app.schemas.report import AnalysisReport, ReportDetection


def build_analysis_report(analysis: Analysis) -> AnalysisReport:
    """Transform an analysis and its loaded detections into an API report."""
    return AnalysisReport(
        analysis_id=analysis.id,
        original_filename=analysis.original_filename,
        status=analysis.status,
        created_at=analysis.created_at,
        started_at=analysis.started_at,
        completed_at=analysis.completed_at,
        processing_time_ms=analysis.processing_time_ms,
        detections=[
            ReportDetection.model_validate(detection)
            for detection in analysis.detections
        ],
    )
