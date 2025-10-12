import sqlite3

from app.exceptions import CurrencyAlreadyExistsError
from app.mappers.currency_mapper import CurrencyMapper
from app.models.currency import Currency

from .base_dao import BaseDAO


class CurrencyDAO(BaseDAO):
    def __init__(self, currency_mapper: CurrencyMapper):
        self.currency_mapper = currency_mapper

    def get_currencies(self) -> list[Currency]:
        """Get all currencies from database."""
        sql = "SELECT id, code, name, sign FROM Currencies"
        rows = self._execute_all(sql)

        return [self.currency_mapper.row_to_entity(row) for row in rows]

    def get_currency(self, code: str) -> Currency | None:
        """Get currency by code."""
        sql = "SELECT id, code, name, sign FROM Currencies WHERE code = ?"
        row = self._execute_one(sql, (code,))
        return self.currency_mapper.row_to_entity(row) if row else None

    def get_currency_by_id(self, currency_id: int) -> Currency | None:
        """Get currency by id."""
        sql = "SELECT id, code, name, sign FROM Currencies WHERE id = ?"
        row = self._execute_one(sql, (currency_id,))
        return self.currency_mapper.row_to_entity(row) if row else None

    def post_currency(self, currency: Currency) -> Currency:
        """Insert new currency and return inserted entity."""
        sql = "INSERT INTO Currencies (code, name, sign) VALUES(?, ?, ?)"
        try:
            inserted_id = self._execute_returning_lastrowid(
                sql, (currency.code, currency.name, currency.sign)
            )
        except sqlite3.IntegrityError as e:
            raise CurrencyAlreadyExistsError(
                f"Currency with code {currency.code} already exists."
            ) from e

        inserted_currency = self.get_currency_by_id(inserted_id)
        if not inserted_currency:
            raise RuntimeError("Failed to retrieve inserted currency")
        return inserted_currency
