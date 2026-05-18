"""Governed LLM provider selection for Agent-Team.

The team may use only:
- local open-source models
- open-source model runtimes
- free-tier APIs

Paid-only, unclear-license, or untrusted providers must be rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProviderKind(StrEnum):
    LOCAL_OPEN_SOURCE = "local_open_source"
    OPEN_SOURCE_RUNTIME = "open_source_runtime"
    FREE_TIER_API = "free_tier_api"
    PAID_API = "paid_api"
    UNKNOWN = "unknown"


class ProviderDecision(StrEnum):
    ALLOW = "allow"
    REJECT = "reject"
    ESCALATE = "escalate"


PREFERRED_LICENSES = {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
}

CONDITIONAL_LICENSES = {
    "MPL-2.0",
    "LGPL-2.1",
    "LGPL-3.0",
}

BLOCKED_LICENSES = {
    "AGPL-3.0",
    "GPL-2.0",
    "GPL-3.0",
    "NOASSERTION",
    "UNKNOWN",
    "Proprietary",
    "Non-Commercial",
}


@dataclass(frozen=True)
class LLMProviderCandidate:
    name: str
    kind: ProviderKind
    license: str
    trusted_source: bool
    requires_payment: bool = False
    requires_external_data_transfer: bool = False
    notes: str = ""


@dataclass(frozen=True)
class LLMProviderEvaluation:
    candidate: LLMProviderCandidate
    decision: ProviderDecision
    reasons: tuple[str, ...]


class LLMProviderSelector:
    """Selects only safe local/open-source/free-tier LLM providers."""

    def evaluate(self, candidate: LLMProviderCandidate) -> LLMProviderEvaluation:
        reasons: list[str] = []

        if candidate.license in BLOCKED_LICENSES:
            return LLMProviderEvaluation(
                candidate=candidate,
                decision=ProviderDecision.REJECT,
                reasons=(f"blocked license: {candidate.license}",),
            )

        if not candidate.trusted_source:
            return LLMProviderEvaluation(
                candidate=candidate,
                decision=ProviderDecision.REJECT,
                reasons=("provider source is not trusted",),
            )

        if candidate.requires_payment or candidate.kind == ProviderKind.PAID_API:
            return LLMProviderEvaluation(
                candidate=candidate,
                decision=ProviderDecision.REJECT,
                reasons=("paid-only providers are not allowed by Agent-Team policy",),
            )

        if candidate.kind in {
            ProviderKind.LOCAL_OPEN_SOURCE,
            ProviderKind.OPEN_SOURCE_RUNTIME,
        }:
            if candidate.license in PREFERRED_LICENSES:
                reasons.append("local/open-source provider with preferred license")
                return LLMProviderEvaluation(candidate, ProviderDecision.ALLOW, tuple(reasons))
            if candidate.license in CONDITIONAL_LICENSES:
                reasons.append("conditional license requires human/security review")
                return LLMProviderEvaluation(candidate, ProviderDecision.ESCALATE, tuple(reasons))

        if candidate.kind == ProviderKind.FREE_TIER_API:
            if candidate.requires_external_data_transfer:
                reasons.append("free-tier API transfers data externally; requires policy review")
                return LLMProviderEvaluation(candidate, ProviderDecision.ESCALATE, tuple(reasons))
            reasons.append("free-tier API allowed when no suitable local option exists")
            return LLMProviderEvaluation(candidate, ProviderDecision.ALLOW, tuple(reasons))

        return LLMProviderEvaluation(
            candidate=candidate,
            decision=ProviderDecision.REJECT,
            reasons=("provider does not meet local/open-source/free-tier policy",),
        )

    def select_first_allowed(
        self, candidates: list[LLMProviderCandidate]
    ) -> LLMProviderEvaluation | None:
        """Return the first allowed provider, preferring earlier candidate order."""

        for candidate in candidates:
            evaluation = self.evaluate(candidate)
            if evaluation.decision == ProviderDecision.ALLOW:
                return evaluation
        return None
