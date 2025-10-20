from http import HTTPStatus

from app.dtos.calculated_exchange_dto import CalculatedExchangeDTO
from app.services.exchange_rate_service import ExchangeRateService
from app.validations.currency_validator import CurrencyValidator
from app.validations.exchange_rate_validator import ExchangeRateValidator


class ExchangeController:
    def __init__(
        self,
        exchange_rates_service: ExchangeRateService,
        exchange_rates_validator: ExchangeRateValidator,
        currency_validator: CurrencyValidator,
    ) -> None:
        self.exchange_rates_service = exchange_rates_service
        self.currency_validator = currency_validator
        self.exchange_rates_validator = exchange_rates_validator

    def handle_get_exchange(
        self, **kwargs: dict
    ) -> tuple[CalculatedExchangeDTO, HTTPStatus]:
        """Handles currency exchange calculation."""
        from_code = str(kwargs.get("from", ""))
        to_code = str(kwargs.get("to", ""))
        amount = str(kwargs.get("amount", ""))

        validated_from = self.currency_validator.validate_currency_code(
            from_code
        )
        validated_to = self.currency_validator.validate_currency_code(to_code)
        validated_amount = self.exchange_rates_validator.validate_amount(
            amount
        )

        calculated_dto = self.exchange_rates_service.calculate_exchange(
            from_code=validated_from,
            to_code=validated_to,
            amount=validated_amount,
        )

        return calculated_dto, HTTPStatus.OK
