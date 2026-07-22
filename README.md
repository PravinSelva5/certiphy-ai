# certiphy-ai

MCP server for EU AI Act compliance evaluation of physical AI systems — robots, autonomous vehicles, industrial automation. Agent-first: a deterministic orchestrator decomposes an evaluation and dispatches specialized subagents for risk classification, obligation routing, sim-to-real validation, and audit reporting.

**Status:** foundation committed; subagent implementations in progress.

## What's committed vs in flight

This is an active build. The foundation is intentional and narrow; the LLM path is the work still open.

| Layer | State | What it is |
| --- | --- | --- |
| Typed contracts (`src/governance_mcp/subagents/base.py`) | **Committed** | Frozen Pydantic I/O; generic `Subagent[TInput, TOutput]`; typed `RiskClassifier` → `ComplianceAssessor` handoff via `ComplianceAssessorInput.from_classification()` |
| Architecture (`docs/ARCHITECTURE.md`) | **Committed** | Knowledge/reasoning separation; multi-regime extension path |
| Knowledge seam (`src/governance_mcp/knowledge/eu_ai_act.json`) | **Seam committed** | Jurisdictional obligations live as data, not code. Article 6(1)(a) automotive pathway content is the next fill — file is present so the load path is real |
| Subagent `execute()` implementations | **In flight** | Stubs exist; Claude calls + contract validation not yet wired |
| Orchestrator routing | **In flight** | Stub; will route on typed fields (`risk_tier`), never call the LLM |
| MCP `evaluate_compliance` tool | **Scaffold** | Server boots; end-to-end evaluation not implemented |

Scope discipline: contracts and architecture first, then one working LLM subagent, then the handoff edge. Not a dashboard of half-built agents.

## Design rationale

Three constraints shape the system:

1. **Orchestrator stays deterministic.** It reads typed fields and routes. It does not call the model.
2. **LLM calls live inside subagent `execute()` only.** Reasoning is localized; composition is checkable at the type boundary.
3. **Knowledge is data.** Obligation sets for a jurisdiction live in JSON. A second regime is a knowledge-file change, not a rewrite of the subagents.

The load-bearing edge is `risk_classifier → compliance_assessor`. That topology — classify by risk tier, then route obligations — is what most tiered AI regimes share. The EU AI Act (Article 6(1)(a) + Annex I automotive pathway) is the first instantiation. Same pattern, swapped knowledge file, extends to OSFI Guideline E-23, ISO 26262 / ISO 21448, dual-use safety cases, and UK AISI-style evaluation frameworks. Details in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Definition of done (next gate)

A fixed fixture enters and exits the type system cleanly:

1. Input: SAE L3 highway pilot as `RiskClassifierInput` (`system_description`, `deployment_context`, `sector="automotive"`).
2. `RiskClassifier.execute()` calls Claude; raw output is validated with `RiskClassifierOutput.model_validate` — no coercion on failure.
3. Output carries `risk_tier`, `applicable_pathway`, `reasoning`, `confidence`.
4. Handoff: `ComplianceAssessorInput.from_classification(output)` — the only sanctioned construction of the assessor payload.

When that gate passes, the artifact demonstrates a working multi-agent edge, not just a typed scaffold.

## Layout

```
src/governance_mcp/
  server.py              # MCP entry + tool registration
  orchestrator/          # deterministic routing (stub)
  subagents/
    base.py              # contracts (committed)
    risk_classifier.py   # in flight
    compliance_assessor.py
    sim_to_real_evaluator.py
    audit_reporter.py
  knowledge/
    eu_ai_act.json       # jurisdictional data seam
docs/
  ARCHITECTURE.md
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # set ANTHROPIC_API_KEY when exercising LLM paths
```

## Run

```bash
python -m governance_mcp.server
```

## Test

```bash
pytest
```
