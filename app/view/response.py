import json
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from http import HTTPStatus
from typing import Any


class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle specific data types
    like Decimal and dataclasses.
    """
    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return float(o)
        if is_dataclass(o) and not isinstance(o, type):
            return asdict(o)
        return super().default(o)


class Response:
    @classmethod
    def render(
        cls, payload: Any, status: HTTPStatus
    ) -> tuple[bytes, int, dict[str, str]]:
        """
        Render payload as JSON response.
        """
        body_str = json.dumps(
            payload,
            ensure_ascii=False,
            cls=CustomJSONEncoder)
        body_bytes = body_str.encode("utf-8")
        headers = cls._headers_dict(body_bytes)
        return (
            body_bytes,
            status,
            headers,
        )

    @staticmethod
    def _headers_dict(body_bytes: bytes) -> dict[str, str]:
        """Return response headers."""
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": str(len(body_bytes)),
        }
        return headers
