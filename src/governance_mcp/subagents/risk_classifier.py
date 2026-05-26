"""Risk classification subagent stub.

Eventually classifies physical AI systems under the EU AI Act risk tiers
(unacceptable, high, limited, minimal) based on system context and use case.
"""

from governance_mcp.subagents.base import Subagent


class RiskClassifier(Subagent):
    """Stub for EU AI Act risk tier classification."""

    @property
    def name(self) -> str:
        return "risk_classifier"

    async def execute(self, context: dict) -> dict:
        raise NotImplementedError
