# Cloud Architect Agent Team

The Cloud Architect Agent can live as an AGenNext agent team in `Agent-Team`.

## Decision

Use `AGenNext/Agent-Team` to define composed multi-agent products such as the Cloud Architect Agent.

Provider-specific implementation packages may live elsewhere, but the full agent team composition belongs here.

## Team role

The Cloud Architect Agent Team coordinates planning, evaluation, security, deployment, lifecycle, compliance, analytics, and operations for cloud and bare-metal infrastructure.

## Team members

```txt
Cloud Architect Agent Team
  ├── Blueprint planner
  ├── Eval gate
  ├── Security gate
  ├── Compliance mapper
  ├── IGA/access governor
  ├── Lifecycle manager
  ├── Deploy coordinator
  ├── Runtime executor
  ├── Kubernetes operator
  ├── Trace recorder
  ├── Runs debugger
  ├── Analytics reporter
  └── FinOps advisor
```

## Repository relationships

| Capability | Repository |
|---|---|
| Team composition | `AGenNext/Agent-Team` |
| Blueprint | `AGenNext/Agent-Blueprint` |
| Runtime | `AGenNext/Agent-Runtime` |
| Framework adapters | `AGenNext/Agent-Frameworks` |
| Kubernetes operations | `AGenNext/AgentKube` |
| Deployment and CI/CD | `AGenNext/Agent-deploy` |
| Security gate | `AGenNext/Agent-Security` |
| Evaluation gate | `AGenNext/Agent-Eval` |
| Compliance | `AGenNext/Agent-Compliance` |
| Lifecycle | `AGenNext/Agent-LCM` |
| Identity governance | `AGenNext/Agent-IGA` |
| Traces | `AGenNext/Agent-Traces` |
| Runs/debugging | `AGenNext/Agent-Runs` |
| Analytics | `AGenNext/Agent-Analytics` |
| FinOps | `AGenNext/Agent-FinOps` |
| Provider implementation | `Agent-Cloud` or provider-specific repo |

## Cloud agent flow

```txt
User intent
  ↓
Cloud Architect Agent Team
  ↓
Blueprint plan
  ↓
Eval gate
  ↓
Security gate
  ↓
IGA/approval checks
  ↓
Deploy + Runtime execution
  ↓
Traces + Runs + Analytics
  ↓
Lifecycle + Compliance updates
```

## First target

```txt
OVH/Kimsufi Eco bare metal
  ↓
k3s
  ↓
k8smicro runtime profile
  ↓
SurrealDB + AgentKube + AgentGraph/LangGraph
```

## Rule

Agent-Team defines the composed agent product.

Individual capability repos implement specialized layers.
