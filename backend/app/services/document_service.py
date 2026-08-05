import hashlib
import uuid
from pathlib import Path
from typing import Any

from fastapi import UploadFile

UPLOAD_DIRECTORY = Path("data/uploads")
MAX_PDF_SIZE_BYTES = 20 * 1024 * 1024


class InvalidPdfError(ValueError):
    pass


class PdfTooLargeError(ValueError):
    pass


async def save_pdf(file: UploadFile) -> dict[str, Any]:
    file_name = Path(file.filename or "").name
    if not file_name or Path(file_name).suffix.lower() != ".pdf":
        raise InvalidPdfError("Only .pdf files are accepted.")

    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise InvalidPdfError("The file must have a PDF content type.")

    document_id = uuid.uuid4()
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    destination = UPLOAD_DIRECTORY / f"{document_id}.pdf"
    temporary_destination = destination.with_suffix(".tmp")
    digest = hashlib.sha256()
    file_size = 0

    try:
        with temporary_destination.open("wb") as output:
            chunk = await file.read(64 * 1024)
            if not chunk.startswith(b"%PDF-"):
                raise InvalidPdfError("The uploaded file is not a valid PDF.")

            while chunk:
                file_size += len(chunk)
                if file_size > MAX_PDF_SIZE_BYTES:
                    raise PdfTooLargeError("PDF exceeds the 20 MB limit.")
                digest.update(chunk)
                output.write(chunk)
                chunk = await file.read(64 * 1024)

        temporary_destination.replace(destination)
        return {
            "document_id": document_id,
            "file_name": file_name,
            "file_hash": digest.hexdigest(),
            "file_size": file_size,
            "storage_path": str(destination),
        }
    except Exception:
        temporary_destination.unlink(missing_ok=True)
        destination.unlink(missing_ok=True)
        raise
    finally:
        await file.close()


def delete_saved_pdf(storage_path: str) -> None:
    Path(storage_path).unlink(missing_ok=True)
