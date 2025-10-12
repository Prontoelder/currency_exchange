from http import HTTPStatus

from app.dtos.currency_dto import CurrencyDTO
from app.mappers.currency_mapper import CurrencyMapper
from app.services.currency_service import CurrencyService
from app.validations.currency_validator import CurrencyValidator


class CurrencyController:
    def __init__(
        self,
        currency_service: CurrencyService,
        currency_validator: CurrencyValidator,
        currency_mapper: CurrencyMapper,
    ) -> None:
        self.currency_service = currency_service
        self.currency_validator = currency_validator
        self.currency_mapper = currency_mapper

    def handle_get_currencies(
        self, **_kwargs
    ) -> tuple[list[CurrencyDTO], HTTPStatus]:
        """Get all currencies."""
        currencies = self.currency_service.get_currencies()
        return currencies, HTTPStatus.OK

    def handle_get_currency(
        self, code: str = "", **_kwargs
    ) -> tuple[CurrencyDTO, HTTPStatus]:
        """Get specific currency by code."""
        validated_code = self.currency_validator.validate_currency_code(code)
        currency = self.currency_service.get_currency(validated_code)
        return currency, HTTPStatus.OK

    def handle_post_currency(
        self, name: str = "", code: str = "", sign: str = "", **_kwargs: dict
    ) -> tuple[CurrencyDTO, HTTPStatus]:
        """Create new currency."""
        validated_data = self.currency_validator.validate_currency_data(
            name, code, sign
        )
        currency_dto = self.currency_mapper.dict_to_dto(validated_data)
        currency = self.currency_service.post_currency(currency_dto)
        return currency, HTTPStatus.CREATED
