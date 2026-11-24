"""Kho SQLite (mục 10). Mọi lần chạy Lean được ghi vào `lan_chay_lean` (I7)."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

_TEP_SCHEMA = Path(__file__).with_name("schema.sql")


def bay_gio() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Kho:
    def __init__(self, duong_dan: Path) -> None:
        self.duong_dan = Path(duong_dan)

    @contextmanager
    def ket_noi(self) -> Iterator[sqlite3.Connection]:
        self.duong_dan.parent.mkdir(parents=True, exist_ok=True)
        kn = sqlite3.connect(self.duong_dan)
        kn.execute("PRAGMA foreign_keys = ON")
        try:
            yield kn
            kn.commit()
        finally:
            kn.close()

    def tao_bang(self) -> None:
        with self.ket_noi() as kn:
            kn.executescript(_TEP_SCHEMA.read_text(encoding="utf-8"))

    def ghi_lan_chay_lean(
        self,
        che_do: str,
        muc_tieu: str,
        tep_hash: str,
        ket_qua: str,
        thong_bao: str,
        thoi_gian_ms: int,
        khuon_id: int | None = None,
        cau_id: int | None = None,
    ) -> int:
        with self.ket_noi() as kn:
            cur = kn.execute(
                "INSERT INTO lan_chay_lean (che_do, muc_tieu, tep_hash, ket_qua, thong_bao,"
                " thoi_gian_ms, khuon_id, cau_id, tao_luc) VALUES (?,?,?,?,?,?,?,?,?)",
                (che_do, muc_tieu, tep_hash, ket_qua, thong_bao, thoi_gian_ms,
                 khuon_id, cau_id, bay_gio()),
            )
            return int(cur.lastrowid)
