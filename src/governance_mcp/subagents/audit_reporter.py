"""Audit reporting subagent stub.

Eventually synthesizes subagent findings into structured audit reports
suitable for internal review and regulatory documentation.
"""

from governance_mcp.subagents.base import Subagent


class AuditReporter(Subagent):
    """Stub for compliance audit report generation."""

    @property
    def name(self) -> str:
        return "audit_reporter"

    async def execute(self, context: dict) -> dict:
        raise NotImplementedError
