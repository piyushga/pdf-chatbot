from collections.abc import Generator

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row

from app.core.config import settings


def open_database() -> Connection:
    return psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        row_factory=dict_row,
    )


def get_database() -> Generator[Connection, None, None]:
    with open_database() as connection:
        yield connection
