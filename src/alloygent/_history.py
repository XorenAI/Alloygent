from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


ToolRole = ToolCall


@dataclass
class Context:
    role: Role
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str | None = None  # set when role == TOOL, links back to the call

    @staticmethod
    def system(content: str) -> "Context":
        return Context(role=Role.SYSTEM, content=content)

    @staticmethod
    def user(content: str) -> "Context":
        return Context(role=Role.USER, content=content)

    @staticmethod
    def assistant(
        content: str = "", tool_calls: list[ToolCall] | None = None
    ) -> "Context":
        return Context(role=Role.ASSISTANT, content=content, tool_calls=tool_calls or [])

    @staticmethod
    def tool_result(tool_call_id: str, content: str) -> "Context":
        return Context(role=Role.TOOL, content=content, tool_call_id=tool_call_id)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"role": self.role.value, "content": self.content}
        if self.tool_calls:
            data["tool_calls"] = [
                {"id": call.id, "name": call.name, "arguments": call.arguments}
                for call in self.tool_calls
            ]
        if self.tool_call_id is not None:
            data["tool_call_id"] = self.tool_call_id
        return data


@dataclass
class History:
    messages: list[Context] = field(default_factory=list)

    def add(self, message: Context) -> Context:
        self.messages.append(message)
        return message

    def system(self, content: str) -> Context:
        return self.add(Context.system(content))

    def user(self, content: str) -> Context:
        return self.add(Context.user(content))

    def assistant(
        self, content: str = "", tool_calls: list[ToolCall] | None = None
    ) -> Context:
        return self.add(Context.assistant(content, tool_calls))

    def tool_result(self, tool_call_id: str, content: str) -> Context:
        return self.add(Context.tool_result(tool_call_id, content))
