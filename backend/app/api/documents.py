from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from psycopg import Connection

from app.core.database import get_database
from app.repositories import document_repository
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.services.document_service import (
    InvalidPdfError,
    PdfTooLargeError,
    delete_saved_pdf,
    save_pdf,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: Annotated[UploadFile, File(description="One PDF document")],
    database: Annotated[Connection, Depends(get_database)],
) -> DocumentResponse:
    try:
        saved_pdf = await save_pdf(file)
    except InvalidPdfError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except PdfTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc

    try:
        row = document_repository.insert_document(database, **saved_pdf)
    except Exception:
        delete_saved_pdf(saved_pdf["storage_path"])
        raise

    return DocumentResponse.model_validate(row)


@router.get("", response_model=DocumentListResponse)
def get_documents(
    database: Annotated[Connection, Depends(get_database)],
) -> DocumentListResponse:
    rows = document_repository.list_documents(database)
    documents = [DocumentResponse.model_validate(row) for row in rows]
    return DocumentListResponse(documents=documents, total=len(documents))
