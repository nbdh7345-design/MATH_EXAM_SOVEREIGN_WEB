# -*- coding: utf-8 -*-
"""
app.py - Hệ Thống Web Sinh Đề Toán Cao Cấp (Giải Tích & Đại Số) Tự Luận & Trắc Nghiệm Tham Số
Kiểm chứng kép bằng LEAN 4 (v4.35.0) & Script Python Chạy Số, Điều phối 20 Agent Song Song (@gng5)
"""

import concurrent.futures
import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database import (
    DB_PATH,
    MERKLE_LEDGER_PATH,
    get_connection,
    get_dashboard_stats,
    get_question_by_id_or_code,
    init_db,
    list_questions,
    log_verification,
    upsert_question,
)
from database import delete_question
from lean_formalizer import formalize_question, lean_status, recheck_question
from llm_generator import generate_questions, llm_status
from parametric_engine import evaluate_question_with_params, sample_valid_parameters
from swarm_orchestrator import ACTIVE_AGENT_IDS, AGENTS_REGISTRY, run_all_20_agents_parallel
from verifier_engine import (
    commit_merkle_node,
    verify_lean4_code,
    verify_python_code,
    verify_question_full,
)

app = FastAPI(
    title="@gng5 Sovereign Higher Mathematics Exam System (20-Agent Swarm + Lean 4 + Python)",
    description="Hệ thống sinh đề Toán Cao Cấp (Giải tích, Đại số) tự luận và trắc nghiệm chứa tham số, kiểm chứng bằng LEAN 4 và Python chạy số với 20 Agent song song.",
    version="5.0.0",
)

# Chỉ cho phép chính giao diện của hệ thống gọi API (trước đây "*" cho phép mọi trang web
# gọi các endpoint chạy code và endpoint sinh câu hỏi tốn phí LLM).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8088", "http://localhost:8088"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class EvaluateParamsRequest(BaseModel):
    parameters: Dict[str, float] = Field(default_factory=dict)
    mode: str = Field(default="dual", description="symbolic | numeric | dual")


class VerifyQuestionRequest(BaseModel):
    lean4_code: Optional[str] = None
    python_code: Optional[str] = None


class SandboxVerifyRequest(BaseModel):
    code_id: str = "SANDBOX-01"
    lean4_code: str
    python_code: str


class GenerateExamRequest(BaseModel):
    title: str = "Đề Thi Kết Thúc Học Phần Toán Cao Cấp (Giải Tích & Đại Số)"
    subject_filter: str = "ALL"  # "ALL" | "Giải tích" | "Đại số"
    mcq_count: int = 12
    essay_count: int = 4
    # "numeric": thay tham số vào đề, phương án/đáp số là số (mặc định cho đề thi) | "symbolic" | "dual" (chỉ để đối chiếu:
    # hiện cả công thức theo tham số và giá trị, kèm đáp án đúng trong đề)
    parameter_mode: str = "numeric"
    randomize_parameters: bool = True
    duration_minutes: int = 90
    seed: Optional[int] = None
    # Mức tin cậy tối thiểu của câu được chọn: "all" | "exclude_failed" (bỏ câu formalize thất bại)
    # | "formal_only" (chỉ câu đã formalize Lean + Mathlib thành công)
    trust_level: str = Field(default="all", pattern="^(all|exclude_failed|formal_only)$")


class LLMGenerateRequest(BaseModel):
    agent_ids: List[int] = Field(default_factory=list, description="Rỗng = tất cả agent")
    count_per_agent: int = Field(default=1, ge=1, le=5)
    question_type: str = Field(default="mixed", pattern="^(mixed|mcq|essay)$")
    difficulty: str = Field(default="Vận dụng", pattern="^(Nhận biết|Thông hiểu|Vận dụng|Vận dụng cao)$")
    max_attempts: int = Field(default=2, ge=1, le=3)
    formalize_lean: bool = True


class FormalizeRequest(BaseModel):
    max_attempts: Optional[int] = Field(default=None, ge=1, le=8)
    # Các bước cải thiện formalize được bật (1: chuẩn hóa đề, 2: truy xuất, 3: suy luận trước khi dịch,
    # 4: nhiều ứng viên + đồng thuận). None = theo MATH_FORMALIZE_STEPS; [] = quy trình gốc.
    steps: Optional[List[int]] = None
    num_candidates: Optional[int] = Field(default=None, ge=1, le=6)


