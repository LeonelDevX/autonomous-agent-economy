from pathlib import Path
import pytest
from agent_economy.config import AppConfig, ConfigError, load_config
from agent_economy.db import Database
from agent_economy.models import RiskLevel, TransactionRequest
from agent_economy.policy import PolicyEngine
from agent_economy.security import KillSwitch, redact_secrets, safe_join
from agent_economy.treasury import SimulationTreasury

def config(tmp_path: Path) -> AppConfig:
    return AppConfig.default(tmp_path)

def test_budget_blocks_agent_overrun(tmp_path: Path) -> None:
    db = Database(tmp_path / "app.db"); cfg = config(tmp_path)
    treasury = SimulationTreasury(db, cfg.treasury); policy = PolicyEngine(cfg, treasury)
    req = TransactionRequest("builder", cfg.treasury.max_agent_spend + 1, "SIM", "compute", "overspend", "simulation-provider")
    decision = policy.evaluate_transaction(req)
    assert not decision.allowed
    assert decision.risk == RiskLevel.HIGH

def test_real_payment_requires_approval(tmp_path: Path) -> None:
    db = Database(tmp_path / "app.db"); cfg = config(tmp_path)
    decision = PolicyEngine(cfg, SimulationTreasury(db, cfg.treasury)).evaluate_transaction(TransactionRequest("finance", 10, "EUR", "payment", "real", "provider", True))
    assert not decision.allowed
    assert decision.approval_required
    assert decision.risk == RiskLevel.CRITICAL

def test_secret_redaction() -> None:
    redacted = redact_secrets("OPENAI_API_KEY=sk-abc123 PRIVATE_KEY=-----BEGIN PRIVATE KEY-----abc")
    assert "sk-abc123" not in redacted
    assert "BEGIN PRIVATE KEY" not in redacted

def test_kill_switch(tmp_path: Path) -> None:
    db = Database(tmp_path / "app.db"); kill = KillSwitch(db); kill.activate("test")
    assert kill.active()

def test_real_mode_guard(tmp_path: Path) -> None:
    p = tmp_path / "config.yaml"; p.write_text("system:\n  mode: controlled_real\n", encoding="utf-8")
    with pytest.raises(ConfigError): load_config(p)

def test_safe_join_blocks_escape(tmp_path: Path) -> None:
    with pytest.raises(ValueError): safe_join(tmp_path, "../secret.txt")
