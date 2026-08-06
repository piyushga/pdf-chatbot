import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


def insert_document(
    db: Session,
    *,
    document_id: uuid.UUID,
    file_name: str,
    file_hash: str,
    file_size: int,
    storage_path: str,
) -> Document:
    document = Document(
        document_id=document_id,
        file_name=file_name,
        file_hash=file_hash,
        file_size=file_size,
        storage_path=storage_path,
        status="uploaded",
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def list_documents(db: Session) -> list[Document]:
    statement = select(Document).order_by(Document.uploaded_at.desc())
    return list(db.scalars(statement).all())
