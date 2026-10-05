from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"
    APPROVAL_REQUIRED = "approval_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class TransactionRequest:
    agent_id: str
    amount: float
    currency: str
    category: str
    purpose: str
    destination_id: str
    real_money: bool = False

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    risk: RiskLevel
    approval_required: bool = False

@dataclass
class Task:
    id: int
    kind: str
    payload: dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    attempts: int = 0

@dataclass
class ProductIdea:
    title: str
    category: str
    demand: float
    competition: float
    effort: float
    cost: float
    revenue: float
    risk: float
    maintainability: float
    score: float = field(default=0.0)
