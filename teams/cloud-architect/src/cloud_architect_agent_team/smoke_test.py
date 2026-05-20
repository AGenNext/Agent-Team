from .models import CloudRunState, PaymentState, HandoffState
from .orchestrator import CloudArchitectOrchestrator


state = CloudRunState(
    run_id="run-001",
    payment=PaymentState(
        payment_intent="pi_001",
        payer_proof=True,
        receiver_acknowledged=True,
    ),
    handoff=HandoffState(
        task="deploy governed k3s cluster",
        context={"tenant": "demo"},
        environment={"provider": "ovh"},
        knowledge={"runtime": "k8smicro"},
    ),
)

orchestrator = CloudArchitectOrchestrator()
result = orchestrator.run(state)

print(result.model_dump_json(indent=2))
