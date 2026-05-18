# Default Memory Loading Rule

## Decision

Every agent in Agent-Team must load Agent-Memory by default before planning, tool selection, A2A handoff, or execution.

## Why

Agents should understand the system they operate in:

- SurrealDB is the canonical runtime/state backend.
- Agent-Traces defines trace/event semantics.
- Agent-Environment defines runtime context.
- Agent-Secrets defines secret handling.
- Agent-Objective defines completion expectations.
- Agent-Constraints defines policy boundaries.
- Agent-Eval, Agent-Trust, and Agent-FinOps define release-readiness signals.
- Agent-Memory stores prior decisions, reusable examples, and self-improvement learnings.

## Startup Flow

```text
agent starts
  → load memory context
  → load objective context
  → load constraints
  → load available skills/tools
  → plan
  → act
  → trace
  → evaluate/trust/finops
  → update memory where useful
```

## Required Memory Context

Each agent should receive:

```yaml
memory_context:
  platform_summary: required
  surrealdb_context: required
  trace_contracts: required
  current_objective: required
  constraints: required
  available_skills: required
  available_tools: required
  prior_decisions: required
  self_improvement_loop: required
```

## Self-Improvement Loop

```text
observe
  → plan
  → act
  → trace
  → evaluate
  → trust-check
  → cost-check
  → human-review if needed
  → update memory
  → improve next run
```

## Final Rule

```text
No agent acts before loading memory.
```
