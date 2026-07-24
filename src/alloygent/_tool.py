from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    """A callable the model is allowed to invoke."""

    name: str
    description: str
    parameters: dict[str, Any]  # JSON schema for arguments
    fn: Callable[..., Any]

    def to_schema(self) -> dict[str, Any]:
        """Provider-agnostic tool schema — adapters translate this per-provider."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

    def run(self, arguments: dict[str, Any]) -> Any:
        return self.fn(**arguments)


def tool(name: str, description: str, parameters: dict[str, Any]):
    """Decorator to turn a plain function into a Tool."""

    def decorator(fn: Callable[..., Any]) -> Tool:
        return Tool(name=name, description=description, parameters=parameters, fn=fn)

    return decorator
