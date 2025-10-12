from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_DB_PATH = DATA_DIR / "database.db"


@dataclass(frozen=True)
class Configuration:
    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    # Database
    db_path: Path = DEFAULT_DB_PATH

    # Domain constraints, "magic numbers" centralized here
    code_length: int = 3
    code_pair_length: int = 6
    currency_name_min_len: int = 2
    currency_name_max_len: int = 64
    currency_sign_max_len: int = 5
    max_rate: str = "1000000"
    max_decimal_places: int = 6


config = Configuration()
