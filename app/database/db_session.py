import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

from app.config import config
from app.exceptions import DatabaseError


@contextmanager
def db_session() -> Iterator[sqlite3.Cursor]:
    """Database session with auto commit/rollback and dict-like rows."""
    try:
        conn = sqlite3.connect(config.db_path)
        conn.row_factory = sqlite3.Row
        # Enforce foreign key constraints in SQLite
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error: {e}") from e

    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
