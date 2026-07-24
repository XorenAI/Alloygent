# Alloygent

A typed Python library for building agent workflows from plain functions.

## Install

```bash
pip install alloygent
```

## Development

```bash
uv sync
uv run ruff check .
uv build
```

## Usage

```python
from alloygent import Agent, Context, Model, ModelResponse, tool


class EchoModel(Model):
    def _call(self, messages: list[Context], tools=None, **params) -> ModelResponse:
        last_message = messages[-1].content
        return ModelResponse(message=f"Echo: {last_message}")


@tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


agent = Agent(model=EchoModel("echo"), tools=[add])
result = agent.run("hello")
print(result.message)
```

## Publishing

Build and publish from your laptop with a PyPI API token:

```bash
uv build
uv publish --token "pypi-..."
```

The GitHub workflow builds release distributions for tags and manual runs, but
does not upload to PyPI.
