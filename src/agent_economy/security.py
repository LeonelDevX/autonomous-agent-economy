from __future__ import annotations
import re
from pathlib import Path
from .db import Database
SECRET_PATTERNS = [re.compile(r"sk-[A-Za-z0-9_-]{6,}"), re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*=\s*[^\s]+"), re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*", re.DOTALL), re.compile(r"(?i)(seed phrase|mnemonic)\s*[:=]\s*.+")]
def redact_secrets(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted
def safe_join(root: Path, relative: str) -> Path:
    root_resolved = root.resolve(); target = (root_resolved / relative).resolve()
    if root_resolved not in target.parents and target != root_resolved: raise ValueError("path escapes configured workspace")
    return target
class KillSwitch:
    def __init__(self, db: Database): self.db = db
    def active(self) -> bool: return self.db.get_setting("kill_switch") == "active"
    def activate(self, reason: str) -> None: self.db.set_setting("kill_switch", "active"); self.db.audit("kill_switch_activated", {"reason": reason})
    def deactivate(self) -> None: self.db.set_setting("kill_switch", "inactive"); self.db.audit("kill_switch_deactivated", {})
