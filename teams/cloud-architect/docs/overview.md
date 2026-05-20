# Cloud Architect Agent Team

The Cloud Architect Agent Team is the first end-to-end governed autonomous infrastructure team for AGenNext.

## Goal

Provision and operate:

- OVH/Kimsufi bare metal
- k3s/k8smicro runtime
- SurrealDB memory layer
- WaltID identity layer
- governed multi-agent orchestration

through runtime-enforced governance.

## Governance stack

```txt
Agent-Constitution
  ↓
Agent-Platform
  ↓
Agent-Guard
Agent-Eval
Agent-Standard
Agent-Handoff
Agent-Security
Agent-Compliance
  ↓
Agent-Runtime
  ↓
Cloud Architect Agent Team
```

## Initial deployment target

```txt
Provider: OVH/Kimsufi
Runtime: k3s / k8smicro
Memory: SurrealDB
Identity: WaltID
```

## Runtime model

No agent can:

- self-approve
- bypass eval
- bypass guard
- deploy directly
- bypass platform authority
- handoff incomplete work

Everything is runtime enforced.
