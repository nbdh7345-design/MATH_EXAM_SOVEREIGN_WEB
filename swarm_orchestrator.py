# -*- coding: utf-8 -*-
"""
swarm_orchestrator.py - Bộ Điều Phối 25 Agent Chạy Song Song (@gng5 Parallel Swarm Engine)
Vận hành mỗi agent trên một luồng song song (ThreadPoolExecutor max_workers = số agent):
- Agent 01..10: Chuyên gia Giải tích (Giới hạn, Đạo hàm, Tích phân, Suy rộng, Chuỗi, Hàm nhiều biến, Lagrange, Tích phân bội, Giải tích Vector, PTVP)
- Agent 11..20: Chuyên gia Đại số (Định thức, Hạng ma trận, Hệ PTT, Không gian Vector, Không gian con, Ánh xạ tuyến tính, Trị riêng, Chéo hóa, Dạng toàn phương, Euclid)
- Agent 21..25: Bổ sung Giải tích 1 (Ứng dụng tích phân, Giới hạn dãy & Liên tục, Định lý giá trị trung bình & Khảo sát,
  Hàm hợp/Hàm ẩn/Đạo hàm theo hướng, Nguyên hàm & Tích phân cận biến thiên)
Mỗi Agent thực thi độc lập:
1. Sinh câu hỏi Tự luận & Trắc nghiệm chứa tham số (m, a, b...).
2. Kiểm chứng hình thức bằng trình biên dịch LEAN 4 (v4.35.0).
3. Kiểm chứng số học & ký hiệu bằng Script Python (SymPy + NumPy/SciPy).
4. Thẩm định Cổng Giám Đốc Thẩm @gng5 (T1-T5) và khắc Sổ cái Merkle DAG.
"""

import concurrent.futures
import importlib
import importlib.util
import json
import os
import sys
import time
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database import (
    DB_PATH,
    init_db,
    list_questions,
    log_verification,
    update_agent_status,
    upsert_question,
)
from verifier_engine import commit_merkle_node, verify_question_full

