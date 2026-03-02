from fastapi import Request, HTTPException, status
from app.config import settings
from typing import Any

MAX_DEPTH = 20
MAX_KEYS = 5000

def validate_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key not in settings.ALLOWED_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

def get_depth(obj: Any, level: int = 0) -> int:
    if isinstance(obj, dict):
        if not obj:
            return level
        return max(get_depth(v, level + 1) for v in obj.values())

    if isinstance(obj, list):
        if not obj:
            return level
        return max(get_depth(i, level + 1) for i in obj)

    return level

def count_keys(obj: Any) -> int:
    if isinstance(obj, dict):
        return len(obj) + sum(count_keys(v) for v in obj.values())

    if isinstance(obj, list):
        return sum(count_keys(i) for i in obj)

    return 0

def precheck_payload_structure(payload: dict) -> str | None:
    if get_depth(payload) > MAX_DEPTH:
        return "Payload nesting too deep"

    if count_keys(payload) > MAX_KEYS:
        return "Payload too large"

    return None

def mask_sensitive_data(payload: Any, fields_to_mask: list[str]) -> Any:
    if isinstance(payload, dict):
        masked = {}
        for key, value in payload.items():
            if key.lower() in [f.lower() for f in fields_to_mask]:
                masked[key] = "***MASKED***"
            else:
                masked[key] = mask_sensitive_data(value, fields_to_mask)
        return masked

    if isinstance(payload, list):
        return [mask_sensitive_data(item, fields_to_mask) for item in payload]

    return payload