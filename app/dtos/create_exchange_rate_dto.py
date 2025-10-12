from dataclasses import dataclass


@dataclass(frozen=True)
class CreateExchangeRateDTO:
    base_currency_code: str
    target_currency_code: str
    rate: str
