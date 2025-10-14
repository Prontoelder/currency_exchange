
from app.database.exchange_rate_dao import ExchangeRateDAO
from app.dtos.create_exchange_rate_dto import CreateExchangeRateDTO
from app.dtos.exchange_rate_dto import ExchangeRateDTO
from app.dtos.update_exchange_rate_dto import UpdateExchangeRateDTO
from app.exceptions import CurrencyPairNotFoundError
from app.mappers.exchange_rate_mapper import ExchangeRateMapper


class ExchangeRateService:
    def __init__(
        self,
        exchange_rates_dao: ExchangeRateDAO,
        exchange_rates_mapper: ExchangeRateMapper,
    ) -> None:
        self.exchange_rates_dao = exchange_rates_dao
        self.exchange_rates_mapper = exchange_rates_mapper

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
