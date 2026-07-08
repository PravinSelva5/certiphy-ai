# certiphy-ai

certiphy-ai is an MCP server for EU AI Act compliance evaluation of physical AI systems, including robots, autonomous vehicles, and industrial automation. The architecture is agent-first: an orchestrator decomposes compliance evaluations and dispatches specialized subagents for risk classification, assessment, sim-to-real validation, and audit reporting.

**Status:** in development

## Beyond the EU AI Act

The risk-classifier → obligation-routing topology is the load-bearing structure
for most regulatory regimes that classify AI systems by risk tier and attach
duties to each tier. Canada's OSFI Guideline E-23 (financial model risk, in force
May 2027), the Defence Industrial Strategy's dual-use safety cases, ISO 26262 /
ISO 21448 functional safety evidence packs, and UK AISI evaluation frameworks
are all candidates for the same orchestration pattern with a swapped knowledge
file. See ARCHITECTURE.md for the extension path.



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
