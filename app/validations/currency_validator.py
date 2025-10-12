from app.config import config
from app.exceptions import (
    InvalidCurrencyCodeError,
    InvalidCurrencyNameError,
    InvalidCurrencySignError,
)


class CurrencyValidator:
    def validate_currency_code(self, code: str) -> str:
        """Validate currency code."""
        cleaned_code = code.strip().upper()

        if not cleaned_code:
            raise InvalidCurrencyCodeError("Currency code cannot be empty")

        if len(cleaned_code) != config.code_length or not all(
            "A" <= ch <= "Z" for ch in cleaned_code
        ):
            raise InvalidCurrencyCodeError(
                f"Currency code must be {config.code_length} "
                f"letters (A-Z only)"
            )
        return cleaned_code

    def validate_currency_name(self, name: str) -> str:
        """Validate currency name."""
        cleaned_name = name.strip()

        if not cleaned_name:
            raise InvalidCurrencyNameError("Currency name cannot be empty")

        if not all(ch.isalpha() or ch.isspace() for ch in cleaned_name):
            raise InvalidCurrencyNameError(
                "Currency name must contain letters and spaces only"
            )

        if len(cleaned_name) < config.currency_name_min_len:
            raise InvalidCurrencyNameError(
                f"Currency name must be at least "
                f"{config.currency_name_min_len} letters long"
            )

        if len(cleaned_name) > config.currency_name_max_len:
            raise InvalidCurrencyNameError(
                f"Currency name cannot exceed "
                f"{config.currency_name_max_len} letters"
            )
        return cleaned_name

    def validate_currency_sign(self, sign: str) -> str:
        """Validate currency sign."""
        cleaned_sign = sign.strip()

        if not cleaned_sign:
            raise InvalidCurrencySignError("Currency sign cannot be empty")

        if len(cleaned_sign) > config.currency_sign_max_len:
            raise InvalidCurrencySignError(
                f"Currency sign cannot exceed "
                f"{config.currency_sign_max_len} characters"
            )
        return cleaned_sign

    def validate_currency_data(
        self, name: str, code: str, sign: str
    ) -> dict[str, str]:
        """Validate all currency data at once."""
        validated_name = self.validate_currency_name(name)
        validated_code = self.validate_currency_code(code)
        validated_sign = self.validate_currency_sign(sign)

        return {
            "name": validated_name,
            "code": validated_code,
            "sign": validated_sign,
        }
