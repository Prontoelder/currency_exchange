import json
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from http import HTTPStatus
from typing import Any


class Response:
    @staticmethod
    def _to_jsonable(data: Any) -> Any:
        """Convert other objects to JSON-serializable format."""
        if isinstance(data, Decimal):
            return float(data)
        if is_dataclass(data) and not isinstance(data, type):
            return Response._to_jsonable(asdict(data))
        if isinstance(data, list):
            return [Response._to_jsonable(item) for item in data]
        if isinstance(data, dict):
            return {
                key: Response._to_jsonable(value)
                for key, value in data.items()
            }
        return data

    @classmethod
    def render(
        cls, payload: Any, status: HTTPStatus
    ) -> tuple[bytes, int, dict[str, str]]:
        """
        Render payload as JSON response.
        """
        json_ready = cls._to_jsonable(payload)
        body_str = json.dumps(json_ready, ensure_ascii=False)
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
