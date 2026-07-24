import json
from dataclasses import dataclass, field
from typing import Any

from ._history import Context
from ._model import Model, ModelResponse
from ._tool import Tool


@dataclass
class AgentResult:
    message: str
    response: ModelResponse
    history: list[Context]


@dataclass
class Agent:
    model: Model
    tools: list[Tool] = field(default_factory=list)
    system_prompt: str | None = None
    max_tool_rounds: int = 5

    def __post_init__(self) -> None:
        self._tool_map = {tool.name: tool for tool in self.tools}

    def run(
        self,
        prompt: str,
        history: list[Context] | None = None,
        **params: Any,
    ) -> AgentResult:
        messages = list(history or [])
        if self.system_prompt and not messages:
            messages.append(Context.system(self.system_prompt))
        messages.append(Context.user(prompt))

        response = self.model.call(messages, tools=self.tools, **params)
        rounds = 0

        while response.tool_calls and rounds < self.max_tool_rounds:
            messages.append(Context.assistant(response.message, response.tool_calls))

            for call in response.tool_calls:
                result = self._run_tool(call.name, call.arguments)
                messages.append(Context.tool_result(call.id, self._stringify(result)))

            response = self.model.call(messages, tools=self.tools, **params)
            rounds += 1

        messages.append(Context.assistant(response.message, response.tool_calls))
        return AgentResult(
            message=response.message,
            response=response,
            history=messages,
        )

    def _run_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        try:
            selected_tool = self._tool_map[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._tool_map)) or "none"
            raise ValueError(f"Unknown tool {name!r}. Available tools: {available}") from exc
        return selected_tool.run(arguments)

    @staticmethod
    def _stringify(value: Any) -> str:
        if isinstance(value, str):
            return value
        try:
            return json.dumps(value)
        except TypeError:
            return str(value)


@dataclass
class SubAgent(Agent):
    name: str = "sub_agent"
    description: str = "Run a delegated agent task."

    def as_tool(self) -> Tool:
        def run(task: str) -> str:
            return self.run(task).message

        return Tool(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {"task": {"type": "string"}},
                "required": ["task"],
            },
            fn=run,
        )
