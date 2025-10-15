# Currency Exchange

This is a REST API for managing currencies and exchange rates. It allows viewing and editing lists of currencies and exchange rates, and calculating the conversion of arbitrary amounts from one currency to another.

## Features

-   **MVC(S) Pattern**: The project follows the Model-View-Controller-Service pattern.
-   **Built-in HTTP Server**: Uses Python's built-in `http.server`.
-   **REST API**: Provides a clean RESTful API for interacting with currency and exchange rate data.
-   **Database**: Uses SQLite for data storage, making it easy to deploy.
-   **No Frameworks**: Built with standard Python libraries to demonstrate core concepts.

## Database Schema

The database consists of two main tables: `Currencies` and `ExchangeRates`.

### `Currencies` Table

| Column   | Type    | Description                        |
| :------- | :------ | :--------------------------------- |
| ID       | INTEGER | Currency ID (Primary Key)          |
| Code     | TEXT    | Currency code (e.g., USD)          |
| FullName | TEXT    | Full name of the currency          |
| Sign     | TEXT    | Currency symbol (e.g., $)          |

### `ExchangeRates` Table

| Column         | Type    | Description                                                     |
| :------------- | :------ | :-------------------------------------------------------------- |
| ID             | INTEGER | Exchange rate ID (Primary Key)                                  |
| BaseCurrencyId | INTEGER | ID of the base currency (Foreign Key to `Currencies.ID`)        |
| TargetCurrencyId| INTEGER | ID of the target currency (Foreign Key to `Currencies.ID`)      |
| Rate           | DECIMAL | Exchange rate                                                   |

## API Endpoints

### Currencies

-   `GET /currencies`: Get a list of all currencies.
-   `POST /currencies`: Add a new currency.
-   `GET /currency/{code}`: Get a specific currency by its code.

### Exchange Rates

-   `GET /exchangeRates`: Get a list of all exchange rates.
-   `POST /exchangeRates`: Add a new exchange rate.
-   `GET /exchangeRate/{pair}`: Get a specific exchange rate by currency pair (e.g., USDEUR).
-   `PATCH /exchangeRate/{pair}`: Update an existing exchange rate.

### Exchange Calculation

-   `GET /exchange?from={from_code}&to={to_code}&amount={amount}`: Calculate the exchange amount between two currencies.

The calculation logic supports:
1.  Direct rates (e.g., A to B).
2.  Reversed rates (using B to A rate).
3.  Cross-rates via a common currency (e.g., USD).

## How to Run

1.  Make sure you have Python installed.
2.  Run the application from the root directory:
    ```bash
    python -m app
    ```
3.  The server will start on `http://127.0.0.1:8000` by default.
