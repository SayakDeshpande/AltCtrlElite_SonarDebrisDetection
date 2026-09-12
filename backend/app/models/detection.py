import uuid
from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.analysis import Analysis


class Detection(Base):
    """A detected underwater object or anomaly from one analysis."""

    __tablename__ = "detections"
    __table_args__ = (
        CheckConstraint(
            "confidence_pct >= 0 AND confidence_pct <= 100",
            name="ck_detections_confidence_range",
        ),
        CheckConstraint("bbox_x >= 0", name="ck_detections_bbox_x_nonnegative"),
        CheckConstraint("bbox_y >= 0", name="ck_detections_bbox_y_nonnegative"),
        CheckConstraint(
            "bbox_width_px > 0", name="ck_detections_bbox_width_positive"
        ),
        CheckConstraint(
            "bbox_height_px > 0", name="ck_detections_bbox_height_positive"
        ),
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90",
            name="ck_detections_latitude_range",
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180",
            name="ck_detections_longitude_range",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    object_type: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    bbox_x: Mapped[int] = mapped_column(Integer, nullable=False)
    bbox_y: Mapped[int] = mapped_column(Integer, nullable=False)
    bbox_width_px: Mapped[int] = mapped_column(Integer, nullable=False)
    bbox_height_px: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    analysis: Mapped["Analysis"] = relationship(back_populates="detections")