ALL_AGENTS: List[Dict[str, Any]] = [
    {"agent_id": 1, "agent_code": "AGENT-01", "module": "agent_01_calc_limits", "agent_name": "Agent-01 (Giải tích: Giới hạn & Taylor)", "domain": "Giải tích", "role_desc": "Giới hạn hàm số, L'Hospital & Khai triển Taylor-Maclaurin có tham số"},
    {"agent_id": 2, "agent_code": "AGENT-02", "module": "agent_02_calc_derivatives", "agent_name": "Agent-02 (Giải tích: Đạo hàm cấp cao & Cực trị)", "domain": "Giải tích", "role_desc": "Đạo hàm cấp cao Leibniz, Tiếp tuyến & Cực trị hàm 1 biến có tham số"},
    {"agent_id": 3, "agent_code": "AGENT-03", "module": "agent_03_calc_integrals", "agent_name": "Agent-03 (Giải tích: Tích phân xác định & Tham số)", "domain": "Giải tích", "role_desc": "Tích phân xác định, Đổi biến, Từng phần & Tích phân phụ thuộc tham số"},
    {"agent_id": 4, "agent_code": "AGENT-04", "module": "agent_04_calc_improper_int", "agent_name": "Agent-04 (Giải tích: Tích phân suy rộng)", "domain": "Giải tích", "role_desc": "Tích phân suy rộng loại 1, 2 & Biện luận hội tụ theo tham số"},
    {"agent_id": 5, "agent_code": "AGENT-05", "module": "agent_05_calc_series", "agent_name": "Agent-05 (Giải tích: Chuỗi số & Chuỗi lũy thừa)", "domain": "Giải tích", "role_desc": "Chuỗi số, Tổng chuỗi & Bán kính hội tụ chuỗi lũy thừa có tham số"},
    {"agent_id": 6, "agent_code": "AGENT-06", "module": "agent_06_calc_multivariable", "agent_name": "Agent-06 (Giải tích: Vi phân hàm nhiều biến)", "domain": "Giải tích", "role_desc": "Đạo hàm riêng, Ma trận Hessian & Cực trị tự do hàm nhiều biến"},
    {"agent_id": 7, "agent_code": "AGENT-07", "module": "agent_07_calc_lagrange_extrema", "agent_name": "Agent-07 (Giải tích: Nhân tử Lagrange)", "domain": "Giải tích", "role_desc": "Cực trị có điều kiện, Nhân tử Lagrange & GTLN/GTNN miền compact"},
    {"agent_id": 8, "agent_code": "AGENT-08", "module": "agent_08_calc_multiple_int", "agent_name": "Agent-08 (Giải tích: Tích phân kép & bội ba)", "domain": "Giải tích", "role_desc": "Tích phân kép, Tích phân bội ba, Đổi biến tọa độ cực/trụ/cầu"},
    {"agent_id": 9, "agent_code": "AGENT-09", "module": "agent_09_calc_vector_fields", "agent_name": "Agent-09 (Giải tích: Giải tích Vector)", "domain": "Giải tích", "role_desc": "Tích phân đường, Tích phân mặt, Định lý Green - Stokes - Gauss"},
    {"agent_id": 10, "agent_code": "AGENT-10", "module": "agent_10_calc_ode", "agent_name": "Agent-10 (Giải tích: Phương trình vi phân)", "domain": "Giải tích", "role_desc": "Phương trình vi phân cấp 1, cấp 2, Bài toán Cauchy & Hệ PTVP"},
    {"agent_id": 11, "agent_code": "AGENT-11", "module": "agent_11_alg_matrices_det", "agent_name": "Agent-11 (Đại số: Ma trận & Định thức)", "domain": "Đại số", "role_desc": "Định thức cấp n chứa tham số, Ma trận phụ hợp & Ma trận nghịch đảo"},
    {"agent_id": 12, "agent_code": "AGENT-12", "module": "agent_12_alg_matrix_rank", "agent_name": "Agent-12 (Đại số: Hạng của ma trận)", "domain": "Đại số", "role_desc": "Biện luận hạng của ma trận rank(A(m)) bằng biến đổi sơ cấp Gauss"},
    {"agent_id": 13, "agent_code": "AGENT-13", "module": "agent_13_alg_linear_systems", "agent_name": "Agent-13 (Đại số: Hệ phương trình tuyến tính)", "domain": "Đại số", "role_desc": "Hệ phương trình tuyến tính Cramer, Gauss, Kronecker-Capelli theo m"},
    {"agent_id": 14, "agent_code": "AGENT-14", "module": "agent_14_alg_vector_spaces", "agent_name": "Agent-14 (Đại số: Không gian Vector & Cơ sở)", "domain": "Đại số", "role_desc": "Độc lập/Phụ thuộc tuyến tính, Cơ sở, Số chiều & Ma trận chuyển cơ sở"},
    {"agent_id": 15, "agent_code": "AGENT-15", "module": "agent_15_alg_subspaces_sum", "agent_name": "Agent-15 (Đại số: Không gian con & Grassmann)", "domain": "Đại số", "role_desc": "Không gian vector con, Giao & Tổng trực tiếp, Công thức Grassmann"},
    {"agent_id": 16, "agent_code": "AGENT-16", "module": "agent_16_alg_linear_maps", "agent_name": "Agent-16 (Đại số: Ánh xạ tuyến tính, Ker & Im)", "domain": "Đại số", "role_desc": "Ma trận ánh xạ tuyến tính, Hạt nhân Ker(f), Ảnh Im(f) & Số chiều"},
    {"agent_id": 17, "agent_code": "AGENT-17", "module": "agent_17_alg_eigenvalues", "agent_name": "Agent-17 (Đại số: Trị riêng & Vector riêng)", "domain": "Đại số", "role_desc": "Đa thức đặc trưng P(lambda; m), Trị riêng, Vector riêng & Vết"},
    {"agent_id": 18, "agent_code": "AGENT-18", "module": "agent_18_alg_diagonalization", "agent_name": "Agent-18 (Đại số: Chéo hóa & Cayley-Hamilton)", "domain": "Đại số", "role_desc": "Điều kiện chéo hóa theo tham số m, Định lý Cayley-Hamilton & A^n(m)"},
    {"agent_id": 19, "agent_code": "AGENT-19", "module": "agent_19_alg_quadratic_forms", "agent_name": "Agent-19 (Đại số: Dạng toàn phương & Sylvester)", "domain": "Đại số", "role_desc": "Dạng toàn phương, Chính tắc Lagrange/Jacobi & Tiêu chuẩn Sylvester"},
    {"agent_id": 20, "agent_code": "AGENT-20", "module": "agent_20_alg_euclidean_spaces", "agent_name": "Agent-20 (Đại số: Không gian Euclid & Gram-Schmidt)", "domain": "Đại số", "role_desc": "Tích vô hướng tham số, Trực giao hóa Gram-Schmidt & Hình chiếu"},
    # Bổ sung các dạng bài Giải tích 1 còn thiếu trong ngân hàng
    {"agent_id": 21, "agent_code": "AGENT-21", "module": "agent_21_calc_integral_applications", "agent_name": "Agent-21 (Giải tích: Ứng dụng của tích phân)", "domain": "Giải tích", "role_desc": "Diện tích hình phẳng, Thể tích vật tròn xoay, Độ dài cung & Diện tích trong tọa độ cực có tham số"},
    {"agent_id": 22, "agent_code": "AGENT-22", "module": "agent_22_calc_continuity", "agent_name": "Agent-22 (Giải tích: Giới hạn dãy, VCB & Liên tục)", "domain": "Giải tích", "role_desc": "Giới hạn dãy dạng 1^∞, Thay VCB tương đương, Tham số để hàm liên tục & Phân loại điểm gián đoạn"},
    {"agent_id": 23, "agent_code": "AGENT-23", "module": "agent_23_calc_mean_value_sketch", "agent_name": "Agent-23 (Giải tích: Định lý giá trị trung bình & Khảo sát hàm số)", "domain": "Giải tích", "role_desc": "Định lý Rolle, Lagrange, Tiệm cận đứng/xiên, Lồi lõm & Điểm uốn có tham số"},
    {"agent_id": 24, "agent_code": "AGENT-24", "module": "agent_24_calc_multivariable_chain", "agent_name": "Agent-24 (Giải tích: Hàm hợp, Hàm ẩn & Đạo hàm theo hướng)", "domain": "Giải tích", "role_desc": "Đạo hàm hàm hợp nhiều biến, Đạo hàm hàm ẩn, Giới hạn hàm hai biến & Đạo hàm theo hướng có tham số"},
    {"agent_id": 25, "agent_code": "AGENT-25", "module": "agent_25_calc_antiderivatives", "agent_name": "Agent-25 (Giải tích: Nguyên hàm & Tích phân cận biến thiên)", "domain": "Giải tích", "role_desc": "Tích phân hàm hữu tỷ (tách phân thức), Tích phân cận biến thiên & Tích phân tam thức bậc hai có tham số"},
]

