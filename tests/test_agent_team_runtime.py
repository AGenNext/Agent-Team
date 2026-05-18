from agent_team import build_bootstrapped_team_registry
from agent_team.a2a.models import (
    A2AHandoff,
    HandoffContext,
    HandoffStatus,
    HandoffType,
    RequestedAction,
)
from agent_team.orchestrator import ProjectManagerOrchestrator


def test_bootstrapped_registry_contains_required_agents() -> None:
    registry = build_bootstrapped_team_registry()

    agent_ids = set(registry.list_agent_ids())

    assert "project_manager_agent" in agent_ids
    assert "product_manager_agent" in agent_ids
    assert "functional_ux_validator_agent" in agent_ids
    assert "release_agent" in agent_ids
    assert "lead_generator_sales_manager_agent" in agent_ids


def test_agent_accepts_valid_a2a_handoff() -> None:
    registry = build_bootstrapped_team_registry()
    product_agent = registry.get("product_manager_agent")

    handoff = A2AHandoff(
        source_agent="project_manager_agent",
        target_agent="product_manager_agent",
        task_id="test-task",
        handoff_type=HandoffType.REVIEW,
        context=HandoffContext(
            summary="Validate product value.",
            objective="Confirm customer value.",
            scope="Unit test scope.",
        ),
        requested_action=RequestedAction(
            action="Review product fit.",
            expected_output="Product review.",
        ),
    )

    response = product_agent.receive(handoff)

    assert response.protocol == "A2A"
    assert response.response_to == handoff.handoff_id
    assert response.responder_agent == "product_manager_agent"
    assert response.status == HandoffStatus.ACCEPTED


def test_agent_rejects_wrong_target_handoff() -> None:
    registry = build_bootstrapped_team_registry()
    product_agent = registry.get("product_manager_agent")

    handoff = A2AHandoff(
        source_agent="project_manager_agent",
        target_agent="security_compliance_agent",
        task_id="test-task",
        handoff_type=HandoffType.REVIEW,
        context=HandoffContext(
            summary="Wrong target.",
            objective="Confirm target validation.",
            scope="Unit test scope.",
        ),
        requested_action=RequestedAction(
            action="Review product fit.",
            expected_output="Product review.",
        ),
    )

    response = product_agent.receive(handoff)

    assert response.status == HandoffStatus.REJECTED
    assert response.required_fixes


def test_project_manager_orchestrator_runs_default_plan() -> None:
    registry = build_bootstrapped_team_registry()
    orchestrator = ProjectManagerOrchestrator(registry)

    result = orchestrator.run_plan(
        task_id="launch-test",
        objective="Validate launch readiness.",
        scope="Unit test orchestration scope.",
    )

    assert result.responses
    assert not result.blocked
    assert not result.rejected
    assert result.ready_for_human_review
    assert result.responses[-1].responder_agent == "release_agent"
