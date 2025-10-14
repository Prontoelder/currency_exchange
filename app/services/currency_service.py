from app.database.currency_dao import CurrencyDAO
from app.dtos.create_currency_dto import CreateCurrencyDTO
from app.dtos.currency_dto import CurrencyDTO
from app.exceptions import CurrencyNotFoundError
from app.mappers.currency_mapper import CurrencyMapper


class CurrencyService:
    def __init__(
        self, currency_dao: CurrencyDAO, currency_mapper: CurrencyMapper
    ) -> None:
        self.currency_dao = currency_dao
        self.currency_mapper = currency_mapper

    def get_currencies(self) -> list[CurrencyDTO]:
        """Gets all currencies, maps them to DTOs and returns them."""
        currencies = self.currency_dao.get_currencies()
        return [self.currency_mapper.entity_to_dto(c) for c in currencies]

    def get_currency(self, code: str) -> CurrencyDTO:
        """Gets a specific currency, maps it to a DTO and returns it."""
        currency_entity = self.currency_dao.get_currency(code)

        if not currency_entity:
            raise CurrencyNotFoundError(f"Currency {code} not found")
        return self.currency_mapper.entity_to_dto(currency_entity)

    def post_currency(self, currency_dto: CreateCurrencyDTO) -> CurrencyDTO:
        """Posts a new currency, maps the result to a DTO and returns it."""
        currency_entity = self.currency_mapper.dto_to_entity(currency_dto)
        inserted_currency = self.currency_dao.post_currency(currency_entity)
        return self.currency_mapper.entity_to_dto(inserted_currency)
