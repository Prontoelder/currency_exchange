from http import HTTPStatus

from app.dtos.exchange_rate_dto import ExchangeRateDTO
from app.mappers.exchange_rate_mapper import ExchangeRateMapper
from app.services.exchange_rate_service import ExchangeRateService
from app.validations.exchange_rate_validator import ExchangeRateValidator


class ExchangeRatesController:
    def __init__(
        self,
        exchange_rates_service: ExchangeRateService,
        exchange_rates_validator: ExchangeRateValidator,
        exchange_rates_mapper: ExchangeRateMapper,
    ) -> None:
        self.exchange_rates_service = exchange_rates_service
        self.exchange_rates_validator = exchange_rates_validator
        self.exchange_rates_mapper = exchange_rates_mapper

    def handle_get_exchange_rates(
        self,
    ) -> tuple[list[ExchangeRateDTO], HTTPStatus]:
        """Get all exchange rates."""
        exchange_rates = self.exchange_rates_service.get_exchange_rates()
        return exchange_rates, HTTPStatus.OK

    def handle_get_exchange_rate(
        self, currency_code_pair: str = "", **_kwargs
    ) -> tuple[ExchangeRateDTO, HTTPStatus]:
        """Get specific exchange rate by currency code pair."""
        validated_code_pair = (
            self.exchange_rates_validator.validate_currency_code_pair(
                currency_code_pair
            )
        )
        exchange_rate = self.exchange_rates_service.get_exchange_rate(
            validated_code_pair
        )
        return exchange_rate, HTTPStatus.OK

    def handle_post_exchange_rate(
        self,
        baseCurrencyCode: str = "",
        targetCurrencyCode: str = "",
        rate: str = "",
        **_kwargs: dict,
    ) -> tuple[ExchangeRateDTO, HTTPStatus]:
        """Create new exchange rate entry."""
        validated_data = (
            self.exchange_rates_validator.validate_exchange_rate_data(
                baseCurrencyCode, targetCurrencyCode, rate
            )
        )
        exchange_rate_dto = self.exchange_rates_mapper.dict_to_dto(
            validated_data
        )
        exchange_rate = self.exchange_rates_service.post_exchange_rate(
            exchange_rate_dto
        )
        return exchange_rate, HTTPStatus.CREATED
