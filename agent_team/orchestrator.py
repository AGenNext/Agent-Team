"""Framework-neutral Project Manager orchestrator.

LangGraph execution adapters belong in Agent-Frameworks. This module keeps the
team-level decision logic reusable and testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agent_team.a2a.models import (
    A2AHandoff,
    A2AResponse,
    HandoffContext,
    HandoffStatus,
    HandoffType,
    Priority,
    RequestedAction,
)
from agent_team.registry import AgentRegistry


@dataclass(frozen=True)
class OrchestrationStep:
    """A single planned A2A handoff target in a team workflow."""

    target_agent: str
    handoff_type: HandoffType
    action: str
    expected_output: str
    acceptance_criteria: tuple[str, ...] = ()


@dataclass
class OrchestrationResult:
    """Result of running a framework-neutral orchestration plan."""

    task_id: str
    responses: list[A2AResponse] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        return any(response.status == HandoffStatus.BLOCKED for response in self.responses)

    @property
    def rejected(self) -> bool:
        return any(response.status == HandoffStatus.REJECTED for response in self.responses)

    @property
    def ready_for_human_review(self) -> bool:
        if not self.responses:
            return False
        return not self.blocked and not self.rejected


class ProjectManagerOrchestrator:
    """Decision orchestrator for the Ideation to Launch Team.

    The Project Manager Agent coordinates. Framework runtimes execute.
    """

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry
        self.agent_id = "project_manager_agent"

    def default_launch_plan(self) -> list[OrchestrationStep]:
        """Return the default internal review chain before human handoff."""

        return [
            OrchestrationStep(
                target_agent="product_manager_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate customer value, use-case fit, and acceptance criteria.",
                expected_output="Product review with pass/block criteria.",
                acceptance_criteria=("customer value is clear", "acceptance criteria are testable"),
            ),
            OrchestrationStep(
                target_agent="ui_ux_designer_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate user workflow and experience design.",
                expected_output="UX review with risks and required fixes.",
                acceptance_criteria=("workflow is clear", "user next action is obvious"),
            ),
            OrchestrationStep(
                target_agent="functional_ux_validator_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate that the intended user can complete the workflow successfully.",
                expected_output="Functional UX validation report.",
                acceptance_criteria=("user can complete task", "output is understandable and useful"),
            ),
            OrchestrationStep(
                target_agent="architecture_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate architecture fit and repository boundaries.",
                expected_output="Architecture review.",
                acceptance_criteria=("fits architecture", "future extensibility preserved"),
            ),
            OrchestrationStep(
                target_agent="security_compliance_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate security, compliance, license, and trust posture.",
                expected_output="Security and compliance review.",
                acceptance_criteria=("no known critical security blocker", "license posture acceptable"),
            ),
            OrchestrationStep(
                target_agent="qa_reliability_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate tests, reliability, failure modes, and reproducibility.",
                expected_output="QA and reliability review.",
                acceptance_criteria=("tests pass", "failure modes understood"),
            ),
            OrchestrationStep(
                target_agent="evaluation_quality_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate quality gates, evaluation criteria, grounding, and citations.",
                expected_output="Evaluation quality review.",
                acceptance_criteria=("evaluation criteria are satisfied", "unsupported claims surfaced"),
            ),
            OrchestrationStep(
                target_agent="billing_admin_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate billing, metering, quota, and admin implications.",
                expected_output="Billing and admin review.",
                acceptance_criteria=("usage impact understood", "admin control path clear"),
            ),
            OrchestrationStep(
                target_agent="deployment_agent",
                handoff_type=HandoffType.REVIEW,
                action="Validate deployment, environments, rollback, and observability.",
                expected_output="Deployment readiness review.",
                acceptance_criteria=("deployment path is documented", "rollback is possible"),
            ),
            OrchestrationStep(
                target_agent="release_agent",
                handoff_type=HandoffType.RELEASE_GATE,
                action="Gate human review only after specialist agent consensus.",
                expected_output="Release readiness report and human handoff recommendation.",
                acceptance_criteria=("no blockers", "risks documented", "handoff package complete"),
            ),
        ]

    def run_plan(
        self,
        *,
        task_id: str,
        objective: str,
        scope: str,
        plan: list[OrchestrationStep] | None = None,
        priority: Priority = Priority.MEDIUM,
    ) -> OrchestrationResult:
        """Run a deterministic A2A review plan against the registered agents."""

        selected_plan = plan or self.default_launch_plan()
        result = OrchestrationResult(task_id=task_id)
        previous_handoffs: list[str] = []

        for step in selected_plan:
            handoff = A2AHandoff(
                source_agent=self.agent_id,
                target_agent=step.target_agent,
                task_id=task_id,
                handoff_type=step.handoff_type,
                priority=priority,
                context=HandoffContext(
                    summary=f"Orchestration step for {task_id}: {step.action}",
                    objective=objective,
                    scope=scope,
                    constraints=[
                        "All agent-to-agent transfers must use A2A.",
                        "Human review only after agent consensus.",
                        "Runtime/framework orchestration belongs in Agent-Frameworks.",
                    ],
                    assumptions=[
                        "Project Manager Agent is the decision orchestrator.",
                        "Specialist agents may block release if their criteria are not met.",
                    ],
                ),
                acceptance_criteria=list(step.acceptance_criteria),
                requested_action=RequestedAction(
                    action=step.action,
                    expected_output=step.expected_output,
                ),
            )
            handoff.trace.previous_handoffs = previous_handoffs.copy()
            agent = self.registry.get(step.target_agent)
            response = agent.receive(handoff)
            result.responses.append(response)
            previous_handoffs.append(handoff.handoff_id)

            if response.status in {HandoffStatus.BLOCKED, HandoffStatus.REJECTED}:
                break

        return result
