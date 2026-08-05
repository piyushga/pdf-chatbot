import uuid
from typing import Any

from psycopg import Connection


def insert_document(
    database: Connection,
    *,
    document_id: uuid.UUID,
    file_name: str,
    file_hash: str,
    file_size: int,
    storage_path: str,
) -> dict[str, Any]:
    row = database.execute(
        """
        INSERT INTO documents (
            document_id, file_name, file_hash, file_size, storage_path, status
        )
        VALUES (%s, %s, %s, %s, %s, 'uploaded')
        RETURNING document_id, file_name, file_hash, file_size, status, uploaded_at
        """,
        (document_id, file_name, file_hash, file_size, storage_path),
    ).fetchone()
    database.commit()
    if row is None:
        raise RuntimeError("PostgreSQL did not return the inserted document.")
    return row


def list_documents(database: Connection) -> list[dict[str, Any]]:
    rows = database.execute(
        """
        SELECT document_id, file_name, file_hash, file_size, status, uploaded_at
        FROM documents
        ORDER BY uploaded_at DESC
        """
    ).fetchall()
    return list(rows)