class SubmitExamRequest(BaseModel):
    student_name: str = "Sinh viên ĐHBK"
    mcq_answers: Dict[str, str] = Field(default_factory=dict)
    essay_self_scores: Dict[str, float] = Field(default_factory=dict)


@app.on_event("startup")
def on_startup():
    init_db(DB_PATH)
    # Mặc định không nạp trước Mathlib (tốn vài GB RAM trong ~1 phút đầu): lượt formalize đầu tiên tự nạp.
    # Đặt MATH_LEAN_WARMUP=1 để nạp trước ở luồng nền như cũ.
    if os.environ.get("MATH_LEAN_WARMUP", "0") == "1":
        import threading
        from lean_formalizer import warmup_mathlib
        threading.Thread(target=warmup_mathlib, daemon=True).start()
    stats = get_dashboard_stats(DB_PATH)
    # Khởi tạo trạng thái ban đầu cho các Agent chưa có trong CSDL (CSDL mới, hoặc Agent mới được bổ sung)
    known_ids = {ag["agent_id"] for ag in stats.get("agents", [])} if stats["total_questions"] else set()
    from database import update_agent_status
    for ag in AGENTS_REGISTRY:
        if ag["agent_id"] not in known_ids:
            update_agent_status(
                agent_id=ag["agent_id"],
                agent_code=ag["agent_code"],
                agent_name=ag["agent_name"],
                domain=ag["domain"],
                role_desc=ag["role_desc"],
                status="READY",
                last_task="Sẵn sàng kích hoạt kiểm chứng song song",
                db_path=DB_PATH,
            )


@app.get("/", response_class=HTMLResponse)
def read_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Đang khởi tạo giao diện...</h1>")


@app.get("/api/dashboard")
def api_dashboard():
    return get_dashboard_stats(DB_PATH, agent_ids=ACTIVE_AGENT_IDS)


@app.get("/api/questions")
def api_list_questions(
    subject: Optional[str] = Query(default=None),
    question_type: Optional[str] = Query(default=None),
    has_parameters: Optional[bool] = Query(default=None),
    agent_id: Optional[int] = Query(default=None),
    search: Optional[str] = Query(default=None),
    mode: str = Query(default="dual"),
):
    qs = list_questions(
        subject=subject,
        question_type=question_type,
        has_parameters=has_parameters,
        agent_id=agent_id,
        search=search,
        db_path=DB_PATH,
        agent_ids=ACTIVE_AGENT_IDS,
    )
    enriched = []
    for q in qs:
        eval_res = evaluate_question_with_params(q, custom_params=None, mode=mode)
        q["evaluated_preview"] = eval_res
        enriched.append(q)
    return {"total": len(enriched), "questions": enriched}


@app.get("/api/questions/{identifier}")
def api_get_question(identifier: str, mode: str = Query(default="dual")):
    q = get_question_by_id_or_code(identifier, db_path=DB_PATH)
    if not q:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy câu hỏi: {identifier}")
    q["evaluated_preview"] = evaluate_question_with_params(q, custom_params=None, mode=mode)
    return q


@app.post("/api/questions/{identifier}/evaluate")
def api_evaluate_question(identifier: str, req: EvaluateParamsRequest):
    q = get_question_by_id_or_code(identifier, db_path=DB_PATH)
    if not q:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy câu hỏi: {identifier}")
    res = evaluate_question_with_params(q, custom_params=req.parameters, mode=req.mode)
    return res


@app.post("/api/questions/{identifier}/randomize")
def api_randomize_question_params(identifier: str, mode: str = Query(default="dual")):
    q = get_question_by_id_or_code(identifier, db_path=DB_PATH)
    if not q:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy câu hỏi: {identifier}")
    sampled = sample_valid_parameters(q)
    res = evaluate_question_with_params(q, custom_params=sampled, mode=mode)
    return res


