from collections.abc import Callable

from app.exceptions import UnsupportedHTTPMethodError


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
        if method not in self.routes:
            raise UnsupportedHTTPMethodError(f"Unsupported HTTP method: "
                                             f"{method}")
        self.routes[method][path] = handler

    def _find_handler_by_template(
        self, method_routes: dict[str, Callable], path: str
    ) -> tuple[Callable, dict[str, str]] | tuple[None, None]:
        """
        Finds a handler by matching the path against registered templates
        (e.g., /path/{param}).
        """
        path_parts = path.split("/")

        for template, handler in method_routes.items():
            if "{" not in template:
                continue

            template_parts = template.split("/")
            if len(template_parts) != len(path_parts):
                continue

            params = {}
            is_match = True
            for template_part, path_part in zip(template_parts, path_parts):
                if template_part.startswith("{") and template_part.endswith(
                    "}"
                ):
                    param_name = template_part.strip("{}")
                    params[param_name] = path_part
                elif template_part != path_part:
                    is_match = False
                    break

            if is_match:
                return handler, params

        return None, None


    def resolve(
        self, method: str, path: str
    ) -> (
            tuple[Callable, dict[str, str]] |
            tuple[Callable, None] |
            tuple[None, None]
    ):
        """Resolve the handler function for a given HTTP method and path."""
        method = method.upper()
        method_routes = self.routes.get(method, {})
        if path in method_routes:
            return method_routes[path], None

        return self._find_handler_by_template(method_routes, path)
