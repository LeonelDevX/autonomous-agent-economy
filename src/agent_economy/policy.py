from __future__ import annotations
from .config import AppConfig
from .models import PolicyDecision, RiskLevel, TransactionRequest
from .treasury import SimulationTreasury
class PolicyEngine:
    def __init__(self, cfg: AppConfig, treasury: SimulationTreasury): self.cfg = cfg; self.treasury = treasury
    def evaluate_transaction(self, request: TransactionRequest) -> PolicyDecision:
        if request.real_money: return PolicyDecision(False, "real-money transactions are critical and require approval", RiskLevel.CRITICAL, True)
        if request.amount > self.cfg.treasury.max_agent_spend: return PolicyDecision(False, "agent spending limit exceeded", RiskLevel.HIGH, True)
        if request.amount > self.cfg.treasury.transaction_limit: return PolicyDecision(False, "transaction limit exceeded", RiskLevel.HIGH, True)
        if self.treasury.balance() - request.amount < self.cfg.treasury.minimum_reserve: return PolicyDecision(False, "minimum reserve would be violated", RiskLevel.HIGH, True)
        if request.amount >= self.cfg.treasury.approval_threshold: return PolicyDecision(False, "approval threshold reached", RiskLevel.MEDIUM, True)
        return PolicyDecision(True, "allowed by simulation policy", RiskLevel.LOW)
    def require_approval_for_publication(self, target: str) -> PolicyDecision:
        return PolicyDecision(False, f"publication to {target} requires human approval", RiskLevel.HIGH, True)
