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


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case string to camelCase."""
    parts = snake_str.split("_")
    return parts[0] + "".join(x.title() for x in parts[1:])


def convert_keys_to_camel_case(data: Any) -> Any:
    """Recursively convert dictionary keys from snake_case to camelCase."""
    if isinstance(data, dict):
        return {
            to_camel_case(k): convert_keys_to_camel_case(v)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [convert_keys_to_camel_case(i) for i in data]
    return data


class Response:
    @classmethod
    def render(
        cls, payload: Any, status: HTTPStatus
    ) -> tuple[bytes, int, dict[str, str]]:
        """
        Render payload as JSON response.
        """
        try:
            processed_payload = json.loads(
                json.dumps(payload, ensure_ascii=False, cls=CustomJSONEncoder)
            )
            camel_case_payload = convert_keys_to_camel_case(processed_payload)
            body_str = json.dumps(camel_case_payload, ensure_ascii=False)
        except (TypeError, ValueError):
            status = HTTPStatus.INTERNAL_SERVER_ERROR
            body_str = json.dumps(
                {"message": "Failed to serialize response payload."}
            )

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
