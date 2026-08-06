from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
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
    db: Annotated[Session, Depends(get_db)],
) -> DocumentResponse:
    try:
        saved_pdf = await save_pdf(file)
    except InvalidPdfError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except PdfTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc

    try:
        document = document_repository.insert_document(db, **saved_pdf)
    except Exception:
        delete_saved_pdf(saved_pdf["storage_path"])
        raise

    return DocumentResponse.model_validate(document)


@router.get("", response_model=DocumentListResponse)
def get_documents(
    db: Annotated[Session, Depends(get_db)],
) -> DocumentListResponse:
    rows = document_repository.list_documents(db)
    documents = [DocumentResponse.model_validate(document) for document in rows]
    return DocumentListResponse(documents=documents, total=len(documents))
