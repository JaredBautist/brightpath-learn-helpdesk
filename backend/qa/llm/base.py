from typing import Protocol

class LLMProvider(Protocol):
    def generate(self, system: str, user: str) -> str:
        """Return raw answer JSON or raise a typed AppError."""
        ...
