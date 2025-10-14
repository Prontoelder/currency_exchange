from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from app.exceptions import (
    AlreadyExistsError,
    ApplicationException,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from app.routing.router import Router
from app.view.response import Response

# Map application exceptions to HTTP status codes
EXCEPTION_TO_STATUS = {
    ValidationError: HTTPStatus.BAD_REQUEST,
    NotFoundError: HTTPStatus.NOT_FOUND,
    AlreadyExistsError: HTTPStatus.CONFLICT,
    DatabaseError: HTTPStatus.INTERNAL_SERVER_ERROR,
}


class RequestHandler(BaseHTTPRequestHandler):
    """Custom request handler for handling HTTP requests."""

    router: Router | None = None
    response_renderer: Response | None = None

    @classmethod
    def configurate(cls, router: Router, response_renderer: Response) -> None:
        """Configure the request handler with router and response renderer."""
        cls.router = router
        cls.response_renderer = response_renderer

    def _parse_url(self) -> tuple[str, dict[str, str]]:
        """
        Parse the URL and query parameters.

        Important: Multi-valued query parameters
        are normalized to the first value.
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        raw_query_params = parse_qs(parsed_path.query)
        query_params = {
            key: value[0] for key, value in raw_query_params.items()
        }
        return path, query_params

    def _handle_request(self, method: str) -> None:
        """
        Process HTTP request by resolving the handler from the router
        and executing it.
        """
        if self.router is None:
            self._send_response(
                self._render_response(
                    {"message": "Router not initialized"},
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            )
            return

        path, query_params = self._parse_url()
        handler, path_params = self.router.resolve(method, path)

        if not handler:
            self._send_response(
                self._render_response(
                    {"message": "Endpoint not found"}, HTTPStatus.NOT_FOUND
                )
            )
            return

        try:
            all_params = {**(path_params or {}), **query_params}
            post_data = self._parse_form_data(method)
            all_params.update(post_data)
            payload, status = handler(**all_params)
            response = self._render_response(payload, status)
        except ApplicationException as e:
            response = self._handle_application_exception(e)
        except Exception:
            response = self._render_response(
                {"message": "Internal server error"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        self._send_response(response)

    def do_GET(self) -> None:
        self._handle_request("GET")

    def do_POST(self) -> None:
        self._handle_request("POST")

    def do_PATCH(self) -> None:
        self._handle_request("PATCH")

    def _render_response(
        self, payload: dict, status: HTTPStatus
    ) -> tuple[bytes, int, dict[str, str]]:
        if not self.response_renderer:
            raise RuntimeError("Response renderer not configured")
        return self.response_renderer.render(payload, status)

    def _handle_application_exception(
        self, e: ApplicationException
    ) -> tuple[bytes, int, dict[str, str]]:
        """Render response for application exceptions."""
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        for exc_type, http_status in EXCEPTION_TO_STATUS.items():
            if isinstance(e, exc_type):
                status = http_status
                break
        return self._render_response({"message": e.message}, status)

    def _parse_form_data(self, method: str) -> dict[str, str]:
        """Parse data from POST or PATCH request body.

        Only processes requests with:
        - Method: POST or PATCH
        - Content-Type: application/x-www-form-urlencoded
        - Positive Content-Length
        """
        if method not in ("POST", "PATCH"):
            return {}
        content_length = int(self.headers.get("Content-Length", 0))
        if (
            content_length > 0
            and self.headers.get("Content-Type")
            == "application/x-www-form-urlencoded"
        ):
            raw_post_data = self.rfile.read(content_length)
            post_data = parse_qs(raw_post_data.decode("utf-8"))
            return {key: value[0] for key, value in post_data.items()}
        return {}

    def _send_response(
        self, response: tuple[bytes, int, dict[str, str]]
    ) -> None:
        """Send an HTTP response to client."""
        body, status, headers = response
        self.send_response(status)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(body)
