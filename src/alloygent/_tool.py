from collections.abc import Callable
from dataclasses import dataclass
from inspect import Parameter, signature
from typing import Any


def _annotation_to_json_type(annotation: Any) -> str:
    if annotation is bool:
        return "boolean"
    if annotation is int:
        return "integer"
    if annotation is float:
        return "number"
    if annotation is list:
        return "array"
    if annotation is dict:
        return "object"
    return "string"


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


def schema_from_function(fn: Callable[..., Any]) -> dict[str, Any]:
    sig = signature(fn)
    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            continue
        properties[name] = {"type": _annotation_to_json_type(param.annotation)}
        if param.default is Parameter.empty:
            required.append(name)

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }


def tool(
    name: str | None = None,
    description: str | None = None,
    parameters: dict[str, Any] | None = None,
):
    """Decorator to turn a plain function into a Tool."""

    def decorator(fn: Callable[..., Any]) -> Tool:
        return Tool(
            name=name or fn.__name__,
            description=description or (fn.__doc__ or "").strip(),
            parameters=parameters or schema_from_function(fn),
            fn=fn,
        )

    return decorator
