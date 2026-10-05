from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

class Database:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        return con

    def _init(self) -> None:
        with self.connect() as con:
            con.executescript("""
            create table if not exists settings(key text primary key, value text not null);
            create table if not exists audit(id integer primary key autoincrement, event text not null, data text not null, created_at text default current_timestamp);
            create table if not exists transactions(id integer primary key autoincrement, agent_id text, amount real not null, currency text not null, category text not null, purpose text not null, destination_id text not null, real_money integer not null, created_at text default current_timestamp);
            create table if not exists approvals(id integer primary key autoincrement, action text not null, risk text not null, payload text not null, status text not null, reviewer text, created_at text default current_timestamp);
            create table if not exists agents(id text primary key, role text not null, budget real not null, depth integer not null default 0, created_at text default current_timestamp);
            create table if not exists tasks(id integer primary key autoincrement, kind text not null, payload text not null, status text not null, attempts integer not null default 0, created_at text default current_timestamp, updated_at text default current_timestamp);
            create table if not exists products(id integer primary key autoincrement, title text not null, status text not null, data text not null, created_at text default current_timestamp);
            """)

    def audit(self, event: str, data: dict[str, Any]) -> None:
        with self.connect() as con:
            con.execute("insert into audit(event, data) values(?, ?)", (event, json.dumps(data)))

    def get_setting(self, key: str) -> str | None:
        with self.connect() as con:
            row = con.execute("select value from settings where key=?", (key,)).fetchone()
        return None if row is None else str(row["value"])

    def set_setting(self, key: str, value: str) -> None:
        with self.connect() as con:
            con.execute("insert into settings(key, value) values(?, ?) on conflict(key) do update set value=excluded.value", (key, value))
