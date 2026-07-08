## Extension Path

The deterministic orchestrator and the typed `RiskClassifier → ComplianceAssessor`
handoff edge form a pattern that generalizes across any regulatory regime sharing
the same shape: a tier-based risk taxonomy plus an obligation lookup keyed by
sector or article. The current build instantiates this pattern for the EU AI Act
(Article 6(1)(a) + Annex I automotive pathway). With a swapped or additional
`*.json` knowledge file and no code changes to subagents, the same topology
extends to:

- **OSFI Guideline E-23 (Canada, in force May 2027)** — enterprise model risk
  management for federally regulated financial institutions; materiality-tiered,
  obligations keyed by lifecycle stage.
- **ISO 26262 + ISO 21448 (SOTIF)** — functional safety and intended-functionality
  evidence for automotive AI; ASIL classification routes to specific work products.
- **Canadian Defence Industrial Strategy dual-use safety cases** — Uncrewed
  Systems designated a Tier 1 Sovereign Capability creates a parallel obligation
  structure under IDEaS and ITB frameworks.
- **UK AISI / EU AI Office model evaluation frameworks** — safety cases share the
  same classification → obligation routing shape.

This isn't a roadmap; it's a statement that the load-bearing value of the
architecture is the separation of knowledge (jurisdictional obligations) from
reasoning (subagent LLM calls). That separation is what makes multi-regime
extension a knowledge-file change rather than a code change.