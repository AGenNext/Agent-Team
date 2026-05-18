"""A2A protocol models for official agent-to-agent handoffs."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


A2A_PROTOCOL = "A2A"
A2A_PROTOCOL_VERSION = "0.1.0"


class HandoffType(StrEnum):
    REQUEST = "request"
    REVIEW = "review"
    APPROVAL = "approval"
    ESCALATION = "escalation"
    CORRECTION = "correction"
    RELEASE_GATE = "release_gate"


class HandoffStatus(StrEnum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class HandoffContext(BaseModel):
    summary: str
    objective: str
    scope: str
    constraints: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class HandoffArtifacts(BaseModel):
    changed_files: list[str] = Field(default_factory=list)
    related_docs: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)


class HandoffChecks(BaseModel):
    tests: list[str] = Field(default_factory=list)
    evaluations: list[str] = Field(default_factory=list)
    security_checks: list[str] = Field(default_factory=list)
    policy_checks: list[str] = Field(default_factory=list)


class HandoffRisks(BaseModel):
    known_risks: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)


class RequestedAction(BaseModel):
    action: str
    expected_output: str
    deadline: str | None = None


class HandoffTrace(BaseModel):
    previous_handoffs: list[str] = Field(default_factory=list)
    decision_refs: list[str] = Field(default_factory=list)
    audit_refs: list[str] = Field(default_factory=list)


class A2AHandoff(BaseModel):
    protocol: Literal["A2A"] = A2A_PROTOCOL
    protocol_version: str = A2A_PROTOCOL_VERSION
    handoff_id: str = Field(default_factory=lambda: f"a2a-{uuid4()}")
    source_agent: str
    target_agent: str
    task_id: str
    parent_task_id: str | None = None
    handoff_type: HandoffType
    status: HandoffStatus = HandoffStatus.PROPOSED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    priority: Priority = Priority.MEDIUM
    context: HandoffContext
    artifacts: HandoffArtifacts = Field(default_factory=HandoffArtifacts)
    acceptance_criteria: list[str] = Field(default_factory=list)
    checks_performed: HandoffChecks = Field(default_factory=HandoffChecks)
    risks: HandoffRisks = Field(default_factory=HandoffRisks)
    requested_action: RequestedAction
    trace: HandoffTrace = Field(default_factory=HandoffTrace)


class A2AResponse(BaseModel):
    protocol: Literal["A2A"] = A2A_PROTOCOL
    protocol_version: str = A2A_PROTOCOL_VERSION
    response_to: str
    responder_agent: str
    status: HandoffStatus
    summary: str
    findings: list[str] = Field(default_factory=list)
    required_fixes: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    next_agent: str | None = None
    next_action: str | None = None
