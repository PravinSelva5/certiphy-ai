"""Compliance assessment subagent stub.

Eventually evaluates system design, documentation, and operational controls
against applicable EU AI Act requirements for the assigned risk tier.
"""

from governance_mcp.subagents.base import Subagent


class ComplianceAssessor(Subagent):
    """Stub for EU AI Act compliance assessment."""

    @property
    def name(self) -> str:
        return "compliance_assessor"

    async def execute(self, context: dict) -> dict:
        raise NotImplementedError
