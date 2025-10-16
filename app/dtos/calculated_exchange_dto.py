from dataclasses import dataclass
from decimal import Decimal

from .currency_dto import CurrencyDTO


@dataclass(frozen=True)
class CalculatedExchangeDTO:
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: Decimal
    amount: Decimal
    convertedAmount: Decimal
