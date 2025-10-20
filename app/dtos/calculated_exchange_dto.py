from dataclasses import dataclass
from decimal import Decimal

from .currency_dto import CurrencyDTO


@dataclass(frozen=True)
class CalculatedExchangeDTO:
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal
