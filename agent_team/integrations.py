"""Integration hook models for the AGenNext agent ecosystem.

Agent-Team coordinates work but does not own skills, model routing, evaluation,
benchmarks, trust, analytics, research, frameworks, environments, or schemas.
These lightweight refs keep ownership boundaries explicit while giving product
repos a stable integration shape.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class IntegrationOwner(StrEnum):
    AGENT_OBJECTIVE = "Agent-Objective"
    AGENT_BLUEPRINT = "Agent-Blueprint"
    AGENT_CONSTRAINTS = "Agent-Constraints"
    AGENT_SKILLS = "Agent-Skills"
    MODEL_ROUTER = "Model-Router"
    AGENT_BENCH = "Agent-Bench"
    AGENT_EVAL = "Agent-Eval"
    AGENT_TRUST = "Agent-Trust"
    AGENT_ANALYTICS = "Agent-Analytics"
    AGENT_RESEARCH = "Agent-Research"
    AGENT_FRAMEWORKS = "Agent-Frameworks"
    AGENT_ENVIRONMENT = "Agent-Environment"
    AGENT_GRAPH = "Agent-Graph"
    PRODUCT_REPOSITORY = "Product-Repository"


class HookStatus(StrEnum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class EcosystemHook(BaseModel):
    hook_id: str = Field(default_factory=lambda: f"hook-{uuid4()}")
    owner: IntegrationOwner
    purpose: str
    reference: str
    status: HookStatus = HookStatus.REQUIRED
    required_for_human_handoff: bool = True
    evidence_refs: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TeamExecutionContext(BaseModel):
    """A portable context object for Agent-Team execution."""

    task_id: str
    objective_ref: str | None = None
    blueprint_ref: str | None = None
    constraint_refs: list[str] = Field(default_factory=list)
    skill_refs: list[str] = Field(default_factory=list)
    model_routing_ref: str | None = None
    benchmark_refs: list[str] = Field(default_factory=list)
    evaluation_refs: list[str] = Field(default_factory=list)
    trust_refs: list[str] = Field(default_factory=list)
    analytics_refs: list[str] = Field(default_factory=list)
    research_refs: list[str] = Field(default_factory=list)
    framework_ref: str | None = None
    environment_ref: str | None = None
    schema_refs: list[str] = Field(default_factory=list)
    product_ref: str | None = None
    hooks: list[EcosystemHook] = Field(default_factory=list)

    def blocking_hooks(self) -> list[EcosystemHook]:
        return [
            hook
            for hook in self.hooks
            if hook.required_for_human_handoff and hook.status == HookStatus.BLOCKED
        ]

    def missing_required_hooks(self) -> list[EcosystemHook]:
        return [
            hook
            for hook in self.hooks
            if hook.required_for_human_handoff and hook.status == HookStatus.REQUIRED
        ]

    def ready_for_human_handoff(self) -> bool:
        return not self.blocking_hooks() and not self.missing_required_hooks()


def default_ecosystem_hooks() -> list[EcosystemHook]:
    """Return the default ecosystem hooks expected by Agent-Team."""

    return [
        EcosystemHook(
            owner=IntegrationOwner.AGENT_OBJECTIVE,
            purpose="Objective contract and completion criteria",
            reference="Agent-Objective/objectives/objective-completion-policy.md",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_CONSTRAINTS,
            purpose="Policy constraints, including LLM/provider selection constraints",
            reference="Agent-Constraints/constraints/llm-provider-selection-policy.md",
        ),
        EcosystemHook(
            owner=IntegrationOwner.MODEL_ROUTER,
            purpose="Compliant model/provider routing",
            reference="Model-Router/docs/agent-model-routing-contract.md",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_SKILLS,
            purpose="Skill/capability declarations required by agent roles",
            reference="Agent-Skills/contracts/skill-registry-contract.md",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_EVAL,
            purpose="Evaluation rubrics and CLEAR-style scoring",
            reference="Agent-Eval",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_BENCH,
            purpose="Reproducible benchmark tasks",
            reference="Agent-Bench/contracts/benchmark-contract.md",
            required_for_human_handoff=False,
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_TRUST,
            purpose="Trust, provenance, and evidence contracts",
            reference="Agent-Trust/contracts/trust-contract.md",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_ANALYTICS,
            purpose="Analytics events and improvement metrics",
            reference="Agent-Analytics/docs/agent-analytics-contract.md",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_FRAMEWORKS,
            purpose="Runtime adapter boundary, including LangGraph",
            reference="Agent-Frameworks",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_ENVIRONMENT,
            purpose="Development, test, staging, and production environment contracts",
            reference="Agent-Environment",
        ),
        EcosystemHook(
            owner=IntegrationOwner.AGENT_GRAPH,
            purpose="Artifact schemas where relevant",
            reference="Agent-Graph/schemas/artifacts",
            required_for_human_handoff=False,
        ),
    ]
