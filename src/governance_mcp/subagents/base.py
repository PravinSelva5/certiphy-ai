"""Typed contracts for compliance evaluation subagents.

The orchestration model: each Subagent declares the exact shape of what it
consumes and what it produces. The dependency edge between subagents
(risk_classifier -> compliance_assessor) is therefore expressed in the type
system: ComplianceAssessor's input is constructed from RiskClassifier's output,
so a mismatch is a static type error, not a runtime surprise.

Orchestrator stays deterministic (it routes based on typed fields it can read);
LLM calls live inside subagent .execute() implementations only.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


# --- Contract primitives -----------------------------------------------------


class SubagentInput(BaseModel):
    """Base class for everything a subagent consumes.

    Pydantic gives validation + a stable serialized form for logging/audit.
    Subclasses add the fields a specific subagent needs.
    """

    model_config = {"frozen": True}  # inputs are immutable once constructed


class SubagentOutput(BaseModel):
    """Base class for everything a subagent produces."""

    model_config = {"frozen": True}


TInput = TypeVar("TInput", bound=SubagentInput)
TOutput = TypeVar("TOutput", bound=SubagentOutput)


# --- The generic subagent contract -------------------------------------------


class Subagent(ABC, Generic[TInput, TOutput]):
    """Abstract base for a specialized compliance subagent.

    Generic over its input and output contract. A concrete subagent binds the
    type parameters, e.g.:

        class RiskClassifier(Subagent[RiskClassifierInput, RiskClassifierOutput]):
            ...

    which makes the I/O shape part of the class's identity and lets the
    orchestrator (and a type checker) reason about how subagents compose.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable subagent identifier (e.g. 'risk_classifier')."""
        ...

    @abstractmethod
    async def execute(self, payload: TInput) -> TOutput:
        """Run subagent logic against a typed, validated payload.

        Implementations may call the LLM here. The return value must satisfy
        the declared TOutput contract.
        """
        ...


# --- Concrete contracts: the risk_classifier -> compliance_assessor edge -----
#
# These live here (rather than in each subagent module) so the dependency edge
# is readable in one place. The knowledge they reason over (Annex III data,
# sectoral law mappings) lives in eu_ai_act.json, not in these types — keeping
# knowledge and reasoning separate so a second jurisdiction is a data change,
# not a code change.


class SystemProfile(BaseModel):
    """Description of the physical-AI system being assessed.

    This is the user-facing entry payload. Keep it descriptive, not
    EU-specific, so the same profile could be evaluated against another
    jurisdiction later.
    """

    model_config = {"frozen": True}

    name: str
    description: str
    deployment_context: str  # e.g. "passenger vehicle, public roads"
    autonomy_level: str  # free-text or enum-like, e.g. "SAE L3"
    # Extension point: add structured capability/sector tags here as the
    # classifier grows. Kept loose deliberately for the gate build.



# A small, explicit vocabulary for risk tiers keeps routing deterministic.
# (Using a Literal rather than str so the orchestrator's branches are
# exhaustive-checkable.)
from typing import Literal

RiskTier = Literal[
        "prohibited",
        "high_risk_annex_i",
        "high_risk_annex_iii",
        "limited",
        "minimal"
]


class RiskClassifierInput(SubagentInput):
    system_description: str
    deployment_context: str
    sector: str


class RiskClassifierOutput(SubagentOutput):
    """What the risk_classifier produces.

    `applicable_pathway` is the EU AI Act hook (e.g. '6(1)(a)') that the
    classifier identified; `reasoning` carries the LLM's reasoning for audit.
    The orchestrator reads `risk_tier` to decide whether to route onward to the
    compliance_assessor.
    """

    risk_tier: RiskTier
    applicable_pathway: str
    reasoning: str
    confidence: Literal["high", "medium", "low"]


class ComplianceAssessorInput(SubagentInput):
    """What the compliance_assessor consumes.

    Constructed *from* a RiskClassifierOutput — this is the typed handoff. The
    classmethod is the single sanctioned way to build it, so the edge is
    explicit and the orchestrator can't accidentally hand over a half-built
    payload.
    """

    classification: RiskClassifierOutput

    @classmethod
    def from_classification(
        cls, output: RiskClassifierOutput
    ) -> ComplianceAssessorInput:
        return cls(classification=output)


class Obligation(BaseModel):
    """A single routed compliance obligation."""

    model_config = {"frozen": True}

    source: str  # e.g. "GSR 2019/2144", "ISO 26262"
    requirement: str
    citation: str  # article/clause for traceability


class ComplianceAssessorOutput(SubagentOutput):
    """What the compliance_assessor produces: the routed obligation set."""

    risk_tier: RiskTier
    applicable_article: str
    obligations: list[Obligation]
    summary: str