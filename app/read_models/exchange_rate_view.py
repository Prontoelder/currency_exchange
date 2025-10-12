from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExchangeRateView:
    id: int
    base_currency_id: int
    base_currency_name: str
    base_currency_code: str
    base_currency_sign: str
    target_currency_id: int
    target_currency_name: str
    target_currency_code: str
    target_currency_sign: str
    rate: Decimal
