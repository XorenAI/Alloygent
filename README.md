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

## Publishing

Build and publish from your laptop with a PyPI API token:

```bash
uv build
uv publish --token "pypi-..."
```

The GitHub workflow builds release distributions for tags and manual runs, but
does not upload to PyPI.
