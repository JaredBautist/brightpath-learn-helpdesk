import os
import logging
import math
from time import monotonic
import httpx
from qa.errors import AppError

INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
DEFAULT_READ_TIMEOUT_SECONDS = 15.0
MIN_READ_TIMEOUT_SECONDS = 5.0
MAX_READ_TIMEOUT_SECONDS = 60.0
TRANSPORT_TIMEOUT_SECONDS = 5.0
logger = logging.getLogger(__name__)
MAX_OUTPUT_TOKENS = 2048

def configured_timeout() -> httpx.Timeout:
    """Read a finite 5–60s read budget; raise MODEL_UNAVAILABLE for invalid configuration."""
    try:
        read_seconds = float(os.getenv("NVIDIA_TIMEOUT_SECONDS", str(DEFAULT_READ_TIMEOUT_SECONDS)))
    except ValueError as exc:
        raise AppError("MODEL_UNAVAILABLE") from exc
    if not math.isfinite(read_seconds) or not MIN_READ_TIMEOUT_SECONDS <= read_seconds <= MAX_READ_TIMEOUT_SECONDS:
        raise AppError("MODEL_UNAVAILABLE")
    return httpx.Timeout(read=read_seconds, connect=TRANSPORT_TIMEOUT_SECONDS, write=TRANSPORT_TIMEOUT_SECONDS, pool=TRANSPORT_TIMEOUT_SECONDS)


class NvidiaProvider:
    """Adapter for NVIDIA hosted chat completions; never expose upstream diagnostics."""
    def __init__(self) -> None:
        self.api_key = os.getenv("NVIDIA_API_KEY", "").strip()
        self.model = os.getenv("NVIDIA_MODEL", "").strip()
        if not self.api_key:
            raise AppError("MISSING_API_KEY")
        if not self.model:
            raise AppError("MODEL_UNAVAILABLE")
        self.timeout = configured_timeout()

    def generate(self, system: str, user: str) -> str:
        """Return message content; map HTTP/transport/output failures to AppError."""
        payload: dict[str, object] = {
            "model": self.model,
            "messages": [{"role":"system", "content":system}, {"role":"user", "content":user}],
            "temperature": 0,
            "max_tokens": MAX_OUTPUT_TOKENS,
            "stream": False,
        }
        if os.getenv("NVIDIA_JSON_MODE", "false").lower() == "true":
            payload["response_format"] = {"type":"json_object"}
        started_at = monotonic()
        try:
            response = httpx.post(INVOKE_URL, json=payload, headers={"Authorization":f"Bearer {self.api_key}", "Accept":"application/json"}, timeout=self.timeout)
        except httpx.TimeoutException as exc:
            logger.warning("NVIDIA timeout phase=%s elapsed_seconds=%.2f model=%s", type(exc).__name__, monotonic() - started_at, self.model)
            raise AppError("TIMEOUT") from exc
        except httpx.RequestError as exc:
            raise AppError("MODEL_UNAVAILABLE") from exc
        if response.status_code == 429:
            raise AppError("RATE_LIMIT")
        if response.status_code != 200:
            raise AppError("MODEL_UNAVAILABLE")
        try:
            message = response.json()["choices"][0]["message"]["content"]
            if not isinstance(message, str) or not message.strip():
                raise ValueError("Missing message content")
            return message
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise AppError("INVALID_MODEL_OUTPUT") from exc
