from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class ToolRole:
    id: str
    name: str
    arguments: dict[str, Any]

@dataclass
class Context:
    role: Role
    content: str = ""
    tool_calls: list[ToolRole] = field(default_factory=list)
    tool_call_id: str | None = None  # set when role == TOOL, links back to the call

    @staticmethod
    def system(content: str) -> "Context":
        return Context(role=Role.SYSTEM, content=content)

    @staticmethod
    def user(content: str) -> "Context":
        return Context(role=Role.USER, content=content)

    @staticmethod
    def assistant(content: str = "", tool_calls: list[ToolRole] | None = None) -> "Context":
        return Context(role=Role.ASSISTANT, content=content, tool_calls=tool_calls or [])

    @staticmethod
    def tool_result(tool_call_id: str, content: str) -> "Context":
        return Context(role=Role.TOOL, content=content, tool_call_id=tool_call_id)
