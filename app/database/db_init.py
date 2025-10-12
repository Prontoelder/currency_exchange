from .db_session import db_session


def init_db() -> None:
    """Initialize database and add default data."""
    with db_session() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Currencies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                sign TEXT NOT NULL
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ExchangeRates(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base_currency_id INTEGER NOT NULL,
                target_currency_id INTEGER NOT NULL,
                rate TEXT NOT NULL,
                FOREIGN KEY (base_currency_id) REFERENCES Currencies(id),
                FOREIGN KEY (target_currency_id) REFERENCES Currencies(id),
                UNIQUE (base_currency_id, target_currency_id)
            )""")

        # Check if table is empty
        cursor.execute("SELECT 1 FROM Currencies LIMIT 1")
        if not cursor.fetchone():
            # Insert default data
            default_currencies_data = [
                ("AUD", "Australian dollar", "A$"),
                ("USD", "United States dollar", "$"),
                ("EUR", "Euro", "€"),
                ("JPY", "Japanese yen", "¥"),
            ]
            cursor.executemany(
                "INSERT OR IGNORE INTO Currencies (code, name, sign)"
                "VALUES(?,?,?)",
                default_currencies_data,
            )

        cursor.execute("SELECT 1 FROM ExchangeRates LIMIT 1")
        if not cursor.fetchone():
            # Insert default data
            default_exchange_rates_data = [
                (2, 3, 0.92),  # USD->EUR
                (2, 4, 0.0073),  # USD->JPY
                (3, 4, 0.0079),  # EUR->JPY
            ]
            cursor.executemany(
                "INSERT OR IGNORE INTO ExchangeRates "
                "(base_currency_id, target_currency_id, rate)"
                "VALUES(?,?,?)",
                default_exchange_rates_data,
            )
