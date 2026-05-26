# certiphy-ai

certiphy-ai is an MCP server for EU AI Act compliance evaluation of physical AI systems, including robots, autonomous vehicles, and industrial automation. The architecture is agent-first: an orchestrator decomposes compliance evaluations and dispatches specialized subagents for risk classification, assessment, sim-to-real validation, and audit reporting.

**Status:** in development

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

Start the MCP server:

```bash
python -m governance_mcp.server
```

## Test

```bash
pytest
```
