from dataclasses import dataclass


@dataclass(frozen=True)
class CurrencyDTO:
    id: int | None
    name: str
    code: str
    sign: str
