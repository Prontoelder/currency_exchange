from app.controllers.currency_controller import CurrencyController
from app.controllers.exchange_rates_controller import ExchangeRatesController
from app.database.currency_dao import CurrencyDAO
from app.database.exchange_rate_dao import ExchangeRateDAO
from app.mappers.currency_mapper import CurrencyMapper
from app.mappers.exchange_rate_mapper import ExchangeRateMapper
from app.routing.router import Router
from app.routing.routes import setup_currency_routes
from app.services.currency_service import CurrencyService
from app.services.exchange_rate_service import ExchangeRateService
from app.validations.currency_validator import CurrencyValidator
from app.validations.exchange_rate_validator import ExchangeRateValidator
from app.view.response import Response


class Container:
    """
    Container for providing dependencies.
    """

    # Utils
    currency_validator = CurrencyValidator()
    exchange_rates_validator = ExchangeRateValidator(currency_validator)
    response_renderer = Response()

    # Mappers
    currency_mapper = CurrencyMapper()
    exchange_rates_mapper = ExchangeRateMapper()

    # DAO
    currency_dao = CurrencyDAO(currency_mapper)
    exchange_rates_dao = ExchangeRateDAO(exchange_rates_mapper)

    # Services
    currency_service = CurrencyService(currency_dao, currency_mapper)
    exchange_rates_service = ExchangeRateService(
        exchange_rates_dao, exchange_rates_mapper
    )

    # Controllers
    currency_controller = CurrencyController(
        currency_service, currency_validator, currency_mapper
    )
    exchange_rates_controller = ExchangeRatesController(
        exchange_rates_service, exchange_rates_validator, exchange_rates_mapper
    )

    # Router
    router = Router()
    setup_currency_routes(
        router, currency_controller, exchange_rates_controller
    )

container = Container()
