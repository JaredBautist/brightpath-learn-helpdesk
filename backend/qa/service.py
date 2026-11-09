import os
from qa.errors import AppError
from qa.llm.base import LLMProvider
from qa.llm.mock import MockProvider
from qa.prompt import system_prompt
from qa.validate import Answer, validate


def select_provider() -> tuple[str, LLMProvider]:
    """Select mock automatically only when neither provider nor key is configured."""
    name = os.getenv("LLM_PROVIDER", "").strip().lower()
    if not name:
        name = "nvidia" if os.getenv("NVIDIA_API_KEY") else "mock"
    if name == "mock":
        return name, MockProvider()
    if name == "nvidia":
        from qa.llm.nvidia import NvidiaProvider
        return name, NvidiaProvider()
    raise AppError("MODEL_UNAVAILABLE")


def ask_question(question: str, simulate: bool = False) -> tuple[str, Answer]:
    """Generate and validate an answer; propagate typed failures without fallback."""
    if simulate or os.getenv("SIMULATE_FAILURE", "false").lower() == "true":
        raise AppError("MODEL_UNAVAILABLE")
    name, provider = select_provider()
    return name, validate(provider.generate(system_prompt(), question), question)
