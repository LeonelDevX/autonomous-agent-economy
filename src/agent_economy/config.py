from __future__ import annotations

from pathlib import Path
from typing import Any, Literal
import yaml
from pydantic import BaseModel, Field, ValidationError

class ConfigError(RuntimeError):
    pass

class SystemConfig(BaseModel):
    mode: Literal["simulation", "controlled_real"] = "simulation"
    require_real_mode_confirmation: bool = True
    workspace: Path = Path("runtime/workspace")
    database: Path = Path("runtime/agent_economy.db")

class OllamaConfig(BaseModel):
    host: str = "http://127.0.0.1:11434"
    profile: Literal["small", "balanced", "powerful"] = "balanced"
    small_model: str = "llama3.2:3b"
    balanced_model: str = "qwen2.5:7b"
    powerful_model: str = "llama3.1:8b"
    request_timeout: float = 60.0

    @property
    def default_model(self) -> str:
        return {"small": self.small_model, "balanced": self.balanced_model, "powerful": self.powerful_model}[self.profile]

class InternetConfig(BaseModel):
    enabled: bool = False
    allowlist: list[str] = Field(default_factory=lambda: ["example.com", "docs.python.org"])
    denylist: list[str] = Field(default_factory=list)
    timeout_seconds: float = 10.0
    requests_per_minute: int = 20

class TreasuryConfig(BaseModel):
    starting_balance: float = 1000.0
    reserve_percent: float = 0.5
    compute_percent: float = 0.3
    growth_percent: float = 0.2
    daily_spending_limit: float = 100.0
    transaction_limit: float = 25.0
    max_agent_spend: float = 50.0
    minimum_reserve: float = 250.0
    approval_threshold: float = 20.0

class AgentConfig(BaseModel):
    max_agents: int = 12
    max_agent_depth: int = 2
    max_agent_budget: float = 50.0
    global_budget: float = 500.0
    allowed_agent_types: list[str] = Field(default_factory=lambda: ["master", "research", "idea_evaluation", "builder", "qa", "marketing", "sales", "finance", "security", "analytics", "support", "model_evaluation"])

class ApprovalConfig(BaseModel):
    low_auto: bool = True
    medium_auto_under_policy: bool = True
    high_requires_manual: bool = True
    critical_requires_manual: bool = True

class SecurityConfig(BaseModel):
    secret_patterns: list[str] = Field(default_factory=list)
    dashboard_host: str = "127.0.0.1"
    dashboard_port: int = 8765

class AppConfig(BaseModel):
    system: SystemConfig = Field(default_factory=SystemConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    internet: InternetConfig = Field(default_factory=InternetConfig)
    treasury: TreasuryConfig = Field(default_factory=TreasuryConfig)
    agents: AgentConfig = Field(default_factory=AgentConfig)
    approvals: ApprovalConfig = Field(default_factory=ApprovalConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    @staticmethod
    def default(root: Path | None = None) -> 'AppConfig':
        cfg = AppConfig()
        if root:
            cfg.system.workspace = root / "runtime" / "workspace"
            cfg.system.database = root / "runtime" / "agent_economy.db"
        return cfg

def load_config(path: Path | str = "config.yaml") -> AppConfig:
    config_path = Path(path)
    data: dict[str, Any] = {}
    if config_path.exists():
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    try:
        cfg = AppConfig.model_validate(data)
    except ValidationError as exc:
        raise ConfigError(str(exc)) from exc
    if cfg.system.mode == "controlled_real" and cfg.system.require_real_mode_confirmation:
        raise ConfigError("controlled_real mode requires explicit confirmation in config")
    return cfg
