from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExchangeRate:
    id: int
    base_currency_id: int
    target_currency_id: int
    rate: Decimal