@app.post("/api/questions/{identifier}/verify")
def api_verify_single_question(identifier: str, req: VerifyQuestionRequest):
    q = get_question_by_id_or_code(identifier, db_path=DB_PATH)
    if not q:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy câu hỏi: {identifier}")
    if req.lean4_code is not None and req.lean4_code.strip():
        q["lean4_code"] = req.lean4_code
    if req.python_code is not None and req.python_code.strip():
        q["python_code"] = req.python_code

    res = verify_question_full(q)
    upsert_question(res["question"], db_path=DB_PATH)
    log_verification(
        question_code=q["code"],
        agent_id=int(q.get("agent_id", 1)),
        verifier_type="MANUAL_DUAL_VERIFY",
        status=res["sovereign_verdict"],
        execution_ms=round(res["lean4"]["elapsed_ms"] + res["python"]["elapsed_ms"], 2),
        output_log=f"LEAN4: {res['lean4']['output']}\nPYTHON: {res['python']['output']}",
        merkle_hash=res["merkle_hash"],
        db_path=DB_PATH,
    )
    commit_merkle_node(
        node_type="SINGLE_QUESTION_REVERIFY",
        parent_hashes=[res["merkle_hash"]],
        payload={
            "code": q["code"],
            "lean4_status": res["lean4"]["status"],
            "python_status": res["python"]["status"],
            "aas_score": res["aas_score"],
            "verdict": res["sovereign_verdict"],
        },
    )
    return res


@app.post("/api/sandbox/verify")
def api_sandbox_verify(req: SandboxVerifyRequest):
    lean_res = verify_lean4_code(req.code_id, req.lean4_code)
    py_res = verify_python_code(req.code_id, req.python_code)
    both_ok = lean_res["status"] == "VERIFIED_PASS" and py_res["status"] == "VERIFIED_PASS"
    m_node = commit_merkle_node(
        node_type="SANDBOX_DUAL_VERIFICATION",
        parent_hashes=[],
        payload={
            "code_id": req.code_id,
            "lean4_status": lean_res["status"],
            "python_status": py_res["status"],
            "verdict": "SOVEREIGN_PASSED" if both_ok else "REJECTED_NEEDS_REPAIR",
        },
    )
    return {
        "code_id": req.code_id,
        "lean4": lean_res,
        "python": py_res,
        "sovereign_verdict": "SOVEREIGN_PASSED" if both_ok else "REJECTED_NEEDS_REPAIR",
        "merkle_hash": m_node["node"]["hash"],
        "merkle_root": m_node["merkle_root"],
    }


@app.post("/api/swarm/run")
def api_run_swarm():
    summary = run_all_20_agents_parallel(db_path=DB_PATH)
    return summary


@app.get("/api/llm/status")
def api_llm_status():
    return llm_status()


@app.post("/api/llm/generate")
def api_llm_generate(req: LLMGenerateRequest):
    st = llm_status()
    if not st["configured"]:
        raise HTTPException(
            status_code=400,
            detail=f"Chưa cấu hình LLM ({st['provider']}). {st['hint']} Sau đó khởi động lại server.",
        )
    return generate_questions(
        agent_ids=req.agent_ids or None,
        count_per_agent=req.count_per_agent,
        question_type=req.question_type,
        difficulty=req.difficulty,
        max_attempts=req.max_attempts,
        db_path=DB_PATH,
        formalize_lean=req.formalize_lean and lean_status()["mathlib_ready"],
    )


@app.get("/api/lean/status")
def api_lean_status():
    return lean_status()


@app.post("/api/questions/{identifier}/formalize")
def api_formalize_question(identifier: str, req: FormalizeRequest):
    st = llm_status()
    if not st["configured"]:
        raise HTTPException(status_code=400, detail=f"Chưa cấu hình LLM ({st['provider']}). {st['hint']}")
    if not lean_status()["mathlib_ready"]:
        raise HTTPException(status_code=400, detail="Chưa có Mathlib đã build (xem MATH_LEAN_PROJECT).")
    try:
        if req.steps is not None and not set(req.steps) <= {1, 2, 3, 4}:
            raise HTTPException(status_code=400, detail="steps chỉ gồm các số 1, 2, 3, 4")
        return formalize_question(identifier, max_attempts=req.max_attempts, db_path=DB_PATH,
                                  steps=req.steps, num_candidates=req.num_candidates)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.post("/api/questions/{identifier}/mathlib-recheck")
