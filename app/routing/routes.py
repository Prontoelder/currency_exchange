def setup_currency_routes(
    router, currency_controller, exchange_rates_controller, exchange_controller
):
    """Setup routes for endpoints."""
    router.add_route(
        "GET", "/currencies", currency_controller.handle_get_currencies
    )
    router.add_route(
        "GET", "/currency/{code}", currency_controller.handle_get_currency
    )
    router.add_route(
        "GET",
        "/exchangeRates",
        exchange_rates_controller.handle_get_exchange_rates,
    )
    router.add_route(
        "GET",
        "/exchangeRate/{currency_code_pair}",
        exchange_rates_controller.handle_get_exchange_rate,
    )
    router.add_route(
        "GET",
        "/exchange",
        exchange_controller.handle_get_exchange,
    )
    router.add_route(
        "POST",
        "/exchangeRates",
        exchange_rates_controller.handle_post_exchange_rate,
    )
    router.add_route(
        "POST", "/currencies", currency_controller.handle_post_currency
    )
    router.add_route(
        "PATCH",
        "/exchangeRate/{currency_code_pair}",
        exchange_rates_controller.handle_patch_exchange_rate,
    )
