from __future__ import annotations
from dataclasses import dataclass
from .config import TreasuryConfig
from .db import Database
from .models import TransactionRequest
@dataclass(frozen=True)
class TreasuryStatus:
    balance: float; reserve: float; compute_budget: float; growth_budget: float; revenue: float; expenses: float; profit: float
class SimulationTreasury:
    def __init__(self, db: Database, cfg: TreasuryConfig):
        self.db = db; self.cfg = cfg
        if self.db.get_setting("treasury_balance") is None:
            self.db.set_setting("treasury_balance", str(cfg.starting_balance)); self.db.set_setting("treasury_revenue", "0"); self.db.set_setting("treasury_expenses", "0")
    def balance(self) -> float: return float(self.db.get_setting("treasury_balance") or self.cfg.starting_balance)
    def status(self) -> TreasuryStatus:
        b = self.balance(); r = float(self.db.get_setting("treasury_revenue") or 0); e = float(self.db.get_setting("treasury_expenses") or 0)
        return TreasuryStatus(b, b*self.cfg.reserve_percent, b*self.cfg.compute_percent, b*self.cfg.growth_percent, r, e, r-e)
    def record_revenue(self, amount: float, source: str) -> None:
        self.db.set_setting("treasury_balance", str(self.balance()+amount)); self.db.audit("revenue_recorded", {"amount": amount, "source": source, "simulation": True})
    def execute(self, request: TransactionRequest) -> None:
        self.db.set_setting("treasury_balance", str(self.balance()-request.amount)); self.db.audit("transaction_executed", request.__dict__)
