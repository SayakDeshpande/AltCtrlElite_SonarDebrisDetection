"""Convert future YOLO detections into the backend detection schema.

This module intentionally does not import Ultralytics or execute model code. A
future YOLO integration can map each model result to :class:`YoloDetection`
and pass it to :func:`adapt_yolo_detection` before calling the existing API.
"""

from dataclasses import dataclass
from collections.abc import Iterable

from app.schemas.detection import DetectionCreate


@dataclass(frozen=True, slots=True)
class YoloDetection:
    """Internal representation of one YOLO result.

    ``confidence`` is expected to be a value from 0.0 to 1.0. Bounding-box
    coordinates use the YOLO-style top-left/bottom-right format ``x1, y1,
    x2, y2`` and are expressed in pixels.
    """

    class_name: str
    confidence: float
    x1: int
    y1: int
    x2: int
    y2: int

    def to_detection_create(self) -> DetectionCreate:
        """Convert this YOLO result to the existing API detection schema."""
        return DetectionCreate(
            object_type=self.class_name,
            confidence_pct=self.confidence * 100,
            bbox_x=self.x1,
            bbox_y=self.y1,
            bbox_width_px=self.x2 - self.x1,
            bbox_height_px=self.y2 - self.y1,
        )


def adapt_yolo_detection(detection: YoloDetection) -> DetectionCreate:
    """Convert one future YOLO result to a :class:`DetectionCreate`."""
    return detection.to_detection_create()


def adapt_yolo_detections(
    detections: Iterable[YoloDetection],
) -> list[DetectionCreate]:
    """Convert an iterable of future YOLO results for API submission."""
    return [adapt_yolo_detection(detection) for detection in detections]
