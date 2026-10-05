from __future__ import annotations
import json
from pathlib import Path
import typer
from .config import AppConfig, load_config
from .db import Database
from .security import KillSwitch
from .treasury import SimulationTreasury
app = typer.Typer(help="Controlled local AI-agent economy")
def ctx() -> tuple[AppConfig, Database]:
    cfg = load_config(); return cfg, Database(cfg.system.database)
@app.command()
def setup() -> None:
    cfg = AppConfig.default(Path.cwd()); cfg.system.workspace.mkdir(parents=True, exist_ok=True); Database(cfg.system.database)
    typer.echo("Setup complete in simulation mode."); typer.echo(f"Default Ollama model: {cfg.ollama.default_model}")
@app.command()
def status() -> None:
    cfg, db = ctx(); typer.echo(f"mode={cfg.system.mode}"); typer.echo(f"kill_switch={'active' if KillSwitch(db).active() else 'inactive'}")
@app.command()
def stop(all: bool = typer.Option(False, "--all")) -> None:
    _, db = ctx(); KillSwitch(db).activate("manual stop"); typer.echo("Kill switch activated.")
@app.command()
def treasury() -> None:
    cfg, db = ctx(); typer.echo(json.dumps(SimulationTreasury(db, cfg.treasury).status().__dict__, indent=2))
def main() -> None: app()
if __name__ == "__main__": main()
