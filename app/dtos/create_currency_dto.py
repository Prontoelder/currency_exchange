from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCurrencyDTO:
    name: str
    code: str
    sign: str