# Các agent đang hoạt động: mặc định chỉ Giải tích 1 (hàm một biến + vi phân hàm nhiều biến). Agent bị tắt vẫn giữ
# module và câu hỏi trong CSDL, chỉ không chạy swarm, không sinh câu, không hiện trên giao diện, không vào đề thi.
# Đổi bằng MATH_ACTIVE_AGENTS, ví dụ "1,2,3" hoặc "all".
GIAI_TICH_1_AGENT_IDS = [1, 2, 3, 4, 6, 7, 21, 22, 23, 24, 25]
_active_env = os.environ.get("MATH_ACTIVE_AGENTS", "").replace(" ", "")
ACTIVE_AGENT_IDS = (
    [a["agent_id"] for a in ALL_AGENTS] if _active_env == "all"
    else [int(s) for s in _active_env.split(",") if s] if _active_env
    else GIAI_TICH_1_AGENT_IDS
)
AGENTS_REGISTRY: List[Dict[str, Any]] = [a for a in ALL_AGENTS if a["agent_id"] in ACTIVE_AGENT_IDS]

# Thang độ khó thống nhất cho toàn bộ ngân hàng (trùng với llm_generator.DIFFICULTIES và API sinh câu hỏi)
DIFFICULTY_LEVELS = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]


def load_agent_questions(agent_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    mod_name = agent_info["module"]
    mod_path = os.path.join(BASE_DIR, "agents_modules", f"{mod_name}.py")
    if not os.path.exists(mod_path):
        return []
    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    if spec is None or spec.loader is None:
        return []
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "get_questions"):
        qs = module.get_questions()
        for q in qs:
            q.setdefault("agent_id", agent_info["agent_id"])
            q.setdefault("agent_name", agent_info["agent_name"])
            q.setdefault("subject", agent_info["domain"])
            if q.get("difficulty") not in DIFFICULTY_LEVELS:
                raise ValueError(
                    f"{q.get('code')}: độ khó {q.get('difficulty')!r} không thuộc thang 4 mức {DIFFICULTY_LEVELS}"
                )
        return qs
    return []


