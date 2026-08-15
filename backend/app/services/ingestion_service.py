from pathlib import Path

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import insert_chunks
from app.services.chunking_service import create_chunks
from app.services.pdf_extraction_service import extract_pages


def ingest_document(db: Session, document: Document) -> list[DocumentChunk]:
    pages = extract_pages(Path(document.storage_path))
    chunks = create_chunks(document.document_id, pages)
    return insert_chunks(db, chunks)
