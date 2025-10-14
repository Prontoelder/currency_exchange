from dataclasses import dataclass
from decimal import Decimal

from app.dtos.currency_dto import CurrencyDTO


@dataclass(frozen=True)
class ExchangeRateDTO:
    id: int | None
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: Decimal