def load_db_questions(agent_id: int, exclude_codes: List[str], db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Câu của agent chỉ có trong CSDL: câu do LLM sinh theo chủ đề (source = 'llm') và câu viết tay đã chuyển
    khỏi module (module chỉ giữ 2 câu trắc nghiệm + 1 câu tự luận làm mẫu)."""
    skip = set(exclude_codes)
    return [q for q in list_questions(agent_id=agent_id, db_path=db_path) if q["code"] not in skip]


def _execute_single_agent(agent_info: Dict[str, Any], db_path: str = DB_PATH) -> Dict[str, Any]:
    """Hàm thực thi độc lập của 1 Agent trong dàn Agent song song."""
    aid = agent_info["agent_id"]
    acode = agent_info["agent_code"]
    aname = agent_info["agent_name"]
    domain = agent_info["domain"]
    rdesc = agent_info["role_desc"]

    t0 = time.perf_counter()
    update_agent_status(
        agent_id=aid,
        agent_code=acode,
        agent_name=aname,
        domain=domain,
        role_desc=rdesc,
        status="RUNNING",
        last_task="Đang nạp câu hỏi & khởi chạy kiểm chứng kép LEAN 4 + Python...",
        db_path=db_path,
    )

    try:
        handwritten = load_agent_questions(agent_info)
        stored = load_db_questions(aid, [q["code"] for q in handwritten], db_path)
        generated = [q for q in stored if q.get("source") == "llm"]
        questions = handwritten + stored
        q_count = len(questions)
        lean_total = 0  # số câu có mã Lean Core (câu do LLM sinh không có)
        lean_ok = 0
        py_ok = 0
        question_hashes: List[str] = []

        for q in questions:
            res = verify_question_full(q)
            verified_q = res["question"]
            upsert_question(verified_q, db_path=db_path)

            if res["lean4"]["status"] != "NOT_APPLICABLE":
                lean_total += 1
            if res["lean4"]["status"] == "VERIFIED_PASS":
                lean_ok += 1
            if res["python"]["status"] == "VERIFIED_PASS":
                py_ok += 1

            log_verification(
                question_code=verified_q["code"],
                agent_id=aid,
                verifier_type="LEAN4+PYTHON_DUAL",
                status=res["sovereign_verdict"],
                execution_ms=round(res["lean4"]["elapsed_ms"] + res["python"]["elapsed_ms"], 2),
                output_log=f"LEAN4: {res['lean4']['output']}\nPYTHON: {res['python']['output']}",
                merkle_hash=res["merkle_hash"],
                db_path=db_path,
            )
            question_hashes.append(res["merkle_hash"])

        # Bản formalize Mathlib nằm ở cột riêng trong CSDL (lean_formalizer), không đi qua verify_question_full
        mathlib_ok = sum(1 for q in list_questions(agent_id=aid, db_path=db_path)
                         if q.get("lean4_mathlib_status") == "VERIFIED_PASS")
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        m_node = commit_merkle_node(
            node_type=f"AGENT_{aid:02d}_VERIFICATION",
            parent_hashes=question_hashes,
            payload={
                "agent_id": aid,
                "agent_code": acode,
                "agent_name": aname,
                "domain": domain,
                "questions_processed": q_count,
                "llm_questions": len(generated),
                "lean4_applicable": lean_total,
                "lean4_verified": lean_ok,
                "python_verified": py_ok,
                "mathlib_verified": mathlib_ok,
                "elapsed_ms": elapsed_ms,
            },
        )
        node_hash = m_node["node"]["hash"]

        final_status = "COMPLETED_PASS" if (q_count > 0 and lean_ok == lean_total and py_ok == q_count) else ("PARTIAL" if q_count > 0 else "WAITING_MODULE")
        update_agent_status(
            agent_id=aid,
            agent_code=acode,
            agent_name=aname,
            domain=domain,
            role_desc=rdesc,
            status=final_status,
            questions_generated=q_count,
            lean4_verified=lean_ok,
            python_verified=py_ok,
            last_task=(f"Hoàn tất {q_count} câu hỏi ({len(handwritten)} mẫu trong module, "
                       f"{len(stored) - len(generated)} viết tay trong CSDL, {len(generated)} do LLM sinh; "
                       f"Lean4: {lean_ok}/{lean_total}, Python: {py_ok}/{q_count}, Mathlib: {mathlib_ok}/{q_count})"),
            elapsed_ms=elapsed_ms,
            merkle_node_hash=node_hash,
            db_path=db_path,
        )
        return {
            "agent_id": aid,
            "agent_code": acode,
            "agent_name": aname,
            "status": final_status,
            "questions_generated": q_count,
            "llm_questions": len(generated),
            "lean4_applicable": lean_total,
            "lean4_verified": lean_ok,
            "python_verified": py_ok,
            "mathlib_verified": mathlib_ok,
            "elapsed_ms": elapsed_ms,
            "merkle_node_hash": node_hash,
        }
    except Exception as e:
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        err_msg = f"{e}\n{traceback.format_exc()}"
        update_agent_status(
            agent_id=aid,
            agent_code=acode,
            agent_name=aname,
            domain=domain,
            role_desc=rdesc,
            status="ERROR",
            last_task=f"Lỗi: {str(e)[:120]}",
            elapsed_ms=elapsed_ms,
            db_path=db_path,
        )
        return {
            "agent_id": aid,
            "agent_code": acode,
            "status": "ERROR",
            "error": err_msg,
            "elapsed_ms": elapsed_ms,
        }


def run_all_20_agents_parallel(db_path: str = DB_PATH) -> Dict[str, Any]:
    """
    Khởi chạy đồng thời toàn bộ Agent trong AGENTS_REGISTRY, mỗi Agent một luồng (ThreadPoolExecutor)
    để nạp, sinh và kiểm chứng toàn bộ ngân hàng câu hỏi Giải tích & Đại số bằng LEAN 4 và Python.
    """
    init_db(db_path)
    t_start = time.perf_counter()
    results: List[Dict[str, Any]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(AGENTS_REGISTRY)) as executor:
        future_map = {
            executor.submit(_execute_single_agent, agent_info, db_path): agent_info["agent_id"]
            for agent_info in AGENTS_REGISTRY
        }
        for fut in concurrent.futures.as_completed(future_map):
            results.append(fut.result())

    results.sort(key=lambda x: x.get("agent_id", 0))
    total_elapsed_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

    total_q = sum(r.get("questions_generated", 0) for r in results)
    total_llm = sum(r.get("llm_questions", 0) for r in results)
    total_lean_applicable = sum(r.get("lean4_applicable", 0) for r in results)
    total_lean = sum(r.get("lean4_verified", 0) for r in results)
    total_py = sum(r.get("python_verified", 0) for r in results)
    total_mathlib = sum(r.get("mathlib_verified", 0) for r in results)
    parent_hashes = [r.get("merkle_node_hash", "") for r in results if r.get("merkle_node_hash")]

    settlement = commit_merkle_node(
        node_type="SOVEREIGN_20_AGENT_SWARM_SETTLEMENT",
        parent_hashes=parent_hashes,
        payload={
            "swarm_size": len(AGENTS_REGISTRY),
            "total_questions": total_q,
            "llm_questions": total_llm,
            "lean4_applicable": total_lean_applicable,
            "lean4_verified": total_lean,
            "python_verified": total_py,
            "mathlib_verified": total_mathlib,
            "wall_clock_ms": total_elapsed_ms,
            "verdict": "SOVEREIGN_PASSED" if (total_q > 0 and total_lean == total_lean_applicable and total_py == total_q) else "PARTIAL",
            "signature": "Gemini-3.8-Flash-High Sovereign Epistemic Gate (@gng5 Apex Dual-Core Native Mode: @gng4 Prover + @gng3 Refuter)",
        },
    )

    return {
        "status": "SUCCESS",
        "swarm_workers": len(AGENTS_REGISTRY),
        "total_questions": total_q,
        "llm_questions": total_llm,
        "lean4_applicable": total_lean_applicable,
        "lean4_verified": total_lean,
        "python_verified": total_py,
        "mathlib_verified": total_mathlib,
        "wall_clock_ms": total_elapsed_ms,
        "merkle_root": settlement["merkle_root"],
        "settlement_hash": settlement["node"]["hash"],
        "agent_results": results,
    }


if __name__ == "__main__":
    summary = run_all_20_agents_parallel()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
