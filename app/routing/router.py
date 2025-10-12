from typing import Callable


class Router:
    PATH_PARAM_INDEX = 2

    def __init__(self) -> None:
        """Initialize the Router with empty routing tables for HTTP methods."""
        self.routes: dict[str, dict[str, Callable]] = {
            "GET": {},
            "POST": {},
            "PATCH": {},
        }

    def add_route(self, method: str, path: str, handler: Callable) -> None:
        """Register a handler function for a specific HTTP method and path."""
        method = method.upper()
        self.routes.setdefault(method, {})[path] = handler

    def resolve(self, method: str, path: str):
        """Resolve the handler function for a given HTTP method and path."""
        method = method.upper()
        method_routes = self.routes.get(method, {})
        if path in method_routes:
            return method_routes[path], None

        if (
            path.startswith("/currency/")
            and "/currency/{code}" in method_routes
        ):
            parts = path.split("/")
            code = (
                parts[self.PATH_PARAM_INDEX]
                if len(parts) > self.PATH_PARAM_INDEX
                else ""
            )
            return method_routes["/currency/{code}"], {"code": code}

        if (
            path.startswith("/exchangeRate/")
            and "/exchangeRate/{currency_code_pair}" in method_routes
        ):
            parts = path.split("/")
            currency_code_pair = (
                parts[self.PATH_PARAM_INDEX]
                if len(parts) > self.PATH_PARAM_INDEX
                else ""
            )
            return method_routes["/exchangeRate/{currency_code_pair}"], {
                "currency_code_pair": currency_code_pair
            }

        return None, None
