import sqlite3
from decimal import Decimal
from typing import Any

from app.dtos.create_exchange_rate_dto import CreateExchangeRateDTO
from app.dtos.currency_dto import CurrencyDTO
from app.dtos.exchange_rate_dto import ExchangeRateDTO
from app.mappers.base_mapper import BaseMapper
from app.read_models.exchange_rate_view import ExchangeRateView


class ExchangeRateMapper(BaseMapper):
    @staticmethod
    def row_to_view(row: sqlite3.Row) -> ExchangeRateView:
        """Converts database row to ExchangeRateView read model."""
        data = dict(row)
        # Ensure rate is Decimal (row contains TEXT)
        if "rate" in data and data["rate"] is not None:
            data["rate"] = Decimal(str(data["rate"]))
        return ExchangeRateView(**data)

    @staticmethod
    def view_to_dto(er_view: ExchangeRateView) -> ExchangeRateDTO:
        """Converts ExchangeRateView to ExchangeRateDTO."""
        base_currency = CurrencyDTO(
            id=er_view.base_currency_id,
            name=er_view.base_currency_name,
            code=er_view.base_currency_code,
            sign=er_view.base_currency_sign,
        )
        target_currency = CurrencyDTO(
            id=er_view.target_currency_id,
            name=er_view.target_currency_name,
            code=er_view.target_currency_code,
            sign=er_view.target_currency_sign,
        )
        return ExchangeRateDTO(
            id=er_view.id,
            baseCurrency=base_currency,
            targetCurrency=target_currency,
            rate=er_view.rate,
        )

    @staticmethod
    def dict_to_dto(data: dict[str, Any]) -> CreateExchangeRateDTO:
        return CreateExchangeRateDTO(
            base_currency_code=data.get("base_currency_code", ""),
            target_currency_code=data.get("target_currency_code", ""),
            rate=data.get("rate", ""),
        )

    @staticmethod
    def dto_to_insert_args(
        dto: CreateExchangeRateDTO,
    ) -> tuple[str, str, str]:
        """Normalize DTO for DAO insert (rate as TEXT)."""
        normalized_rate = str(Decimal(dto.rate))
        return (
            dto.base_currency_code,
            dto.target_currency_code,
            normalized_rate,
        )
