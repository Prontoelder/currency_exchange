import sqlite3
from typing import Any

from app.dtos.create_currency_dto import CreateCurrencyDTO
from app.dtos.currency_dto import CurrencyDTO
from app.models.currency import Currency


class CurrencyMapper:
    @staticmethod
    def dict_to_dto(data: dict[str, Any]) -> CreateCurrencyDTO:
        """Converts dictionary to CreateCurrencyDTO."""
        return CreateCurrencyDTO(
            name=data.get("name", ""),
            code=data.get("code", ""),
            sign=data.get("sign", ""),
        )

    @staticmethod
    def entity_to_dto(entity: Currency) -> CurrencyDTO:
        """Converts a Currency entity to a CurrencyDTO."""
        return CurrencyDTO(
            id=entity.id,
            name=entity.name,
            code=entity.code,
            sign=entity.sign
        )

    @staticmethod
    def dto_to_entity(dto: CurrencyDTO | CreateCurrencyDTO) -> Currency:
        """Converts CurrencyDTO or CreateCurrencyDTO to Currency entity."""
        # For CreateCurrencyDTO, id will not be present.
        currency_id = getattr(dto, "id", None)
        return Currency(
            id=currency_id,
            name=dto.name,
            code=dto.code,
            sign=dto.sign,
        )

    @staticmethod
    def row_to_entity(row: sqlite3.Row) -> Currency:
        """Converts database row to Currency entity."""
        return Currency(**dict(row))
