from abc import ABC, abstractmethod
from typing import Any

from _history import Context
from _tool import Tool


class ModelResponse:
    message:str
    raw:str

class Model(ABC):
    def __init__(self, model:str, **default_params:Any):
        self.model = model
        self.default_params = default_params

    @abstractmethod
    def _call(
        self,
        messages: list[Context],
        tools: list[Tool] | None = None,
        **params: Any,
    ) -> ModelResponse:
        """Send messages (+ optional tools) to the provider, return a normalized response."""
        raise NotImplementedError
