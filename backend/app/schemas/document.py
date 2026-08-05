import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    document_id: uuid.UUID
    file_name: str
    file_hash: str
    file_size: int
    status: Literal["uploaded", "processing", "ready", "failed"]
    uploaded_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int

