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

This repository is configured for PyPI Trusted Publishing through GitHub Actions.
Create a PyPI trusted publisher for:

- Repository: `XorenAI/Alloygent`
- Workflow: `publish.yml`
- Environment: `pypi`

Then publish a release by pushing a version tag:

```bash
git tag v0.1.1
git push origin v0.1.1
```
