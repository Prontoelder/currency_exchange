from decimal import Decimal, InvalidOperation

from app.config import config
from app.exceptions import InvalidCurrencyPairError, InvalidExchangeRateError
from app.validations.currency_validator import CurrencyValidator


class ExchangeRateValidator:
    def __init__(
        self,
        currency_validator: CurrencyValidator,
    ) -> None:
        self.currency_validator = currency_validator

    def validate_currency_code_pair(self, code_pair: str) -> str:
        """Validate currency code pair."""
        cleaned_code_pair = code_pair.strip().upper()

        if not cleaned_code_pair:
            raise InvalidCurrencyPairError("Currency pair cannot be empty")

        if len(cleaned_code_pair) != config.code_pair_length or not all(
            "A" <= ch <= "Z" for ch in cleaned_code_pair
        ):
            raise InvalidCurrencyPairError(
                f"Currency pair must be {config.code_pair_length} "
                f"letters (A-Z only). First 3 letters base currency, "
                f"second 3 target currency"
            )
        return cleaned_code_pair

    def validate_exchange_rate(self, rate: str) -> Decimal:
        """
        Validate exchange rate and return it as a Decimal.
        """
        cleaned_rate = rate.strip()

        if not cleaned_rate:
            raise InvalidExchangeRateError("Exchange rate cannot be empty")

        try:
            decimal_value = Decimal(cleaned_rate)
        except InvalidOperation:
            raise InvalidExchangeRateError(
                "Exchange rate must be a valid number"
            )

        if decimal_value <= 0:
            raise InvalidExchangeRateError(
                "Exchange rate must be greater than zero"
            )

        if decimal_value > Decimal(config.max_rate):
            raise InvalidExchangeRateError(
                f"Exchange rate must not exceed {config.max_rate}"
            )

        # Check decimal places
        if "." in cleaned_rate:
            decimal_places = len(cleaned_rate.split(".")[1])
            if decimal_places > config.max_decimal_places:
                raise InvalidExchangeRateError(
                    f"Exchange rate cannot have more than "
                    f"{config.max_decimal_places} decimal places"
                )

        return decimal_value.normalize()

    def validate_exchange_rate_data(
        self, base_currency_code: str, target_currency_code: str, rate: str
    ):
        """Validate all exchange rate data at once."""
        validated_base_currency_code = (
            self.currency_validator.validate_currency_code(base_currency_code)
        )
        validated_target_currency_code = (
            self.currency_validator.validate_currency_code(
                target_currency_code
            )
        )
        validated_rate = self.validate_exchange_rate(rate)

        return {
            "base_currency_code": validated_base_currency_code,
            "target_currency_code": validated_target_currency_code,
            "rate": validated_rate,
        }
