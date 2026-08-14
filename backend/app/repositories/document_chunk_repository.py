from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.chunking_service import TextChunk


def insert_chunks(db: Session, chunks: list[TextChunk]) -> list[DocumentChunk]:
    chunk_rows = [
        DocumentChunk(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            page_number=chunk.page_number,
            chunk_index=chunk.chunk_index,
            chunk_text=chunk.chunk_text,
            chunk_hash=chunk.chunk_hash,
            token_count=chunk.token_count,
        )
        for chunk in chunks
    ]

    db.add_all(chunk_rows)
    db.commit()
    return chunk_rows
