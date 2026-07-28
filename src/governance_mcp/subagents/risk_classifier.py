"""Risk classification subagent.

Calls Claude inside execute(), then validates the raw tool payload against
RiskClassifierOutput. The orchestrator never sees untyped LLM text — only a
frozen Pydantic object (or a ValidationError).
"""

from __future__ import annotations

import anthropic

from governance_mcp.subagents.base import (
    RiskClassifierInput,
    RiskClassifierOutput,
    Subagent,
)

# Forced tool name — Claude must call this tool; we never parse free text.
_TOOL_NAME = "record_risk_classification"

_SYSTEM_PROMPT = """\
You are an EU AI Act risk classifier for physical AI systems (robots, vehicles,
industrial automation).

Choose exactly one risk_tier from the tool schema enum. Guidance:
- high_risk_annex_i: AI safety component of a product covered by Annex I Union
  harmonisation legislation (e.g. type-approved motor vehicles) — Article 6(1)(a).
- high_risk_annex_iii: standalone high-risk use listed in Annex III.
- prohibited / limited / minimal: only when those regimes clearly apply.

Put the legal hook in applicable_pathway (e.g. "6(1)(a)"). Justify in reasoning.
Set confidence honestly (high / medium / low).
"""


class RiskClassifier(Subagent[RiskClassifierInput, RiskClassifierOutput]):
    """Classifies a system into an EU AI Act risk tier via Claude."""

    def __init__(
        self,
        client: anthropic.AsyncAnthropic | None = None,
        *,
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        # Inject a client in tests; production uses ANTHROPIC_API_KEY from env.
        self._client = client or anthropic.AsyncAnthropic()
        self._model = model

    @property
    def name(self) -> str:
        return "risk_classifier"

    async def execute(self, payload: RiskClassifierInput) -> RiskClassifierOutput:
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            tools=[
                {
                    "name": _TOOL_NAME,
                    "description": (
                        "Record the final EU AI Act risk classification."
                    ),
                    # Same shape as RiskClassifierOutput — Claude fills these fields.
                    "input_schema": RiskClassifierOutput.model_json_schema(),
                }
            ],
            # Force the tool: no prose-only answers that skip the contract.
            tool_choice={"type": "tool", "name": _TOOL_NAME},
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Classify this physical AI system under the EU AI Act.\n\n"
                        f"system_description: {payload.system_description}\n"
                        f"deployment_context: {payload.deployment_context}\n"
                        f"sector: {payload.sector}"
                    ),
                }
            ],
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == _TOOL_NAME:
                # Contract gate: wrong enum / missing field → ValidationError.
                return RiskClassifierOutput.model_validate(block.input)

        raise RuntimeError(
            f"{self.name}: expected a tool_use block named {_TOOL_NAME!r}"
        )
