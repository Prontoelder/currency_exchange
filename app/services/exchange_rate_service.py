from decimal import ROUND_HALF_UP, Decimal

from app.database.currency_dao import CurrencyDAO
from app.database.exchange_rate_dao import ExchangeRateDAO
from app.dtos.calculated_exchange_dto import CalculatedExchangeDTO
from app.dtos.create_exchange_rate_dto import CreateExchangeRateDTO
from app.dtos.exchange_rate_dto import ExchangeRateDTO
from app.dtos.update_exchange_rate_dto import UpdateExchangeRateDTO
from app.exceptions import (
    CurrencyNotFoundError,
    CurrencyPairNotFoundError,
    SameCurrencyError,
)
from app.mappers.currency_mapper import CurrencyMapper
from app.mappers.exchange_rate_mapper import ExchangeRateMapper


class ExchangeRateService:
    def __init__(
        self,
        exchange_rates_dao: ExchangeRateDAO,
        currency_dao: CurrencyDAO,
        exchange_rates_mapper: ExchangeRateMapper,
        currency_mapper: CurrencyMapper,
    ) -> None:
        self.exchange_rates_dao = exchange_rates_dao
        self.currency_dao = currency_dao
        self.exchange_rates_mapper = exchange_rates_mapper
        self.currency_mapper = currency_mapper

    def get_exchange_rates(self) -> list[ExchangeRateDTO]:
        """Get all exchange rates, map them to DTOs and return."""
        views = self.exchange_rates_dao.get_exchange_rates()
        return [
            self.exchange_rates_mapper.view_to_dto(er_view)
            for er_view in views
        ]

    def get_exchange_rate(self, currency_code_pair: str) -> ExchangeRateDTO:
        """Gets a specific exchange rate, maps it to a DTO and returns it."""
        base_currency = currency_code_pair[:3]
        target_currency = currency_code_pair[3:]
        view = self.exchange_rates_dao.get_exchange_rate(
            base_currency, target_currency
        )

        if not view:
            raise CurrencyPairNotFoundError(
                f"Exchange rate for currency pair {currency_code_pair} "
                f"not found"
            )
        return self.exchange_rates_mapper.view_to_dto(view)

    def post_exchange_rate(
        self, exchange_rate_dto: CreateExchangeRateDTO
    ) -> ExchangeRateDTO:
        """Create a new exchange rate and return it as DTO."""
        base_code, target_code, rate_str = (
            self.exchange_rates_mapper.dto_to_insert_args(exchange_rate_dto)
        )
        view = self.exchange_rates_dao.post_exchange_rate(
            base_code, target_code, rate_str
        )
        return self.exchange_rates_mapper.view_to_dto(view)

    def patch_exchange_rate(
        self, exchange_rate_dto: UpdateExchangeRateDTO
    ) -> ExchangeRateDTO:
        """Update an existing exchange rate."""
        base_code = exchange_rate_dto.currency_code_pair[:3]
        target_code = exchange_rate_dto.currency_code_pair[3:]
        rate_str = str(exchange_rate_dto.rate)

        view = self.exchange_rates_dao.patch_exchange_rate(
            base_code, target_code, rate_str
        )
        return self.exchange_rates_mapper.view_to_dto(view)

    def calculate_exchange(
        self, from_code: str, to_code: str, amount: Decimal
    ) -> CalculatedExchangeDTO:
        """
        Calculates the exchange of a given amount from one currency to another.
        """
        if from_code == to_code:
            raise SameCurrencyError(
                "Base and target currency codes cannot be the same."
            )
        rate = self._find_best_rate(from_code, to_code)

        if rate is None:
            raise CurrencyPairNotFoundError(
                f"Exchange rate for {from_code}{to_code} not found"
            )

        base_currency_entity = self.currency_dao.get_currency(from_code)
        target_currency_entity = self.currency_dao.get_currency(to_code)

        if not base_currency_entity or not target_currency_entity:
            raise CurrencyNotFoundError(
                "One or both currencies for exchange not found."
            )

        converted_amount = (amount * rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        return CalculatedExchangeDTO(
            base_currency=self.currency_mapper.entity_to_dto(
                base_currency_entity
            ),
            target_currency=self.currency_mapper.entity_to_dto(
                target_currency_entity
            ),
            rate=rate,
            amount=amount,
            converted_amount=converted_amount,
        )

    def _find_best_rate(
        self, from_code: str, to_code: str
    ) -> Decimal | None:
        """
        Finds available exchange rate according to the logic:
        1. Direct rate (A->B)
        2. Inverse rate (B->A)
        3. Cross-rate through USD (A->USD->B)
        """
        direct_view = self.exchange_rates_dao.get_exchange_rate(
            from_code, to_code
        )
        if direct_view:
            return direct_view.rate

        inverse_view = self.exchange_rates_dao.get_exchange_rate(
            to_code, from_code
        )
        if inverse_view:
            return Decimal(1) / inverse_view.rate

        if from_code != "USD" and to_code != "USD":
            from_usd_view = self.exchange_rates_dao.get_exchange_rate(
                "USD", from_code
            )
            to_usd_view = self.exchange_rates_dao.get_exchange_rate(
                "USD", to_code
            )

            if from_usd_view and to_usd_view:
                return to_usd_view.rate / from_usd_view.rate

        return None
