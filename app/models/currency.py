from dataclasses import dataclass


@dataclass
class Currency:
    id: int | None
    name: str
    code: str
    sign: str
