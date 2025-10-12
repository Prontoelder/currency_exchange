import sqlite3

from app.database.base_dao import BaseDAO
from app.exceptions import (
    CurrencyNotFoundError,
    ExchangeRateAlreadyExistsError,
)
from app.mappers.exchange_rate_mapper import ExchangeRateMapper
from app.read_models.exchange_rate_view import ExchangeRateView

SELECT_EXCHANGE_RATE_QUERY = """SELECT
    er.id,
    bc.id   AS base_currency_id,
    bc.name AS base_currency_name,
    bc.code AS base_currency_code,
    bc.sign AS base_currency_sign,
    tc.id   AS target_currency_id,
    tc.name AS target_currency_name,
    tc.code AS target_currency_code,
    tc.sign AS target_currency_sign,
    er.rate
FROM ExchangeRates er
JOIN Currencies bc ON er.base_currency_id = bc.id
JOIN Currencies tc ON er.target_currency_id = tc.id"""


class ExchangeRateDAO(BaseDAO):
    def __init__(self, exchange_rates_mapper: ExchangeRateMapper):
        self.exchange_rates_mapper = exchange_rates_mapper

    def get_exchange_rates(self) -> list[ExchangeRateView]:
        """Get all exchange rates from database with joined currency data."""
        sql = f"{SELECT_EXCHANGE_RATE_QUERY};"
        rows = self._execute_all(sql)

        return [self.exchange_rates_mapper.row_to_view(row) for row in rows]

    def get_exchange_rate(
        self, base_currency: str, target_currency: str
    ) -> ExchangeRateView | None:
        """Get exchange rate by base and target currency codes."""
        sql = f"""{SELECT_EXCHANGE_RATE_QUERY}
                WHERE bc.code = ? AND tc.code = ?;
                """
        row = self._execute_one(sql, (base_currency, target_currency))
        return self.exchange_rates_mapper.row_to_view(row) if row else None

    def get_exchange_rate_by_id(self, rate_id: int) -> ExchangeRateView | None:
        """Get exchange rate by its ID."""
        sql = f"""{SELECT_EXCHANGE_RATE_QUERY}
                WHERE er.id = ?;
                """
        row = self._execute_one(sql, (rate_id,))
        return self.exchange_rates_mapper.row_to_view(row) if row else None

    def post_exchange_rate(
        self, base_code: str, target_code: str, rate_str: str
    ) -> ExchangeRateView:
        """Insert new exchange rate and return inserted entity."""
        sql = """INSERT INTO ExchangeRates (base_currency_id,
                                            target_currency_id, rate)
                        SELECT bc.id, tc.id, ?
                        FROM Currencies bc CROSS JOIN Currencies tc
                        WHERE bc.code = ? AND tc.code = ?;
        """
        try:
            inserted_id = self._execute_returning_lastrowid(
                sql, (rate_str, base_code, target_code)
            )
            if inserted_id == 0:
                raise CurrencyNotFoundError(
                    "One or both currencies for the exchange rate not found."
                )
        except sqlite3.IntegrityError as e:
            raise ExchangeRateAlreadyExistsError(
                f"Exchange rate for {base_code}-{target_code} already exists."
            ) from e

        inserted_rate = self.get_exchange_rate_by_id(inserted_id)
        if not inserted_rate:
            raise RuntimeError("Failed to retrieve inserted exchange rate")
        return inserted_rate
