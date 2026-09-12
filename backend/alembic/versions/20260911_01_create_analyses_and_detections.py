"""Create analyses and detections tables.

Revision ID: 20260911_01
Revises:
Create Date: 2026-09-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260911_01"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


analysis_status = postgresql.ENUM(
    "queued",
    "processing",
    "completed",
    "failed",
    name="analysis_status",
    create_type=False,
)


def upgrade() -> None:
    # gen_random_uuid() is used as the database-side UUID default.
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    analysis_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "analyses",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("original_filename", sa.Text(), nullable=False),
        sa.Column("content_type", sa.Text(), nullable=False),
        sa.Column("stored_file_path", sa.Text(), nullable=False),
        sa.Column("file_size_bytes", sa.BigInteger(), nullable=False),
        sa.Column(
            "status",
            analysis_status,
            nullable=False,
            server_default=sa.text("'queued'"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("processing_time_ms", sa.BigInteger(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("annotated_file_path", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "file_size_bytes >= 0", name="ck_analyses_file_size_nonnegative"
        ),
        sa.CheckConstraint(
            "processing_time_ms >= 0",
            name="ck_analyses_processing_time_nonnegative",
        ),
    )

    op.create_table(
        "detections",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("analysis_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("object_type", sa.Text(), nullable=False),
        sa.Column("confidence_pct", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("bbox_x", sa.Integer(), nullable=False),
        sa.Column("bbox_y", sa.Integer(), nullable=False),
        sa.Column("bbox_width_px", sa.Integer(), nullable=False),
        sa.Column("bbox_height_px", sa.Integer(), nullable=False),
        sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "confidence_pct >= 0 AND confidence_pct <= 100",
            name="ck_detections_confidence_range",
        ),
        sa.CheckConstraint("bbox_x >= 0", name="ck_detections_bbox_x_nonnegative"),
        sa.CheckConstraint("bbox_y >= 0", name="ck_detections_bbox_y_nonnegative"),
        sa.CheckConstraint(
            "bbox_width_px > 0", name="ck_detections_bbox_width_positive"
        ),
        sa.CheckConstraint(
            "bbox_height_px > 0", name="ck_detections_bbox_height_positive"
        ),
        sa.CheckConstraint(
            "latitude >= -90 AND latitude <= 90",
            name="ck_detections_latitude_range",
        ),
        sa.CheckConstraint(
            "longitude >= -180 AND longitude <= 180",
            name="ck_detections_longitude_range",
        ),
        sa.ForeignKeyConstraint(
            ["analysis_id"], ["analyses.id"], ondelete="CASCADE"
        ),
    )
    op.create_index("ix_detections_analysis_id", "detections", ["analysis_id"])


def downgrade() -> None:
    op.drop_index("ix_detections_analysis_id", table_name="detections")
    op.drop_table("detections")
    op.drop_table("analyses")
    analysis_status.drop(op.get_bind(), checkfirst=True)
