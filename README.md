# Agent Team

Agent Team implements reusable goal-oriented agent teams for AGenNext products.

The first team is:

```text
Ideation to Launch Team (Bootstrapped)
```

This team is designed for lean, no-investor-funded product building: validate problems, build the smallest useful product, launch quickly, generate revenue, and continuously learn.

## Source Blueprint

This implementation is based on:

```text
Agent-Blueprint: blueprints/team/ideation-to-launch-bootstrapped/0.1.0
```

## Core Rule

All agent-to-agent handoffs must use A2A only.

```text
If it is not passed through A2A, it is not an official handoff.
```

## LLM Provider Rule

The orchestrator may use only:

- local open-source LLMs
- open-source model runtimes
- free-tier LLM APIs

The orchestrator must prefer local/open-source options when possible and must evaluate license safety, trust, and cost before selecting a provider.
