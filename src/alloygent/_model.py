from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ._history import Context, ToolCall
from ._tool import Tool


@dataclass
class ModelResponse:
    message: str
    raw: Any = None
    tool_calls: list[ToolCall] = field(default_factory=list)

    @property
    def content(self) -> str:
        return self.message


class Model(ABC):
    def __init__(self, model: str, **default_params: Any):
        self.model = model
        self.default_params = default_params

    def call(
        self,
        messages: list[Context],
        tools: list[Tool] | None = None,
        **params: Any,
    ) -> ModelResponse:
        call_params = {**self.default_params, **params}
        return self._call(messages, tools=tools, **call_params)

    @abstractmethod
    def _call(
        self,
        messages: list[Context],
        tools: list[Tool] | None = None,
        **params: Any,
    ) -> ModelResponse:
        """Send messages (+ optional tools) to the provider, return a normalized response."""
        raise NotImplementedError
