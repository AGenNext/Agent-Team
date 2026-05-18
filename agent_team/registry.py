"""Agent registry for reusable goal-oriented teams."""

from __future__ import annotations

from dataclasses import dataclass, field

from agent_team.base import AgentRole, StaticReviewAgent


@dataclass
class AgentRegistry:
    """In-memory registry of reusable agents."""

    agents: dict[str, StaticReviewAgent] = field(default_factory=dict)

    def register(self, agent: StaticReviewAgent) -> None:
        if agent.role.agent_id in self.agents:
            raise ValueError(f"Agent already registered: {agent.role.agent_id}")
        self.agents[agent.role.agent_id] = agent

    def get(self, agent_id: str) -> StaticReviewAgent:
        try:
            return self.agents[agent_id]
        except KeyError as exc:
            raise KeyError(f"Unknown agent_id: {agent_id}") from exc

    def list_agent_ids(self) -> list[str]:
        return sorted(self.agents.keys())

    def list_roles(self) -> list[AgentRole]:
        return [self.agents[agent_id].role for agent_id in self.list_agent_ids()]


def _role(
    agent_id: str,
    name: str,
    goal: str,
    responsibilities: tuple[str, ...],
    outputs: tuple[str, ...],
    pass_criteria: tuple[str, ...],
    block_criteria: tuple[str, ...],
    tags: tuple[str, ...] = (),
) -> AgentRole:
    return AgentRole(
        agent_id=agent_id,
        name=name,
        goal=goal,
        responsibilities=responsibilities,
        inputs=("A2AHandoff", "Blueprint contract", "Product context", "Evidence refs"),
        outputs=outputs,
        pass_criteria=pass_criteria,
        block_criteria=block_criteria,
        tags=tags,
    )


