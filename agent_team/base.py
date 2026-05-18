"""Base agent contract for reusable Agent-Team roles."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from agent_team.a2a.models import A2AHandoff, A2AResponse, HandoffStatus


@dataclass(frozen=True)
class AgentRole:
    """Describes a reusable agent role."""

    agent_id: str
    name: str
    goal: str
    responsibilities: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    pass_criteria: tuple[str, ...]
    block_criteria: tuple[str, ...]
    tags: tuple[str, ...] = field(default_factory=tuple)


class Agent(Protocol):
    """Protocol implemented by every reusable agent."""

    role: AgentRole

    def receive(self, handoff: A2AHandoff) -> A2AResponse:
        """Receive an official A2A handoff and return an A2A response."""
        ...


class StaticReviewAgent:
    """Deterministic baseline agent implementation.

    This is intentionally simple. It gives every role a runnable implementation while
    framework-specific reasoning/runtime support is added in Agent-Frameworks.
    """

    def __init__(self, role: AgentRole) -> None:
        self.role = role

    def receive(self, handoff: A2AHandoff) -> A2AResponse:
        if handoff.target_agent != self.role.agent_id:
            return A2AResponse(
                response_to=handoff.handoff_id,
                responder_agent=self.role.agent_id,
                status=HandoffStatus.REJECTED,
                summary="Handoff target does not match this agent.",
                findings=[f"Expected target_agent={self.role.agent_id}, got {handoff.target_agent}."],
                required_fixes=["Route the handoff to the correct target_agent."],
            )

        blockers = list(handoff.risks.blockers)
        if blockers:
            return A2AResponse(
                response_to=handoff.handoff_id,
                responder_agent=self.role.agent_id,
                status=HandoffStatus.BLOCKED,
                summary="Handoff contains blockers that must be resolved before this agent can pass it.",
                findings=blockers,
                required_fixes=["Resolve blockers and submit a corrected A2A handoff."],
            )

        return A2AResponse(
            response_to=handoff.handoff_id,
            responder_agent=self.role.agent_id,
            status=HandoffStatus.ACCEPTED,
            summary=f"{self.role.name} accepted the A2A handoff for review/work.",
            findings=["A2A envelope is structurally valid and targeted to this agent."],
            next_agent=None,
            next_action="Proceed according to role responsibilities and acceptance criteria.",
        )