def api_mathlib_recheck(identifier: str):
    try:
        return recheck_question(identifier, db_path=DB_PATH)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.delete("/api/questions/{code}")
def api_delete_question(code: str):
    q = get_question_by_id_or_code(code, db_path=DB_PATH)
    if not q:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy câu hỏi: {code}")
    if q.get("source") != "llm":
        raise HTTPException(status_code=403, detail="Chỉ được xóa câu hỏi do LLM sinh; câu viết tay nằm trong agents_modules.")
    delete_question(code, db_path=DB_PATH)
    return {"deleted": code}


@app.post("/api/exams/generate")
def api_generate_exam(req: GenerateExamRequest):
    rng = random.Random(req.seed or int(time.time() * 1000))
    subject = req.subject_filter if req.subject_filter != "ALL" else None
    all_qs = list_questions(subject=subject, db_path=DB_PATH, agent_ids=ACTIVE_AGENT_IDS)
    if not all_qs:
        # Nếu DB chưa nạp, tự động kích hoạt các agent đang hoạt động để nạp câu hỏi
        run_all_20_agents_parallel(db_path=DB_PATH)
        all_qs = list_questions(subject=subject, db_path=DB_PATH, agent_ids=ACTIVE_AGENT_IDS)
    if req.trust_level == "exclude_failed":
        all_qs = [q for q in all_qs if q.get("lean4_mathlib_status") not in ("FAILED", "UNCONFIRMED", "DISPROVED")]
    elif req.trust_level == "formal_only":
        all_qs = [q for q in all_qs if q.get("lean4_mathlib_status") == "VERIFIED_PASS"]

    mcq_pool = [q for q in all_qs if q["question_type"] == "mcq"]
    essay_pool = [q for q in all_qs if q["question_type"] == "essay"]

    rng.shuffle(mcq_pool)
    rng.shuffle(essay_pool)

    selected_mcqs = mcq_pool[: max(0, min(req.mcq_count, len(mcq_pool)))]
    selected_essays = essay_pool[: max(0, min(req.essay_count, len(essay_pool)))]
    combined = selected_mcqs + selected_essays

    # Sử dụng 20 worker song song để tính toán tham số & xác nhận trạng thái kiểm chứng cho toàn bộ câu hỏi trong đề
    def _prepare_exam_item(idx_and_q):
        idx, q = idx_and_q
        custom_params = None
        if req.randomize_parameters and q.get("has_parameters"):
            custom_params = sample_valid_parameters(q, seed=rng.randint(1, 10**6))
        evaluated = evaluate_question_with_params(q, custom_params=custom_params, mode=req.parameter_mode)
        return {
            "order_index": idx + 1,
            "code": q["code"],
            "agent_id": q["agent_id"],
            "agent_name": q["agent_name"],
            "subject": q["subject"],
            "topic": q["topic"],
            "question_type": q["question_type"],
            "difficulty": q["difficulty"],
            "has_parameters": q["has_parameters"],
            "parameters_schema": q["parameters_schema"],
            "active_parameters": evaluated["active_parameters"],
            "param_summary_latex": evaluated["param_summary_latex"],
            "title": q["title"],
            "stem_display": evaluated["stem_display"],
            "stem_symbolic": q["stem_symbolic"],
            "options": evaluated["options"],
            "correct_option": q["correct_option"],
            "target_evaluated_latex": evaluated["target_evaluated_latex"],
            "solution_display": evaluated["solution_display"],
            "rubric_points": q.get("rubric_points", []),
            "lean4_status": q["lean4_status"],
            "lean4_output": q["lean4_output"],
            "lean4_code": q["lean4_code"],
            "python_status": q["python_status"],
            "python_output": q["python_output"],
            "python_code": q["python_code"],
            "merkle_hash": q["merkle_hash"],
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        snapshot = list(ex.map(_prepare_exam_item, enumerate(combined)))

    exam_code = f"EXAM-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{rng.randint(100, 999)}"
    param_count = sum(1 for item in snapshot if item.get("has_parameters"))
    q_hashes = [item.get("merkle_hash", "") for item in snapshot]

    m_node = commit_merkle_node(
        node_type="EXAM_GENERATED",
        parent_hashes=q_hashes,
        payload={
            "exam_code": exam_code,
            "title": req.title,
            "total_questions": len(snapshot),
            "mcq_count": len(selected_mcqs),
            "essay_count": len(selected_essays),
            "parametric_count": param_count,
            "parameter_mode": req.parameter_mode,
        },
    )

    now = datetime.now().isoformat(timespec="seconds")
    conn = get_connection(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO exams (
                exam_code, title, subject_filter, duration_minutes,
                parameter_mode, questions_snapshot, total_questions,
                mcq_count, essay_count, parametric_count, merkle_root, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                exam_code,
                req.title,
                req.subject_filter,
                req.duration_minutes,
                req.parameter_mode,
                json.dumps(snapshot, ensure_ascii=False),
                len(snapshot),
                len(selected_mcqs),
                len(selected_essays),
                param_count,
                m_node["node"]["hash"],
                now,
            ),
        )
        conn.commit()
        exam_id = cur.lastrowid
    finally:
        conn.close()

    return {
        "id": exam_id,
        "exam_code": exam_code,
        "title": req.title,
        "subject_filter": req.subject_filter,
        "duration_minutes": req.duration_minutes,
        "parameter_mode": req.parameter_mode,
        "total_questions": len(snapshot),
        "mcq_count": len(selected_mcqs),
        "essay_count": len(selected_essays),
        "parametric_count": param_count,
        "merkle_root": m_node["node"]["hash"],
        "created_at": now,
        "questions": snapshot,
    }


@app.get("/api/exams")
def api_list_exams():
    conn = get_connection(DB_PATH)
    try:
        rows = conn.execute(
            """
            SELECT id, exam_code, title, subject_filter, duration_minutes,
                   parameter_mode, total_questions, mcq_count, essay_count,
                   parametric_count, merkle_root, created_at
            FROM exams ORDER BY id DESC
            """
        ).fetchall()
        return {"exams": [dict(r) for r in rows]}
    finally:
        conn.close()


@app.get("/api/exams/{exam_id}")
def api_get_exam(exam_id: int):
    conn = get_connection(DB_PATH)
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Không tìm thấy đề thi")
        d = dict(row)
        d["questions"] = json.loads(d.pop("questions_snapshot", "[]"))
        return d
    finally:
        conn.close()


@app.post("/api/exams/{exam_id}/submit")
def api_submit_exam(exam_id: int, req: SubmitExamRequest):
    exam = api_get_exam(exam_id)
    questions = exam["questions"]

    mcq_items = [q for q in questions if q["question_type"] == "mcq"]
    essay_items = [q for q in questions if q["question_type"] == "essay"]

    mcq_correct = 0
    details = []

    for q in mcq_items:
        qcode = q["code"]
        user_choice = req.mcq_answers.get(qcode, "")
        is_ok = user_choice == q["correct_option"]
        if is_ok:
            mcq_correct += 1
        details.append(
            {
                "code": qcode,
                "question_type": "mcq",
                "user_choice": user_choice,
                "correct_option": q["correct_option"],
                "is_correct": is_ok,
                "active_parameters": q.get("active_parameters", {}),
                "target_evaluated_latex": q.get("target_evaluated_latex", ""),
            }
        )

    essay_total = 0.0
    for q in essay_items:
        qcode = q["code"]
        self_sc = float(req.essay_self_scores.get(qcode, 0.0))
        self_sc = max(0.0, min(1.0, self_sc))
        essay_total += self_sc
        details.append(
            {
                "code": qcode,
                "question_type": "essay",
                "self_score_ratio": self_sc,
                "active_parameters": q.get("active_parameters", {}),
            }
        )

    total_items = max(1, len(mcq_items) + len(essay_items))
    raw_points = mcq_correct + essay_total
    score_10 = round((raw_points / total_items) * 10.0, 2)

    now = datetime.now().isoformat(timespec="seconds")
    conn = get_connection(DB_PATH)
    try:
        conn.execute(
            """
            INSERT INTO exam_submissions (
                exam_id, student_name, answers_json, score, max_score, detail_json, submitted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                exam_id,
                req.student_name,
                json.dumps({"mcq": req.mcq_answers, "essay": req.essay_self_scores}, ensure_ascii=False),
                score_10,
                10.0,
                json.dumps(details, ensure_ascii=False),
                now,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return {
        "exam_id": exam_id,
        "exam_code": exam["exam_code"],
        "student_name": req.student_name,
        "score": score_10,
        "max_score": 10.0,
        "mcq_correct": mcq_correct,
        "mcq_total": len(mcq_items),
        "essay_score_units": round(essay_total, 2),
        "essay_total": len(essay_items),
        "details": details,
        "submitted_at": now,
    }


@app.get("/api/exams/{exam_id}/export-latex", response_class=PlainTextResponse)
def api_export_exam_latex(exam_id: int):
    exam = api_get_exam(exam_id)
    lines = [
        r"\documentclass[12pt,a4paper]{article}",
        r"\usepackage{amsmath,amssymb,amsfonts,amsthm}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[vietnamese]{babel}",
        r"\usepackage[margin=2cm]{geometry}",
        r"\usepackage{enumitem}",
        r"\begin{document}",
        r"\begin{center}",
        r"\textbf{\Large HỆ THỐNG SINH ĐỀ TOÁN CAO CẤP SOVEREIGN (@gng5)}\\[4pt]",
        f"\\textbf{{\\large {exam['title']}}}\\\\[4pt]",
        f"Mã đề: \\textbf{{{exam['exam_code']}}} \\quad|\\quad Thời gian: {exam['duration_minutes']} phút \\quad|\\quad Chế độ tham số: \\texttt{{{exam['parameter_mode']}}}\\\\[2pt]",
        f"\\footnotesize{{Merkle Root (SHA-256): \\texttt{{{exam['merkle_root']}}}}}",
        r"\end{center}",
        r"\hrule\vspace{10pt}",
        r"\section*{PHẦN I: TRẮC NGHIỆM KHÁCH QUAN CÓ THAM SỐ}",
    ]

    for q in exam["questions"]:
        if q["question_type"] != "mcq":
            continue
        lines.append(f"\\noindent\\textbf{{Câu {q['order_index']} [{q['code']} - {q['subject']} / {q['topic']}]:}} {q['stem_display']}\\\\")
        opts = q.get("options", {})
        lines.append(r"\begin{enumerate}[label=\textbf{\Alph*.}]")
        for k in ("A", "B", "C", "D"):
            if k in opts:
                lines.append(f"  \\item {opts[k].get('display', opts[k].get('symbolic', ''))}")
        lines.append(r"\end{enumerate}\vspace{4pt}")

    lines.append(r"\section*{PHẦN II: TỰ LUẬN TOÁN CAO CẤP}")
    for q in exam["questions"]:
        if q["question_type"] != "essay":
            continue
        lines.append(f"\\noindent\\textbf{{Câu {q['order_index']} [{q['code']} - {q['subject']} / {q['topic']}]:}} {q['stem_display']}\\\\[6pt]")

    lines.append(r"\newpage")
    lines.append(r"\section*{ĐÁP ÁN, LỜI GIẢI CHI TIẾT & CHỨNG NHẬN KIỂM CHỨNG LEAN 4 + PYTHON}")
    for q in exam["questions"]:
        lines.append(f"\\subsection*{{Câu {q['order_index']} ({q['code']}) - Đáp án: {q['correct_option']}}}")
        lines.append(f"\\noindent\\textbf{{Trạng thái kiểm chứng:}} LEAN 4 = \\texttt{{{q['lean4_status']}}} \\quad|\\quad Python = \\texttt{{{q['python_status']}}}\\\\[4pt]")
        lines.append(q["solution_display"])
        lines.append(r"\vspace{6pt}")

    lines.append(r"\end{document}")
    return PlainTextResponse("\n".join(lines), media_type="text/plain; charset=utf-8")


@app.get("/api/merkle-ledger")
def api_get_merkle_ledger():
    if os.path.exists(MERKLE_LEDGER_PATH):
        with open(MERKLE_LEDGER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"system": "@gng5", "merkle_root": "0" * 64, "total_nodes": 0, "nodes": []}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8088, reload=False)
