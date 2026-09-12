"""Reusable storage helpers for uploaded analysis files."""

from dataclasses import dataclass
from pathlib import Path
import uuid

from fastapi import HTTPException, UploadFile, status


UPLOADS_DIRECTORY = Path(__file__).resolve().parents[2] / "storage" / "uploads"
SUPPORTED_IMAGE_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/tiff": ".tiff",
}
CHUNK_SIZE_BYTES = 1024 * 1024


@dataclass(frozen=True, slots=True)
class StoredFile:
    """Details about a file written to the backend upload directory."""

    relative_path: str
    file_size_bytes: int
    absolute_path: Path


async def store_uploaded_file(file: UploadFile) -> StoredFile:
    """Validate and store an uploaded supported image in chunks.

    JPEG uploads are stored with the normalized ``.jpg`` extension, matching
    the existing upload endpoint behavior. The returned relative path is
    suitable for persistence in the analysis record.
    """
    suffix = SUPPORTED_IMAGE_TYPES.get(file.content_type)
    if suffix is None:
        await file.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Use PNG, JPEG, or TIFF.",
        )

    stored_filename = f"{uuid.uuid4().hex}{suffix}"
    relative_path = (Path("storage") / "uploads" / stored_filename).as_posix()
    destination = UPLOADS_DIRECTORY / stored_filename
    file_size_bytes = 0

    try:
        UPLOADS_DIRECTORY.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as output_file:
            while chunk := await file.read(CHUNK_SIZE_BYTES):
                output_file.write(chunk)
                file_size_bytes += len(chunk)
    except Exception:
        delete_stored_file(
            StoredFile(
                relative_path=relative_path,
                file_size_bytes=file_size_bytes,
                absolute_path=destination,
            )
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store uploaded file.",
        ) from None
    finally:
        await file.close()

    return StoredFile(
        relative_path=relative_path,
        file_size_bytes=file_size_bytes,
        absolute_path=destination,
    )


def delete_stored_file(stored_file: StoredFile) -> None:
    """Remove a stored upload when its database transaction cannot finish."""
    try:
        stored_file.absolute_path.unlink(missing_ok=True)
    except OSError:
        pass