def build_bootstrapped_team_registry() -> AgentRegistry:
    """Build the Ideation to Launch Team (Bootstrapped) registry."""

    registry = AgentRegistry()

    roles = [
        _role(
            "project_manager_agent",
            "Project Manager Agent",
            "Coordinate goal-oriented work from idea to launch using A2A-only handoffs.",
            (
                "decompose objectives into tasks",
                "route work to specialist agents",
                "track blockers and dependencies",
                "enforce review loops and handoff gates",
            ),
            ("task plan", "A2A routing decisions", "status report"),
            ("work is scoped", "next agent is clear", "blockers are visible"),
            ("unclear scope", "missing owner", "unresolved blocker"),
            ("orchestrator", "delivery"),
        ),
        _role(
            "product_manager_agent",
            "Product Manager Agent",
            "Validate customer value, use-case fit, and product acceptance criteria.",
            (
                "prioritize use cases",
                "define acceptance criteria",
                "prevent generic platform drift",
                "translate feedback into roadmap decisions",
            ),
            ("product review", "acceptance criteria", "roadmap recommendation"),
            ("customer value is clear", "acceptance criteria are testable"),
            ("unclear buyer", "weak use case", "missing acceptance criteria"),
            ("product", "customer"),
        ),
        _role(
            "functional_ux_validator_agent",
            "Functional UX Validator Agent",
            "Prove the intended user can complete the workflow and trust the output.",
            (
                "run scenario-based validation",
                "validate end-to-end usability",
                "check artifact usefulness",
                "block unusable workflows",
            ),
            ("functional UX validation report", "blocking usability issues"),
            ("user can complete task", "output is understandable and useful"),
            ("workflow fails", "output is not useful", "trust/provenance unclear"),
            ("ux", "validation"),
        ),
        _role(
            "ui_ux_designer_agent",
            "UI/UX Designer Agent",
            "Design clear workflows for source-to-artifact product experiences.",
            (
                "design user flows",
                "define screen behavior",
                "make citations and evaluations understandable",
                "review accessibility and clarity",
            ),
            ("UX spec", "workflow notes", "design risks"),
            ("workflow is clear", "user next action is obvious"),
            ("confusing workflow", "hidden control", "unclear approval gate"),
            ("design", "ux"),
        ),
        _role(
            "backend_implementation_agent",
            "Backend Implementation Agent",
            "Implement production-quality backend slices with tests and docs.",
            (
                "write backend code",
                "add schemas and APIs",
                "add tests",
                "document implementation",
            ),
            ("code changes", "tests", "implementation notes"),
            ("code runs", "tests pass", "errors handled"),
            ("scaffold only", "failing tests", "missing tenant scope"),
            ("engineering", "backend"),
        ),
        _role(
            "code_reviewer_agent",
            "Code Reviewer Agent",
            "Keep implementation simple, maintainable, tested, and production-minded.",
            (
                "review code quality",
                "check edge cases",
                "check test meaning",
                "prevent technical debt",
            ),
            ("code review", "required fixes"),
            ("code is maintainable", "tests are meaningful"),
            ("unsafe shortcut", "unhandled edge case", "missing regression test"),
            ("review", "quality"),
        ),
        _role(
            "architecture_agent",
            "Architecture Agent",
            "Preserve architecture boundaries, lossless-first design, and reusable contracts.",
            (
                "review system fit",
                "enforce repository boundaries",
                "validate versioning/diff/dedupe readiness",
                "check provider abstraction",
            ),
            ("architecture review", "boundary risks"),
            ("fits architecture", "future extensibility preserved"),
            ("boundary violation", "lossy source design", "tight coupling"),
            ("architecture", "systems"),
        ),
        _role(
            "security_compliance_agent",
            "Security and Compliance Agent",
            "Enforce enterprise security, license safety, and governance controls.",
            (
                "review tenant isolation",
                "review secrets and tokens",
                "review licenses and dependencies",
                "check auditability and policy controls",
            ),
            ("security review", "compliance risks"),
            ("no known critical security blocker", "license posture acceptable"),
            ("secret leakage", "unclear license", "tenant isolation risk"),
            ("security", "compliance"),
        ),
        _role(
            "qa_reliability_agent",
            "QA and Reliability Agent",
            "Validate tests, retry behavior, failure modes, and local reproducibility.",
            (
                "run tests",
                "check reliability risks",
                "validate idempotency",
                "require regression tests",
            ),
            ("QA report", "reliability risks"),
            ("tests pass", "failure modes understood"),
            ("non-retryable workflow", "unreproducible setup", "missing test"),
            ("qa", "reliability"),
        ),
        _role(
            "evaluation_quality_agent",
            "Evaluation and Quality Agent",
            "Validate output quality, grounding, citations, and evaluation criteria.",
            (
                "define evaluation rubric",
                "check grounding and citation coverage",
                "surface hallucination risk",
                "track quality metrics",
            ),
            ("evaluation report", "quality risks"),
            ("evaluation criteria are satisfied", "unsupported claims surfaced"),
            ("missing evaluation", "unsupported claim", "unclear quality gate"),
            ("evaluation", "quality"),
        ),
        _role(
            "deployment_agent",
            "Deployment Agent",
            "Validate deployability, environments, rollback, monitoring, and runtime config.",
            (
                "review environment readiness",
                "check deployment path",
                "verify rollback plan",
                "check observability",
            ),
            ("deployment review", "runtime risks"),
            ("deployment path is documented", "rollback is possible"),
            ("unsafe migration", "missing config", "no rollback plan"),
            ("deployment", "ops"),
        ),
        _role(
            "billing_admin_agent",
            "Billing and Admin Agent",
            "Ensure SaaS controls, metering, quotas, and admin governance are considered.",
            (
                "review metering impact",
                "review admin controls",
                "check quota implications",
                "validate billing events",
            ),
            ("billing/admin review", "metering requirements"),
            ("usage impact understood", "admin control path clear"),
            ("unmetered paid feature", "missing admin control", "quota bypass"),
            ("billing", "admin"),
        ),
        _role(
            "release_agent",
            "Release Agent",
            "Gate human handoff only after agent consensus and launch readiness.",
            (
                "verify specialist signoffs",
                "check blockers",
                "prepare handoff report",
                "emit release gate",
            ),
            ("release readiness report", "A2A release_gate"),
            ("no blockers", "risks documented", "handoff package complete"),
            ("blocked review", "missing test results", "unknown deployment risk"),
            ("release", "gate"),
        ),
        _role(
            "discussion_board_moderator_agent",
            "Discussion Board Moderator Agent",
            "Convert discussions and customer feedback into clean product signals.",
            (
                "moderate discussions",
                "classify feedback",
                "route actionable requests",
                "identify repeated pain points",
            ),
            ("feedback classification", "escalation recommendation"),
            ("feedback is categorized", "actionable items routed"),
            ("unclear feedback", "abuse/spam", "untriaged high-signal request"),
            ("community", "feedback"),
        ),
        _role(
            "marketing_content_writer_agent",
            "Marketing Content Writer Agent",
            "Create outcome-specific messaging and launch content without generic AI jargon.",
            (
                "write launch content",
                "translate features into outcomes",
                "maintain positioning",
                "create docs-to-marketing assets",
            ),
            ("marketing copy", "positioning review"),
            ("message is outcome-specific", "buyer value is clear"),
            ("generic RAG positioning", "unclear business value"),
            ("marketing", "content"),
        ),
        _role(
            "lead_generator_sales_manager_agent",
            "Lead Generator / Sales Manager Agent",
            "Validate commercial value, ICP, lead strategy, and revenue signals.",
            (
                "identify ICP",
                "generate lead hypotheses",
                "capture objections",
                "prioritize revenue-heavy use cases",
            ),
            ("sales signal report", "ICP recommendation", "objection log"),
            ("buyer and pain are clear", "commercial path exists"),
            ("no clear buyer", "weak urgency", "unpriced value"),
            ("sales", "gtm"),
        ),
    ]

    for role in roles:
        registry.register(StaticReviewAgent(role))

    return registry
