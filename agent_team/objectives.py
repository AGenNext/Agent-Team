"""Objective-aware task models for Agent-Team.

Agent-Objective owns the canonical objective contract. This module provides a
small runtime-compatible model so Agent-Team can execute against objective-shaped
work without owning the objective policy.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ObjectiveStatus(StrEnum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DECOMPOSED = "decomposed"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ObjectiveRef(BaseModel):
    """Reference to an objective governed by Agent-Objective."""

    objective_id: str = Field(default_factory=lambda: f"objective-{uuid4()}")
    title: str
    target_outcome: str
    owner_agent: str = "project_manager_agent"
    status: ObjectiveStatus = ObjectiveStatus.PROPOSED
    completion_criteria: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    required_agents: list[str] = Field(default_factory=list)
    required_evidence: list[str] = Field(default_factory=list)
    validation_method: str = "agent consensus plus release gate"
    stop_conditions: list[str] = Field(default_factory=list)
    human_approval_required: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def is_complete(self) -> bool:
        return self.status == ObjectiveStatus.COMPLETED

    def can_rest(self) -> bool:
        """Agents may rest only after completion or an approved terminal status."""

        return self.status in {ObjectiveStatus.COMPLETED, ObjectiveStatus.CANCELLED}
