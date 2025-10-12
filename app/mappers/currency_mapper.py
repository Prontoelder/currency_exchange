import sqlite3
from typing import Any

from app.dtos.currency_dto import CurrencyDTO
from app.mappers.base_mapper import BaseMapper
from app.models.currency import Currency


class CurrencyMapper(BaseMapper):
    @staticmethod
    def dict_to_dto(data: dict[str, Any]) -> CurrencyDTO:
        """Converts dictionary to CurrencyDTO."""
        currency_id = data.get("id")
        return CurrencyDTO(
            id=int(currency_id) if currency_id is not None else None,
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
    def dto_to_entity(dto: CurrencyDTO) -> Currency:
        """Converts CurrencyDTO to Currency entity."""
        return Currency(
            id=dto.id,
            name=dto.name,
            code=dto.code,
            sign=dto.sign,
        )

    @staticmethod
    def row_to_entity(row: sqlite3.Row) -> Currency:
        """Converts database row to Currency entity."""
        return Currency(**dict(row))
