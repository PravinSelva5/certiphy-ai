"""Sim-to-real evaluation subagent stub.

Eventually assesses gaps between simulated training/validation environments
and real-world deployment conditions for physical AI systems.
"""

from governance_mcp.subagents.base import Subagent


class SimToRealEvaluator(Subagent):
    """Stub for sim-to-real compliance evaluation."""

    @property
    def name(self) -> str:
        return "sim_to_real_evaluator"

    async def execute(self, context: dict) -> dict:
        raise NotImplementedError
