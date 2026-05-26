"""Abstract base class for compliance evaluation subagents."""

from abc import ABC, abstractmethod


class Subagent(ABC):
    """Abstract base for specialized compliance subagents."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable subagent identifier."""
        ...

    @abstractmethod
    async def execute(self, context: dict) -> dict:
        """Run subagent logic against the given evaluation context."""
        ...
