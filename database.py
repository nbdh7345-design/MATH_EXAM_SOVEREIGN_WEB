# -*- coding: utf-8 -*-
"""
database.py - Cơ sở dữ liệu SQLite (WAL Mode) cho Hệ thống Sinh Đề Toán Cao Cấp (@gng5)
Hỗ trợ truy cập đồng thời 20 Agent song song, lưu trữ câu hỏi Tự luận & Trắc nghiệm tham số,
bằng chứng kiểm chứng hình thức LEAN 4, script chạy số Python, đề thi và Sổ cái Merkle DAG.
"""

import hashlib
import json
import os
import sqlite3
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "math_exam_sovereign.db")
MERKLE_LEDGER_PATH = os.path.join(BASE_DIR, "gng5_merkle_ledger.json")

_db_lock = threading.RLock()


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=60.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def compute_question_merkle_hash(q_data: Dict[str, Any]) -> str:
    payload = {
        "code": q_data.get("code", ""),
        "subject": q_data.get("subject", ""),
        "topic": q_data.get("topic", ""),
        "question_type": q_data.get("question_type", ""),
        "stem_symbolic": q_data.get("stem_symbolic", ""),
        "options_symbolic": q_data.get("options_symbolic", {}),
        "correct_option": q_data.get("correct_option", ""),
        "lean4_code": q_data.get("lean4_code", ""),
        "python_code": q_data.get("python_code", ""),
        "lean4_status": q_data.get("lean4_status", ""),
        "python_status": q_data.get("python_status", ""),
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def init_db(db_path: str = DB_PATH) -> None:
    with _db_lock:
        conn = get_connection(db_path)
        try:
            cur = conn.cursor()
            cur.executescript(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    agent_id INTEGER NOT NULL,
                    agent_name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    question_type TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    has_parameters INTEGER NOT NULL DEFAULT 1,
                    parameters_schema TEXT NOT NULL DEFAULT '[]',
                    title TEXT NOT NULL,
                    stem_symbolic TEXT NOT NULL,
                    stem_template TEXT NOT NULL,
                    options_symbolic TEXT NOT NULL DEFAULT '{}',
                    parametric_formulas TEXT NOT NULL DEFAULT '{}',
                    correct_option TEXT NOT NULL,
                    solution_symbolic TEXT NOT NULL,
                    rubric_points TEXT NOT NULL DEFAULT '[]',
                    lean4_code TEXT NOT NULL,
                    lean4_status TEXT NOT NULL DEFAULT 'PENDING',
                    lean4_output TEXT NOT NULL DEFAULT '',
                    lean4_elapsed_ms REAL NOT NULL DEFAULT 0.0,
                    python_code TEXT NOT NULL,
                    python_status TEXT NOT NULL DEFAULT 'PENDING',
                    python_output TEXT NOT NULL DEFAULT '',
                    python_elapsed_ms REAL NOT NULL DEFAULT 0.0,
                    aas_score REAL NOT NULL DEFAULT 1.0,
                    sovereign_verdict TEXT NOT NULL DEFAULT 'SOVEREIGN_PASSED',
                    merkle_hash TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS exams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    subject_filter TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL DEFAULT 90,
                    parameter_mode TEXT NOT NULL DEFAULT 'mixed',
                    questions_snapshot TEXT NOT NULL,
                    total_questions INTEGER NOT NULL,
                    mcq_count INTEGER NOT NULL,
                    essay_count INTEGER NOT NULL,
                    parametric_count INTEGER NOT NULL,
                    merkle_root TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS exam_submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_id INTEGER NOT NULL,
                    student_name TEXT NOT NULL DEFAULT 'Sinh viên',
                    answers_json TEXT NOT NULL,
                    score REAL NOT NULL,
                    max_score REAL NOT NULL,
                    detail_json TEXT NOT NULL,
                    submitted_at TEXT NOT NULL,
                    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS agent_swarm_status (
                    agent_id INTEGER PRIMARY KEY,
                    agent_code TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    role_desc TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'IDLE',
                    questions_generated INTEGER NOT NULL DEFAULT 0,
                    lean4_verified INTEGER NOT NULL DEFAULT 0,
                    python_verified INTEGER NOT NULL DEFAULT 0,
                    last_task TEXT NOT NULL DEFAULT '',
                    elapsed_ms REAL NOT NULL DEFAULT 0.0,
                    merkle_node_hash TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS verification_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_code TEXT NOT NULL,
                    agent_id INTEGER NOT NULL,
                    verifier_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    execution_ms REAL NOT NULL,
                    output_log TEXT NOT NULL,
                    merkle_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            # Migration: phân biệt câu viết tay ('manual') và câu do LLM sinh ('llm')
            cols = {r["name"] for r in conn.execute("PRAGMA table_info(questions)").fetchall()}
            if "source" not in cols:
                conn.execute("ALTER TABLE questions ADD COLUMN source TEXT NOT NULL DEFAULT 'manual'")
            # Migration: kết quả formalize Lean 4 + Mathlib (tách riêng để swarm không ghi đè)
            for col, default in (
                ("lean4_mathlib_code", "''"),
                ("lean4_mathlib_status", "'NOT_RUN'"),
                ("lean4_mathlib_output", "''"),
                ("lean4_mathlib_review", "''"),
            ):
                if col not in cols:
                    conn.execute(f"ALTER TABLE questions ADD COLUMN {col} TEXT NOT NULL DEFAULT {default}")
            conn.commit()
        finally:
            conn.close()


def update_mathlib_result(code: str, lean_code: str, status: str, output: str, review: str,
                          db_path: str = DB_PATH) -> None:
    with _db_lock:
        conn = get_connection(db_path)
        try:
            conn.execute(
                """
                UPDATE questions SET lean4_mathlib_code = ?, lean4_mathlib_status = ?,
                    lean4_mathlib_output = ?, lean4_mathlib_review = ?, updated_at = ?
                WHERE code = ?
                """,
                (lean_code, status, output[:8000], review, datetime.now().isoformat(timespec="seconds"), code),
            )
            conn.commit()
        finally:
            conn.close()


def delete_question(code: str, db_path: str = DB_PATH) -> bool:
    with _db_lock:
        conn = get_connection(db_path)
        try:
            cur = conn.execute("DELETE FROM questions WHERE code = ?", (code,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()


def upsert_question(q: Dict[str, Any], db_path: str = DB_PATH) -> int:
    now = datetime.now().isoformat(timespec="seconds")
    options_sym = q.get("options_symbolic", {})
    if not isinstance(options_sym, str):
        options_sym = json.dumps(options_sym, ensure_ascii=False)

    param_schema = q.get("parameters_schema", [])
    if not isinstance(param_schema, str):
        param_schema = json.dumps(param_schema, ensure_ascii=False)

    param_formulas = q.get("parametric_formulas", {})
    if not isinstance(param_formulas, str):
        param_formulas = json.dumps(param_formulas, ensure_ascii=False)

    rubric = q.get("rubric_points", [])
    if not isinstance(rubric, str):
        rubric = json.dumps(rubric, ensure_ascii=False)

    merkle_hash = q.get("merkle_hash") or compute_question_merkle_hash(q)

    with _db_lock:
        conn = get_connection(db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO questions (
                    code, agent_id, agent_name, subject, topic, question_type,
                    difficulty, has_parameters, parameters_schema, title,
                    stem_symbolic, stem_template, options_symbolic, parametric_formulas,
                    correct_option, solution_symbolic, rubric_points,
                    lean4_code, lean4_status, lean4_output, lean4_elapsed_ms,
                    python_code, python_status, python_output, python_elapsed_ms,
                    aas_score, sovereign_verdict, merkle_hash, created_at, updated_at, source
                ) VALUES (
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT(code) DO UPDATE SET
                    agent_id=excluded.agent_id,
                    agent_name=excluded.agent_name,
                    subject=excluded.subject,
                    topic=excluded.topic,
                    question_type=excluded.question_type,
                    difficulty=excluded.difficulty,
                    has_parameters=excluded.has_parameters,
                    parameters_schema=excluded.parameters_schema,
                    title=excluded.title,
                    stem_symbolic=excluded.stem_symbolic,
                    stem_template=excluded.stem_template,
                    options_symbolic=excluded.options_symbolic,
                    parametric_formulas=excluded.parametric_formulas,
                    correct_option=excluded.correct_option,
                    solution_symbolic=excluded.solution_symbolic,
                    rubric_points=excluded.rubric_points,
                    lean4_code=excluded.lean4_code,
                    lean4_status=excluded.lean4_status,
                    lean4_output=excluded.lean4_output,
                    lean4_elapsed_ms=excluded.lean4_elapsed_ms,
                    python_code=excluded.python_code,
                    python_status=excluded.python_status,
                    python_output=excluded.python_output,
                    python_elapsed_ms=excluded.python_elapsed_ms,
                    aas_score=excluded.aas_score,
                    sovereign_verdict=excluded.sovereign_verdict,
                    merkle_hash=excluded.merkle_hash,
                    updated_at=excluded.updated_at,
                    source=excluded.source
                """,
                (
                    q["code"],
                    int(q.get("agent_id", 1)),
                    q.get("agent_name", "Agent-01"),
                    q["subject"],
                    q["topic"],
                    q["question_type"],
                    q.get("difficulty", "Vận dụng"),
                    1 if q.get("has_parameters", True) else 0,
                    param_schema,
                    q["title"],
                    q["stem_symbolic"],
                    q.get("stem_template", q["stem_symbolic"]),
                    options_sym,
                    param_formulas,
                    q.get("correct_option", "A"),
                    q["solution_symbolic"],
                    rubric,
                    q["lean4_code"],
                    q.get("lean4_status", "PENDING"),
                    q.get("lean4_output", ""),
                    float(q.get("lean4_elapsed_ms", 0.0)),
                    q["python_code"],
                    q.get("python_status", "PENDING"),
                    q.get("python_output", ""),
                    float(q.get("python_elapsed_ms", 0.0)),
                    float(q.get("aas_score", 1.0)),
                    q.get("sovereign_verdict", "SOVEREIGN_PASSED"),
                    merkle_hash,
                    now,
                    now,
                    q.get("source", "manual"),
                ),
            )
            conn.commit()
            cur.execute("SELECT id FROM questions WHERE code = ?", (q["code"],))
            row = cur.fetchone()
            return row["id"] if row else 0
        finally:
            conn.close()


def update_agent_status(
    agent_id: int,
    agent_code: str,
    agent_name: str,
    domain: str,
    role_desc: str,
    status: str,
    questions_generated: int = 0,
    lean4_verified: int = 0,
    python_verified: int = 0,
    last_task: str = "",
    elapsed_ms: float = 0.0,
    merkle_node_hash: str = "",
    db_path: str = DB_PATH,
) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    with _db_lock:
        conn = get_connection(db_path)
        try:
            conn.execute(
                """
                INSERT INTO agent_swarm_status (
                    agent_id, agent_code, agent_name, domain, role_desc,
                    status, questions_generated, lean4_verified, python_verified,
                    last_task, elapsed_ms, merkle_node_hash, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(agent_id) DO UPDATE SET
                    agent_code=excluded.agent_code,
                    agent_name=excluded.agent_name,
                    domain=excluded.domain,
                    role_desc=excluded.role_desc,
                    status=excluded.status,
                    questions_generated=excluded.questions_generated,
                    lean4_verified=excluded.lean4_verified,
                    python_verified=excluded.python_verified,
                    last_task=excluded.last_task,
                    elapsed_ms=excluded.elapsed_ms,
                    merkle_node_hash=excluded.merkle_node_hash,
                    updated_at=excluded.updated_at
                """,
                (
                    agent_id,
                    agent_code,
                    agent_name,
                    domain,
                    role_desc,
                    status,
                    questions_generated,
                    lean4_verified,
                    python_verified,
                    last_task,
                    elapsed_ms,
                    merkle_node_hash,
                    now,
                ),
            )
            conn.commit()
        finally:
            conn.close()


def log_verification(
    question_code: str,
    agent_id: int,
    verifier_type: str,
    status: str,
    execution_ms: float,
    output_log: str,
    merkle_hash: str,
    db_path: str = DB_PATH,
) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    with _db_lock:
        conn = get_connection(db_path)
        try:
            conn.execute(
                """
                INSERT INTO verification_logs (
                    question_code, agent_id, verifier_type, status,
                    execution_ms, output_log, merkle_hash, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    question_code,
                    agent_id,
                    verifier_type,
                    status,
                    execution_ms,
                    output_log[:4000],
                    merkle_hash,
                    now,
                ),
            )
            conn.commit()
        finally:
            conn.close()


def row_to_question_dict(row: sqlite3.Row) -> Dict[str, Any]:
    d = dict(row)
    for k in ("parameters_schema", "options_symbolic", "parametric_formulas", "rubric_points"):
        if k in d and isinstance(d[k], str):
            try:
                d[k] = json.loads(d[k])
            except Exception:
                pass
    if isinstance(d.get("parameters_schema"), dict):
        norm_list = []
        for k, v in d["parameters_schema"].items():
            if isinstance(v, dict):
                item = dict(v)
                item.setdefault("name", k)
                item.setdefault("symbol", k)
                norm_list.append(item)
        d["parameters_schema"] = norm_list
    d["has_parameters"] = bool(d.get("has_parameters", 0))
    return d


def list_questions(
    subject: Optional[str] = None,
    question_type: Optional[str] = None,
    has_parameters: Optional[bool] = None,
    agent_id: Optional[int] = None,
    search: Optional[str] = None,
    db_path: str = DB_PATH,
    agent_ids: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        clauses = ["1=1"]
        params: List[Any] = []
        if agent_ids is not None:
            clauses.append(f"agent_id IN ({','.join('?' * len(agent_ids)) or 'NULL'})")
            params.extend(int(a) for a in agent_ids)
        if subject and subject != "ALL":
            clauses.append("subject = ?")
            params.append(subject)
        if question_type and question_type != "ALL":
            clauses.append("question_type = ?")
            params.append(question_type)
        if has_parameters is not None:
            clauses.append("has_parameters = ?")
            params.append(1 if has_parameters else 0)
        if agent_id is not None:
            clauses.append("agent_id = ?")
            params.append(int(agent_id))
        if search:
            clauses.append("(title LIKE ? OR stem_symbolic LIKE ? OR topic LIKE ? OR code LIKE ?)")
            s = f"%{search}%"
            params.extend([s, s, s, s])

        sql = f"SELECT * FROM questions WHERE {' AND '.join(clauses)} ORDER BY agent_id ASC, id ASC"
        cur = conn.execute(sql, params)
        return [row_to_question_dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def get_question_by_id_or_code(identifier: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        if str(identifier).isdigit():
            cur = conn.execute("SELECT * FROM questions WHERE id = ?", (int(identifier),))
        else:
            cur = conn.execute("SELECT * FROM questions WHERE code = ?", (str(identifier),))
        row = cur.fetchone()
        return row_to_question_dict(row) if row else None
    finally:
        conn.close()


def get_dashboard_stats(db_path: str = DB_PATH, agent_ids: Optional[List[int]] = None) -> Dict[str, Any]:
    """Thống kê ngân hàng; agent_ids (nếu có) giới hạn theo các agent đang hoạt động."""
    conn = get_connection(db_path)
    try:
        scope, scope_params = "1=1", []
        if agent_ids is not None:
            scope = f"agent_id IN ({','.join('?' * len(agent_ids)) or 'NULL'})"
            scope_params = [int(a) for a in agent_ids]

        def count(cond: str = "1=1") -> int:
            return conn.execute(f"SELECT COUNT(*) FROM questions WHERE {scope} AND {cond}", scope_params).fetchone()[0]

        total = count()
        calc_cnt = count("subject = 'Giải tích'")
        alg_cnt = count("subject = 'Đại số'")
        mcq_cnt = count("question_type = 'mcq'")
        essay_cnt = count("question_type = 'essay'")
        param_cnt = count("has_parameters = 1")
        lean_pass = count("lean4_status = 'VERIFIED_PASS'")
        py_pass = count("python_status = 'VERIFIED_PASS'")
        exams_cnt = conn.execute("SELECT COUNT(*) FROM exams").fetchone()[0]
        llm_cnt = count("source = 'llm'")
        mathlib_cnt = count("lean4_mathlib_status = 'VERIFIED_PASS'")
        agents = [dict(r) for r in conn.execute(
            f"SELECT * FROM agent_swarm_status WHERE {scope} ORDER BY agent_id ASC", scope_params).fetchall()]
        recent_logs = [dict(r) for r in conn.execute("SELECT * FROM verification_logs ORDER BY id DESC LIMIT 30").fetchall()]

        merkle_root = "0" * 64
        if os.path.exists(MERKLE_LEDGER_PATH):
            try:
                with open(MERKLE_LEDGER_PATH, "r", encoding="utf-8") as f:
                    mdata = json.load(f)
                    merkle_root = mdata.get("merkle_root", merkle_root)
            except Exception:
                pass

        return {
            "total_questions": total,
            "calculus_count": calc_cnt,
            "algebra_count": alg_cnt,
            "mcq_count": mcq_cnt,
            "essay_count": essay_cnt,
            "parametric_count": param_cnt,
            "lean4_verified_count": lean_pass,
            "python_verified_count": py_pass,
            "exams_count": exams_cnt,
            "llm_count": llm_cnt,
            "mathlib_verified_count": mathlib_cnt,
            "merkle_root": merkle_root,
            "agents": agents,
            "recent_logs": recent_logs,
        }
    finally:
        conn.close()
