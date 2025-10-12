import sqlite3

from .db_session import db_session


class BaseDAO:
    """
    Base class for DAO. Encapsulates cursor and connection logic.
    """

    @staticmethod
    def _execute(sql: str, params: tuple | None = None) -> None:
        """Execute statement without returning rows
        (INSERT/UPDATE/DELETE/DDL).
        """
        with db_session() as cursor:
            cursor.execute(sql, params or ())

    @staticmethod
    def _execute_one(
        sql: str, params: tuple | None = None
    ) -> sqlite3.Row | None:
        """Execute SELECT and return one row or None if no results."""
        with db_session() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchone()

    @staticmethod
    def _execute_all(
        sql: str, params: tuple | None = None
    ) -> list[sqlite3.Row]:
        """Execute SELECT query and return all rows as list (maybe empty)."""
        with db_session() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()

    @staticmethod
    def _execute_returning_lastrowid(
        sql: str, params: tuple | None = None
    ) -> int:
        """Execute a statement and return the last inserted row id."""
        with db_session() as cursor:
            cursor.execute(sql, params or ())
            return int(cursor.lastrowid)
