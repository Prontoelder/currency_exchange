from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class UpdateExchangeRateDTO:
    currency_code_pair: str
    rate: Decimal
