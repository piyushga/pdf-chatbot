import hashlib
import uuid
from dataclasses import dataclass

import tiktoken

from app.services.pdf_extraction_service import ExtractedPage

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOKEN_ENCODING = "cl100k_base"


@dataclass(frozen=True, slots=True)
class TextChunk:
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    page_number: int
    chunk_index: int
    chunk_text: str
    chunk_hash: str
    token_count: int


def create_chunks(
    document_id: uuid.UUID,
    pages: list[ExtractedPage],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be between zero and chunk size.")

    encoding = tiktoken.get_encoding(TOKEN_ENCODING)
    chunks: list[TextChunk] = []
    chunk_index = 0

    for page in pages:
        page_tokens = encoding.encode(page.text)
        start = 0

        while start < len(page_tokens):
            end = min(start + chunk_size, len(page_tokens))
            chunk_tokens = page_tokens[start:end]
            chunk_text = encoding.decode(chunk_tokens).strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        chunk_id=uuid.uuid4(),
                        document_id=document_id,
                        page_number=page.page_number,
                        chunk_index=chunk_index,
                        chunk_text=chunk_text,
                        chunk_hash=hashlib.sha256(chunk_text.encode("utf-8")).hexdigest(),
                        token_count=len(chunk_tokens),
                    )
                )
                chunk_index += 1

            if end == len(page_tokens):
                break
            start = end - overlap

    return chunks
