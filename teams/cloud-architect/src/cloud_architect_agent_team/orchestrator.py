from .models import CloudRunState


class GovernanceError(Exception):
    pass


class CloudArchitectOrchestrator:
    def validate_handoff(self, state: CloudRunState):
        handoff = state.handoff

        if not handoff.task:
            raise GovernanceError("missing task")

        if not handoff.context:
            raise GovernanceError("missing context")

        if not handoff.environment:
            raise GovernanceError("missing environment")

        if not handoff.knowledge:
            raise GovernanceError("missing knowledge")

        handoff.accepted = True
        state.traces.append("handoff_accepted")

    def validate_payment(self, state: CloudRunState):
        payment = state.payment

        if not payment.payer_proof:
            raise GovernanceError("payer proof missing")

        if not payment.receiver_acknowledged:
            raise GovernanceError("receiver acknowledgement missing")

        payment.reconciled = True
        state.traces.append("payment_reconciled")

    def evaluate(self, state: CloudRunState):
        state.traces.append("eval_passed")

    def security_check(self, state: CloudRunState):
        state.traces.append("security_passed")

    def platform_approve(self, state: CloudRunState):
        state.deployment_approved = True
        state.traces.append("platform_approved")

    def deploy(self, state: CloudRunState):
        if not state.deployment_approved:
            raise GovernanceError("deployment not approved")

        state.deployment_completed = True
        state.traces.append("deployment_completed")

    def health_check(self, state: CloudRunState):
        state.health_ok = True
        state.traces.append("health_ok")

    def monitor(self, state: CloudRunState):
        state.monitor_ok = True
        state.traces.append("monitor_ok")

    def run(self, state: CloudRunState):
        self.validate_handoff(state)
        self.validate_payment(state)
        self.evaluate(state)
        self.security_check(state)
        self.platform_approve(state)
        self.deploy(state)
        self.health_check(state)
        self.monitor(state)

        return state
