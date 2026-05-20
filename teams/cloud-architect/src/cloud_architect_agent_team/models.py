from typing import List, Optional
from pydantic import BaseModel


class PaymentState(BaseModel):
    payment_intent: str
    payer_proof: bool = False
    receiver_acknowledged: bool = False
    reconciled: bool = False


class HandoffState(BaseModel):
    task: str
    context: dict
    environment: dict
    knowledge: dict
    accepted: bool = False


class CloudRunState(BaseModel):
    run_id: str
    provider: str = "ovh"
    cluster_runtime: str = "k3s"
    governance_state: str = "normal"
    payment: PaymentState
    handoff: HandoffState
    deployment_approved: bool = False
    deployment_completed: bool = False
    health_ok: bool = False
    monitor_ok: bool = False
    traces: List[str] = []
