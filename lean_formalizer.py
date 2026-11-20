# -*- coding: utf-8 -*-
"""
lean_formalizer.py - Lớp chuyển đổi giữa câu hỏi trong ngân hàng (NV1) và lõi dùng chung lean_core.py (FR08 + FR09).

Từ một câu hỏi trong CSDL, hệ thống tự điền phần cố định (QT17): header định lý `exam_answer`, tham số nguyên và miền
giá trị, đáp án (SymPy, đã qua bộ giải độc lập) vào chỗ ANSWER. Lõi hình thức hóa đề rồi chứng minh; lớp này ghi kết
quả vào CSDL (cột lean4_mathlib_*) và nhật ký kiểm chứng.
"""

import json
import time
from typing import Any, Dict, List, Optional

import sympy as sp

from database import DB_PATH, get_question_by_id_or_code, log_verification, update_mathlib_result
from lean_core import (  # noqa: F401  (lean_status, warmup_mathlib, lean_imports dùng ở app.py và công cụ khác)
    PROOF_FIXES, CoreRun, FormalTask, compile_lean, ensure_mathlib, formalize_and_prove, lean_imports, lean_status,
    param_binders, param_domain_note, warmup_mathlib,
)
from parametric_engine import _normalize_schema, parse_sympy_expr


def _answer_expr(q: Dict[str, Any]) -> str:
    formulas = q.get("parametric_formulas") or {}
    if isinstance(formulas, str):
        formulas = json.loads(formulas or "{}")
    target = formulas.get("target_expr")
    if not target:
        opts = formulas.get("options", {})
        target = opts.get(q.get("correct_option", ""))
    if not target:
        raise ValueError("Câu hỏi không có công thức đáp án (target_expr) để formalize")
    return target


def question_task(q: Dict[str, Any]) -> FormalTask:
    """Phát biểu cần hình thức hóa của một câu hỏi: đề bài, tham số + miền, đáp án do hệ thống điền, lời giải tham khảo."""
    params = _normalize_schema(q.get("parameters_schema", []))
    names = [p["name"] for p in params]
    answer_sympy = _answer_expr(q)
    return FormalTask(
        code=q["code"],
        text_vi=q["stem_symbolic"],
        binders=param_binders(params),
        domain_note=param_domain_note(params),
        answer_sympy=answer_sympy,
        answer_expr=parse_sympy_expr(answer_sympy, {n: sp.Symbol(n, real=True) for n in names}),
        answer_vars=names,
        hint=q.get("solution_symbolic") or "",
    )


def formalize_question(identifier: str, max_attempts: Optional[int] = None, db_path: str = DB_PATH,
                       steps: Optional[List[int]] = None, num_candidates: Optional[int] = None,
                       question: Optional[Dict[str, Any]] = None, persist: bool = True) -> Dict[str, Any]:
    """Formalize một câu hỏi. Mặc định đọc câu từ CSDL và ghi kết quả vào CSDL; khi sinh câu mới bằng LLM thì
    truyền `question` (câu chưa lưu) và persist=False: người gọi chỉ lưu câu khi kết quả là VERIFIED_PASS."""
    q = question or get_question_by_id_or_code(identifier, db_path=db_path)
    if not q:
        raise ValueError(f"Không tìm thấy câu hỏi: {identifier}")
    ensure_mathlib()
    run = CoreRun(steps, num_candidates)
    task = question_task(q)
    t0 = time.perf_counter()
    proof_fixes = PROOF_FIXES if max_attempts is None else max(0, max_attempts - 1)
    res = formalize_and_prove(task, run, proof_fixes)

    if persist:
        update_mathlib_result(q["code"], lean_code=res["lean_code"], status=res["status"], output=res["output"],
                              review=res["review"].get("issues", ""), db_path=db_path)
    elapsed = round((time.perf_counter() - t0) * 1000.0, 2)
    log_verification(
        question_code=q["code"], agent_id=int(q.get("agent_id", 0)), verifier_type="LEAN4_MATHLIB_LLM_FORMALIZE",
        status=res["status"], execution_ms=elapsed, output_log=res["summary"], merkle_hash="", db_path=db_path,
    )
    return {
        "code": q["code"],
        "status": res["status"],
        "attempts": run.proof_calls,
        "history": run.history,
        "summary": res["summary"],
        "output": res["output"],
        "review": res["review"],
        "lean_code": res["lean_code"],
        "statement": res["statement"],
        "elapsed_ms": elapsed,
        "pipeline": run.pipeline,
    }


def recheck_question(identifier: str, db_path: str = DB_PATH) -> Dict[str, Any]:
    """Biên dịch lại file Mathlib đã lưu (không gọi LLM)."""
    q = get_question_by_id_or_code(identifier, db_path=db_path)
    if not q or not q.get("lean4_mathlib_code"):
        raise ValueError("Câu hỏi chưa có bản formalize Mathlib")
    res = compile_lean(q["code"], q["lean4_mathlib_code"])
    status = "VERIFIED_PASS" if res["ok"] else "FAILED"
    update_mathlib_result(q["code"], lean_code=q["lean4_mathlib_code"], status=status,
                          output=("; ".join(res["problems"]) or "OK") + "\n" + res["output"][-3000:],
                          review=q.get("lean4_mathlib_review", ""), db_path=db_path)
    return {"code": q["code"], "status": status, **res}
