# -*- coding: utf-8 -*-
"""
llm_generator.py - Sinh câu hỏi mới bằng LLM (Qwen hoặc Claude) theo chủ đề của từng Agent, kèm kiểm chứng độc lập.

Quy trình cho mỗi câu hỏi (một "agent" chuyên đề):
1. GENERATOR: LLM sinh câu hỏi tham số (đề, 4 phương án + công thức SymPy, đáp án, lời giải, rubric)
   theo đúng chủ đề của agent, tham khảo các câu viết tay có sẵn làm mẫu.
2. SOLVER ĐỘC LẬP: một lượt gọi LLM khác CHỈ nhìn thấy đề bài (không thấy đáp án, không thấy phương án),
   viết hàm Python `solve(...)` dùng SymPy để tính trực tiếp đáp số từ đề.
3. ĐỐI CHIẾU: chạy bộ giải trên toàn bộ lưới tham số và so với công thức đáp án sẽ lưu vào CSDL:
   - đáp án đúng phải khớp bộ giải tại mọi điểm,
   - 3 phương án nhiễu phải khác bộ giải và 4 phương án phải đôi một phân biệt,
   - giá trị tham số gây trùng phương án được đưa vào danh sách `forbidden`.
4. SỬA LẠI: nếu bị loại, gửi lý do cho GENERATOR để sinh lại (tối đa `max_attempts` lần).
Chỉ câu vượt qua bước 3 mới được lưu vào ngân hàng câu hỏi (source = 'llm').
"""

import ast
import concurrent.futures
import itertools
import json
import math
import os
import random
import re
import secrets
import subprocess
import sys
import shutil
import tempfile
import threading
import time
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp

from database import DB_PATH, list_questions, log_verification, update_mathlib_result, upsert_question
from parametric_engine import SAFE_SYMPY_LOCALS, parse_sympy_expr
from swarm_orchestrator import AGENTS_REGISTRY, load_agent_questions
from verifier_engine import commit_merkle_node, verify_python_code

# Nhà cung cấp LLM:
#   "qwen"      - mọi endpoint chuẩn OpenAI (Alibaba Model Studio/DashScope, Ollama, LM Studio, vLLM...)
#   "anthropic" - Claude qua Anthropic SDK (cần ANTHROPIC_API_KEY, tính tiền theo token)
#   "claude-cli" - Claude Code CLI (`claude -p`) đăng nhập bằng gói claude.ai (Pro/Max): không cần API key,
#                  tính vào hạn mức sử dụng của gói
LLM_PROVIDER = os.environ.get("MATH_LLM_PROVIDER", "qwen").lower()
_DEFAULT_MODEL = {"anthropic": "claude-opus-5-5", "claude-cli": "opus"}.get(LLM_PROVIDER, "qwen-plus")
LLM_MODEL = os.environ.get("MATH_LLM_MODEL", _DEFAULT_MODEL)
LLM_EFFORT = os.environ.get("MATH_LLM_EFFORT", "high")  # chỉ dùng cho Claude
LLM_MAX_TOKENS = 64000

# Cấu hình cho provider "claude-cli"
CLAUDE_CLI_TIMEOUT_SEC = float(os.environ.get("MATH_CLAUDE_CLI_TIMEOUT", "900"))
# Mỗi lượt gọi là một tiến trình claude riêng (vài trăm MB RAM) và cùng tính vào hạn mức của gói: giới hạn song song
_claude_cli_slots = threading.Semaphore(int(os.environ.get("MATH_CLAUDE_CLI_MAX_PARALLEL", "2")))

# Cấu hình cho provider "qwen"
QWEN_BASE_URL = os.environ.get("MATH_LLM_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
QWEN_API_KEY = os.environ.get("MATH_LLM_API_KEY") or os.environ.get("DASHSCOPE_API_KEY", "")
# "json_object" tương thích rộng nhất; "json_schema" nếu endpoint hỗ trợ ép theo schema
QWEN_JSON_MODE = os.environ.get("MATH_LLM_JSON_MODE", "json_object")
QWEN_MAX_TOKENS = int(os.environ.get("MATH_LLM_MAX_TOKENS", "8192"))
QWEN_TIMEOUT_SEC = float(os.environ.get("MATH_LLM_TIMEOUT", "600"))
# Tham số bổ sung gửi kèm request, ví dụ '{"enable_thinking": false}' cho DashScope
QWEN_EXTRA_BODY = json.loads(os.environ.get("MATH_LLM_EXTRA_BODY", "{}") or "{}")

SOLVER_TIMEOUT_SEC = 120

ALLOWED_PARAM_NAMES = {"m", "n", "k", "a", "b", "c", "p", "q"}
MAX_GRID_POINTS = 100
MIN_VALID_POINTS = 3
DIFFICULTIES = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]

_client = None


def _is_local_url(url: str) -> bool:
    return any(h in url for h in ("://localhost", "://127.0.0.1", "://0.0.0.0", "://[::1]"))


def _find_claude_cli() -> str:
    """Đường dẫn claude CLI: MATH_CLAUDE_CLI, `claude` trên PATH, hoặc bản đi kèm tiện ích VS Code (mới nhất)."""
    if os.environ.get("MATH_CLAUDE_CLI"):
        return os.environ["MATH_CLAUDE_CLI"]
    found = shutil.which("claude")
    if found:
        return found
    exe = "claude.exe" if sys.platform == "win32" else "claude"
    bundled = Path.home().glob(f".vscode/extensions/anthropic.claude-code-*/resources/native-binary/{exe}")

    def version(p: Path) -> Tuple[int, ...]:
        m = re.search(r"claude-code-([\d.]+)", str(p))
        return tuple(int(x) for x in m.group(1).split(".") if x) if m else ()

    best = max(bundled, key=version, default=None)
    return str(best) if best else ""


def _claude_cli_env() -> Dict[str, str]:
    # Bỏ API key để CLI dùng phiên đăng nhập claude.ai (gói Pro/Max) thay vì tính tiền theo API
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    env["PYTHONIOENCODING"] = "utf-8"
    return env


@lru_cache(maxsize=1)
def _claude_cli_login() -> str:
    """Kiểm tra một lần: CLI có chạy được và đã đăng nhập claude.ai chưa. Trả về chuỗi rỗng nếu ổn, ngược lại là lý do."""
    cli = _find_claude_cli()
    if not cli:
        return "Không tìm thấy claude CLI (cài Claude Code hoặc đặt MATH_CLAUDE_CLI)."
    try:
        proc = subprocess.run([cli, "auth", "status"], capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=60, env=_claude_cli_env())
        info = json.loads(proc.stdout or "{}")
    except Exception as exc:
        return f"Không chạy được claude CLI: {exc}"
    if not info.get("loggedIn"):
        return "claude CLI chưa đăng nhập: chạy `claude` rồi /login bằng tài khoản claude.ai."
    return ""


def llm_status() -> Dict[str, Any]:
    if LLM_PROVIDER == "claude-cli":
        problem = _claude_cli_login()
        configured = not problem
        hint = problem or "Dùng gói claude.ai qua Claude Code CLI."
        endpoint = _find_claude_cli()
    elif LLM_PROVIDER == "anthropic":
        configured = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
        hint = "Đặt ANTHROPIC_API_KEY."
        endpoint = "api.anthropic.com"
    else:
        configured = bool(QWEN_API_KEY) or _is_local_url(QWEN_BASE_URL)
        hint = "Đặt DASHSCOPE_API_KEY (hoặc MATH_LLM_API_KEY), hoặc trỏ MATH_LLM_BASE_URL tới Qwen chạy local."
        endpoint = QWEN_BASE_URL
    return {
        "provider": LLM_PROVIDER,
        "configured": configured,
        "model": LLM_MODEL,
        "endpoint": endpoint,
        "effort": LLM_EFFORT if LLM_PROVIDER in ("anthropic", "claude-cli") else "",
        "hint": hint,
    }


def _get_client():
    global _client
    if _client is None:
        if LLM_PROVIDER == "anthropic":
            import anthropic

            _client = anthropic.Anthropic()
        else:
            from openai import OpenAI

            # Server local (Ollama, LM Studio...) không cần key nhưng thư viện yêu cầu chuỗi khác rỗng
            _client = OpenAI(base_url=QWEN_BASE_URL, api_key=QWEN_API_KEY or "local", timeout=QWEN_TIMEOUT_SEC)
    return _client


# =============================================================================
# Schema JSON cho structured outputs
# =============================================================================

GENERATOR_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "difficulty": {"type": "string", "enum": DIFFICULTIES},
        "parameters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "label": {"type": "string"},
                    "min": {"type": "integer"},
                    "max": {"type": "integer"},
                    "default": {"type": "integer"},
                },
                "required": ["name", "label", "min", "max", "default"],
                "additionalProperties": False,
            },
        },
        "stem_symbolic": {"type": "string"},
        "stem_template": {"type": "string"},
        "options": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "latex": {"type": "string"},
                    "formula": {"type": "string"},
                },
                "required": ["latex", "formula"],
                "additionalProperties": False,
            },
        },
        "correct_index": {"type": "integer"},
        "answer_formula": {"type": "string"},
        "solution_markdown": {"type": "string"},
        "rubric_points": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "title", "difficulty", "parameters", "stem_symbolic", "stem_template", "options",
        "correct_index", "answer_formula", "solution_markdown", "rubric_points",
    ],
    "additionalProperties": False,
}

SOLVER_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "solver_code": {"type": "string"},
        "notes": {"type": "string"},
    },
    "required": ["solver_code", "notes"],
    "additionalProperties": False,
}


# =============================================================================
# Prompt
# =============================================================================

GENERATOR_SYSTEM = """Bạn là giảng viên Toán cao cấp giàu kinh nghiệm, chuyên ra đề thi đại học (Giải tích và Đại số tuyến tính) bằng tiếng Việt.
Nhiệm vụ: sinh MỘT câu hỏi MỚI có tham số nguyên cho ngân hàng đề, đúng chủ đề được giao.

Yêu cầu bắt buộc:
- Tham số: 1 hoặc 2 tham số nguyên, tên chọn trong {m, n, k, a, b, c, p, q}. Mỗi tham số có miền [min, max] gồm 4 đến 9 giá trị nguyên, default nằm trong miền. Không dùng tên tham số trùng biến của bài (x, y, z, t).
- Bài toán phải có đáp số DUY NHẤT là một biểu thức đóng theo tham số, tính được hoàn toàn bằng SymPy (giới hạn, đạo hàm, tích phân, tổng chuỗi, định thức, hạng, trị riêng, nghiệm PTVP tại một điểm, ...). Đáp số phải là số thực hữu hạn với mọi giá trị tham số trong miền.
- Công thức (answer_formula và formula của từng phương án) viết theo cú pháp SymPy: chỉ dùng tên tham số, số, + - * / ** ( ) và các hàm sqrt, exp, log, sin, cos, tan, atan, asin, acos, pi, E, Rational(a, b), factorial, binomial, Abs. Không dùng ^, không dùng biến khác ngoài tham số.
- stem_symbolic: đề bài Markdown + LaTeX ($...$ hoặc $$...$$), tham số để dạng ký hiệu.
- stem_template: cùng đề bài nhưng mỗi chỗ cần thay giá trị tham số viết đúng dạng {m} (dấu ngoặc nhọn bao quanh tên tham số).
- Câu trắc nghiệm (mcq): đúng 4 phương án; `correct_index` là chỉ số (0..3) của phương án đúng; formula của phương án đúng phải bằng answer_formula. 3 phương án nhiễu mô phỏng lỗi sai điển hình của sinh viên (sai dấu, quên hệ số, nhầm công thức) và phải KHÁC đáp án đúng, đôi một khác nhau, tại MỌI giá trị tham số trong miền.
- Câu tự luận (essay): options = [], correct_index = -1, answer_formula là đáp số cuối cùng của bài.
- solution_markdown: lời giải chi tiết từng bước (Markdown + LaTeX), KHÔNG nhắc tới chữ cái phương án (A/B/C/D) vì thứ tự phương án sẽ được xáo trộn.
- rubric_points: 3 đến 5 ý chấm điểm, mỗi ý ghi kèm số điểm.
- Câu hỏi phải khác hẳn các câu đã có trong ngân hàng (được liệt kê bên dưới), không chỉ đổi số."""

SOLVER_SYSTEM = """Bạn là người kiểm định độc lập cho đề thi Toán cao cấp. Bạn CHỈ được xem đề bài, không biết đáp án của người ra đề.
Nhiệm vụ: viết mã Python định nghĩa hàm `solve(<tham số>)` nhận các tham số nguyên (keyword arguments đúng tên tham số) và trả về đáp số chính xác dưới dạng biểu thức SymPy (hoặc số).

Yêu cầu bắt buộc:
- TÍNH TRỰC TIẾP từ dữ kiện đề bài bằng SymPy: sp.limit, sp.diff, sp.integrate, sp.summation, sp.series, sp.Matrix(...).det()/.rank()/.eigenvals(), sp.solve, sp.dsolve, ... KHÔNG được tự giải tay rồi trả về công thức đóng, vì mục đích là kiểm tra lại người ra đề.
- Chỉ được import: sympy (import sympy as sp), math, fractions, itertools, functools. Không dùng os, sys, file, mạng, eval, exec, __import__, thuộc tính bắt đầu bằng dấu gạch dưới.
- Mã phải chạy được độc lập, không in ra màn hình, mỗi lần gọi solve(...) chạy dưới 10 giây.
- Nếu đề hỏi một số nguyên (ví dụ số chiều, hạng, ngưỡng hội tụ), hãy tính nó bằng lập luận lập trình được (duyệt, kiểm tra điều kiện) dựa trên SymPy.
- Trường notes: tóm tắt ngắn cách bạn tính."""


def _agent_examples(agent_info: Dict[str, Any], db_path: str, limit: int = 2) -> List[Dict[str, Any]]:
    """Câu mẫu cho GENERATOR: luôn giữ một câu viết tay làm chuẩn; các chỗ còn lại ưu tiên câu LLM sinh của agent
    đã formalize Mathlib thành công (mới nhất trước), thiếu thì bù bằng câu viết tay."""
    handwritten = load_agent_questions(agent_info)
    verified = [q for q in list_questions(agent_id=agent_info["agent_id"], db_path=db_path)
                if q.get("source") == "llm" and q.get("lean4_mathlib_status") == "VERIFIED_PASS"]
    picked = handwritten[:1] + verified[::-1][:limit - 1]
    picked += handwritten[1:1 + limit - len(picked)]
    out = []
    for q in picked:
        out.append(
            {
                "question_type": q.get("question_type"),
                "title": q.get("title"),
                "parameters_schema": q.get("parameters_schema"),
                "stem_symbolic": q.get("stem_symbolic"),
                "stem_template": q.get("stem_template"),
                "options_symbolic": q.get("options_symbolic"),
                "parametric_formulas": q.get("parametric_formulas"),
            }
        )
    return out


def _existing_titles(agent_id: int, db_path: str) -> List[str]:
    return [q["title"] for q in list_questions(agent_id=agent_id, db_path=db_path)]


def _build_generator_prompt(
    agent_info: Dict[str, Any],
    question_type: str,
    difficulty: str,
    examples: List[Dict[str, Any]],
    titles: List[str],
    feedback: Optional[str],
) -> str:
    kind = "trắc nghiệm 4 phương án (mcq)" if question_type == "mcq" else "tự luận (essay)"
    parts = [
        f"Chủ đề của agent: {agent_info['agent_name']} — {agent_info['role_desc']} (môn {agent_info['domain']}).",
        f"Loại câu hỏi cần sinh: {kind}. Mức độ: {difficulty}.",
        "Các câu đã có trong ngân hàng của chủ đề này (không được trùng ý tưởng):",
        "\n".join(f"- {t}" for t in titles) or "- (chưa có)",
        "Câu mẫu viết tay của chủ đề, chỉ để tham khảo định dạng và độ khó (JSON):",
        json.dumps(examples, ensure_ascii=False, indent=1),
    ]
    if feedback:
        parts.append(
            "Lần sinh trước đã bị bộ kiểm chứng độc lập loại với lý do dưới đây. "
            "Hãy sinh một câu hỏi khác, tránh lỗi này:\n" + feedback
        )
    return "\n\n".join(parts)


def _build_solver_prompt(stem_symbolic: str, params: List[Dict[str, Any]]) -> str:
    sig = ", ".join(p["name"] for p in params)
    ranges = "; ".join(f"{p['name']} nguyên trong [{p['min']}, {p['max']}]" for p in params)
    return (
        f"Đề bài:\n{stem_symbolic}\n\n"
        f"Tham số: {ranges}.\n"
        f"Viết hàm `def solve({sig}):` trả về đáp số của đề bài."
    )


def _check_schema(data: Any, schema: Dict[str, Any], path: str = "$") -> None:
    """Kiểm tra JSON theo schema (tập con dùng ở file này), vì chế độ json_object không ép schema."""
    t = schema.get("type")
    if t == "object":
        if not isinstance(data, dict):
            raise ValueError(f"{path} phải là object")
        missing = [k for k in schema.get("required", []) if k not in data]
        if missing:
            raise ValueError(f"{path} thiếu trường {missing}")
        for k, sub in schema.get("properties", {}).items():
            if k in data:
                _check_schema(data[k], sub, f"{path}.{k}")
    elif t == "array":
        if not isinstance(data, list):
            raise ValueError(f"{path} phải là mảng")
        for i, item in enumerate(data):
            _check_schema(item, schema["items"], f"{path}[{i}]")
    elif t == "string":
        if not isinstance(data, str):
            raise ValueError(f"{path} phải là chuỗi")
        if "enum" in schema and data not in schema["enum"]:
            raise ValueError(f"{path} phải thuộc {schema['enum']}")
    elif t == "integer":
        if isinstance(data, bool) or not (isinstance(data, int) or (isinstance(data, float) and data.is_integer())):
            raise ValueError(f"{path} phải là số nguyên")


def _coerce_ints(data: Any, schema: Dict[str, Any]) -> Any:
    """Một số model trả 3.0 thay cho 3; đưa về int theo schema."""
    t = schema.get("type")
    if t == "object" and isinstance(data, dict):
        return {k: _coerce_ints(v, schema.get("properties", {}).get(k, {})) for k, v in data.items()}
    if t == "array" and isinstance(data, list):
        return [_coerce_ints(v, schema["items"]) for v in data]
    if t == "integer" and isinstance(data, float):
        return int(data)
    return data


_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL)


def _extract_json(text: str) -> Any:
    text = _THINK_BLOCK.sub("", text or "").strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Phản hồi không chứa đối tượng JSON")
    return json.loads(text[start:end + 1])


def _call_qwen(system: str, user: str, schema: Dict[str, Any], model: str) -> Dict[str, Any]:
    client = _get_client()
    system_full = (
        system
        + "\n\nĐịnh dạng đầu ra: chỉ trả về MỘT đối tượng JSON hợp lệ (không Markdown, không giải thích thêm) "
        "đúng theo JSON Schema sau:\n" + json.dumps(schema, ensure_ascii=False)
    )
    if QWEN_JSON_MODE == "json_schema":
        response_format = {"type": "json_schema", "json_schema": {"name": "output", "schema": schema, "strict": True}}
    else:
        response_format = {"type": "json_object"}
    messages = [{"role": "system", "content": system_full}, {"role": "user", "content": user}]

    last_error = ""
    for _ in range(2):
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format=response_format,
            max_tokens=QWEN_MAX_TOKENS,
            extra_body=QWEN_EXTRA_BODY or None,
        )
        choice = resp.choices[0]
        if choice.finish_reason == "length":
            raise RuntimeError("Phản hồi bị cắt do vượt max_tokens (tăng MATH_LLM_MAX_TOKENS)")
        content = choice.message.content or ""
        try:
            data = _coerce_ints(_extract_json(content), schema)
            _check_schema(data, schema)
            return data
        except Exception as exc:
            # Cho model một lần sửa định dạng
            last_error = str(exc)
            messages = messages + [
                {"role": "assistant", "content": content},
                {"role": "user", "content": f"Đầu ra chưa đúng định dạng: {last_error}. Hãy trả lại đúng một đối tượng JSON theo schema."},
            ]
    raise RuntimeError(f"Model không trả JSON đúng schema: {last_error}")


def _call_claude_cli(system: str, user: str, schema: Dict[str, Any], model: str,
                     effort: Optional[str] = None) -> Dict[str, Any]:
    """Một lượt `claude -p` không công cụ, không lưu phiên, không nạp cấu hình người dùng/dự án;
    đầu ra ép theo JSON Schema (--json-schema)."""
    cmd = [
        _find_claude_cli(), "-p",
        "--model", model,
        "--effort", effort or LLM_EFFORT,
        "--output-format", "json",
        "--tools", "",
        "--no-session-persistence",
        "--setting-sources", "",
        "--strict-mcp-config",
        "--system-prompt", system,
        "--json-schema", json.dumps(schema, ensure_ascii=False),
    ]
    with _claude_cli_slots:
        # Chạy trong thư mục tạm để CLI không đọc CLAUDE.md hay tệp của dự án
        proc = subprocess.run(cmd, input=user, capture_output=True, text=True, encoding="utf-8", errors="replace",
                              timeout=CLAUDE_CLI_TIMEOUT_SEC, cwd=tempfile.gettempdir(), env=_claude_cli_env())
    try:
        out = json.loads(proc.stdout)
    except Exception:
        raise RuntimeError(f"claude CLI lỗi (mã {proc.returncode}): {(proc.stderr or proc.stdout or '').strip()[-600:]}")
    if out.get("is_error") or out.get("subtype") != "success":
        raise RuntimeError(f"claude CLI lỗi ({out.get('subtype')}): {str(out.get('result', ''))[-600:]}")
    data = out.get("structured_output")
    if data is None:
        data = _extract_json(out.get("result", ""))
    data = _coerce_ints(data, schema)
    _check_schema(data, schema)
    return data


def _call_structured(system: str, user: str, schema: Dict[str, Any], model: Optional[str] = None,
                     effort: Optional[str] = None) -> Dict[str, Any]:
    """Một lượt gọi LLM trả JSON theo schema. effort: mức suy nghĩ riêng cho lượt này (Claude), mặc định LLM_EFFORT."""
    model = model or LLM_MODEL
    if LLM_PROVIDER == "claude-cli":
        return _call_claude_cli(system, user, schema, model, effort)
    if LLM_PROVIDER != "anthropic":
        return _call_qwen(system, user, schema, model)
    client = _get_client()
    with client.beta.messages.stream(
        model=model,
        max_tokens=LLM_MAX_TOKENS,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        thinking={"type": "adaptive"},
        output_config={"effort": effort or LLM_EFFORT, "format": {"type": "json_schema", "schema": schema}},
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        message = stream.get_final_message()

    if message.stop_reason == "refusal":
        detail = message.stop_details.explanation if message.stop_details else ""
        raise RuntimeError(f"Claude từ chối yêu cầu: {detail}")
    if message.stop_reason == "max_tokens":
        raise RuntimeError("Phản hồi bị cắt do vượt max_tokens")
    text = next((b.text for b in message.content if b.type == "text"), "")
    return json.loads(text)


# =============================================================================
# Kiểm tra dữ liệu do LLM sinh
# =============================================================================

_FORMULA_CHARS = re.compile(r"^[0-9A-Za-z_+\-*/().,\s]+$")
_IDENT = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


def _check_formula(expr: str, param_names: List[str]) -> sp.Expr:
    """Chỉ chấp nhận biểu thức SymPy an toàn: ký tự cho phép, tên hàm trong danh sách trắng, biến là tham số."""
    if not expr or not _FORMULA_CHARS.match(expr):
        raise ValueError(f"Công thức chứa ký tự không hợp lệ: {expr!r}")
    allowed = set(SAFE_SYMPY_LOCALS) | set(param_names)
    unknown = {tok for tok in _IDENT.findall(expr) if tok not in allowed}
    if unknown:
        raise ValueError(f"Công thức dùng tên không cho phép {sorted(unknown)}: {expr!r}")
    syms = {n: sp.Symbol(n, real=True) for n in param_names}
    parsed = parse_sympy_expr(expr, syms)
    extra = {str(s) for s in parsed.free_symbols} - set(param_names)
    if extra:
        raise ValueError(f"Công thức chứa biến lạ {sorted(extra)}: {expr!r}")
    return parsed


_ALLOWED_IMPORTS = {"sympy", "math", "fractions", "itertools", "functools"}
_BANNED_NAMES = {
    "open", "exec", "eval", "compile", "__import__", "globals", "locals", "vars", "getattr",
    "setattr", "delattr", "input", "breakpoint", "exit", "quit", "help", "memoryview",
}


def _check_solver_code(code: str) -> None:
    """Rào chắn tĩnh cho mã do LLM viết trước khi chạy ở tiến trình con (không thay thế sandbox thật)."""
    tree = ast.parse(code)
    has_solve = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] not in _ALLOWED_IMPORTS:
                    raise ValueError(f"Bộ giải import module không cho phép: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in _ALLOWED_IMPORTS:
                raise ValueError(f"Bộ giải import module không cho phép: {node.module}")
        elif isinstance(node, ast.Name) and node.id in _BANNED_NAMES:
            raise ValueError(f"Bộ giải dùng tên bị cấm: {node.id}")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise ValueError(f"Bộ giải truy cập thuộc tính bị cấm: {node.attr}")
        elif isinstance(node, ast.FunctionDef) and node.name == "solve":
            has_solve = True
    if not has_solve:
        raise ValueError("Bộ giải không định nghĩa hàm solve(...)")


def _validate_generated(gen: Dict[str, Any], question_type: str) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    params = gen["parameters"]
    if not 1 <= len(params) <= 2:
        raise ValueError("Cần 1 hoặc 2 tham số")
    names = [p["name"] for p in params]
    if len(set(names)) != len(names) or not set(names) <= ALLOWED_PARAM_NAMES:
        raise ValueError(f"Tên tham số không hợp lệ: {names}")
    grid_size = 1
    for p in params:
        if not p["min"] < p["max"] or p["max"] - p["min"] > 12:
            raise ValueError(f"Miền tham số {p['name']} không hợp lệ: [{p['min']}, {p['max']}]")
        grid_size *= p["max"] - p["min"] + 1
    if grid_size > MAX_GRID_POINTS:
        raise ValueError(f"Lưới tham số quá lớn ({grid_size} điểm)")

    solution = (gen.get("solution_markdown") or "").strip()
    if len(solution) < 120 or solution.lower().strip(".… ") in {"placeholder", "todo", "tbd", "lời giải", "solution"}:
        raise ValueError("Lời giải trống hoặc chỉ là chữ giữ chỗ; phải viết lời giải chi tiết từng bước (Markdown + LaTeX)")
    if not [r for r in gen.get("rubric_points", []) if str(r).strip()]:
        raise ValueError("Thiếu thang điểm (rubric_points)")

    answer = _check_formula(gen["answer_formula"], names)
    formulas: Dict[str, str] = {}
    if question_type == "mcq":
        opts = gen["options"]
        if len(opts) != 4:
            raise ValueError(f"Câu trắc nghiệm cần đúng 4 phương án, nhận {len(opts)}")
        if not 0 <= gen["correct_index"] <= 3:
            raise ValueError(f"correct_index không hợp lệ: {gen['correct_index']}")
        for i, o in enumerate(opts):
            _check_formula(o["formula"], names)
            formulas["ABCD"[i]] = o["formula"]
        correct_expr = _check_formula(opts[gen["correct_index"]]["formula"], names)
        if sp.simplify(correct_expr - answer) != 0:
            raise ValueError("Công thức phương án đúng khác answer_formula")
    else:
        formulas["__target__"] = gen["answer_formula"]
    return params, formulas


# =============================================================================
# Chạy bộ giải độc lập trên lưới tham số
# =============================================================================

_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
# Kiểm chứng tự động cho câu hỏi do LLM sinh: {code}
# Hàm solve() do một lượt gọi LLM độc lập viết, chỉ nhìn thấy đề bài (không thấy đáp án),
# tính trực tiếp bằng SymPy rồi đối chiếu với công thức đáp án lưu trong ngân hàng câu hỏi.
import json
import math
import sympy as sp

# ===================== BỘ GIẢI ĐỘC LẬP =====================
{solver}
# ===================== ĐỐI CHIẾU =====================
PARAM_NAMES = {names}
GRID = {grid}
FORMULAS = {formulas}
CORRECT = {correct}
STRICT = {strict}

_L = {{n: getattr(sp, n) for n in ("pi", "E", "oo", "sqrt", "sin", "cos", "tan", "cot", "asin", "acos",
                                   "atan", "exp", "log", "Rational", "factorial", "binomial", "Abs")}}
_L.update({{"e": sp.E, "ln": sp.log, "abs": sp.Abs}})
SYMS = {{n: sp.Symbol(n, real=True) for n in PARAM_NAMES}}


def to_real(v):
    c = complex(sp.N(sp.sympify(v), 30))
    if abs(c.imag) > 1e-9 * max(1.0, abs(c.real)) or not math.isfinite(c.real):
        raise ValueError(f"giá trị không phải số thực hữu hạn: {{v}}")
    return c.real


def close(a, b):
    return abs(a - b) <= 1e-7 * max(1.0, abs(a), abs(b))


report = []
for point in GRID:
    row = {{"point": point, "values": {{}}}}
    try:
        row["solver"] = to_real(solve(**point))
    except Exception as exc:
        row["solver_error"] = f"{{type(exc).__name__}}: {{exc}}"
    sub = {{SYMS[n]: sp.Integer(point[n]) for n in PARAM_NAMES}}
    for key, f in FORMULAS.items():
        try:
            row["values"][key] = to_real(sp.sympify(f, locals={{**_L, **SYMS}}).subs(sub))
        except Exception:
            row["values"][key] = None
    report.append(row)

print("REPORT_JSON:" + json.dumps(report))

if STRICT:
    for row in report:
        p, s, v = row["point"], row.get("solver"), row["values"]
        assert s is not None, f"Bộ giải lỗi tại {{p}}: {{row.get('solver_error')}}"
        assert v[CORRECT] is not None and close(v[CORRECT], s), f"Đáp án sai tại {{p}}: công thức={{v[CORRECT]}}, bộ giải={{s}}"
        keys = [k for k in v if k != "__target__"]
        for k in keys:
            if k != CORRECT:
                assert v[k] is not None and not close(v[k], s), f"Phương án {{k}} trùng đáp án tại {{p}}"
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                assert not close(v[keys[i]], v[keys[j]]), f"Phương án {{keys[i]}} và {{keys[j]}} trùng nhau tại {{p}}"
    print(f"VERIFIED_OK: {code} ({{len(report)}} điểm tham số khớp bộ giải độc lập)")
'''


def _build_check_script(code: str, solver: str, names: List[str], grid: List[Dict[str, int]],
                        formulas: Dict[str, str], correct: str, strict: bool) -> str:
    return _SCRIPT_TEMPLATE.format(
        code=code,
        solver=solver.strip(),
        names=repr(names),
        grid=repr(grid),
        formulas=repr(formulas),
        correct=repr(correct),
        strict=repr(strict),
    )


def _run_probe(script: str) -> List[Dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix="llm_probe_") as tmp:
        path = os.path.join(tmp, "probe.py")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(script)
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
            env.pop(k, None)
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=SOLVER_TIMEOUT_SEC, cwd=tmp, env=env,
        )
    lines = [ln for ln in (proc.stdout or "").splitlines() if ln.startswith("REPORT_JSON:")]
    if proc.returncode != 0 or not lines:
        raise RuntimeError(f"Bộ giải không chạy được: {(proc.stderr or proc.stdout or '').strip()[-800:]}")
    return json.loads(lines[-1][len("REPORT_JSON:"):])


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= 1e-7 * max(1.0, abs(a), abs(b))


def _analyze(report: List[Dict[str, Any]], correct: str) -> Tuple[List[Dict[str, int]], List[str], List[str]]:
    """Trả về (điểm hợp lệ, lý do loại điểm, lỗi sai đáp án)."""
    valid, dropped, mismatches = [], [], []
    for row in report:
        p, s, v = row["point"], row.get("solver"), row["values"]
        if s is None:
            dropped.append(f"{p}: bộ giải lỗi ({row.get('solver_error')})")
            continue
        if v.get(correct) is None:
            dropped.append(f"{p}: công thức đáp án không xác định")
            continue
        if not _close(v[correct], s):
            mismatches.append(f"{p}: công thức đáp án = {v[correct]:.10g}, bộ giải độc lập = {s:.10g}")
            continue
        keys = [k for k in v if k != "__target__"]
        others = [k for k in keys if k != correct]
        if any(v[k] is None or _close(v[k], s) for k in others):
            dropped.append(f"{p}: có phương án nhiễu trùng đáp án")
            continue
        if any(_close(v[a], v[b]) for a, b in itertools.combinations(keys, 2)):
            dropped.append(f"{p}: hai phương án trùng nhau")
            continue
        valid.append(p)
    return valid, dropped, mismatches


# =============================================================================
# Sinh một câu hỏi (vòng sinh → giải độc lập → đối chiếu → sửa lại)
# =============================================================================


def _new_code(agent_info: Dict[str, Any], examples_codes: List[str]) -> str:
    prefix = examples_codes[0].rsplit("-", 1)[0] if examples_codes else agent_info["agent_code"]
    return f"{prefix}-AI-{datetime.now().strftime('%y%m%d%H%M%S')}-{secrets.token_hex(2).upper()}"


def _shuffle_options(gen: Dict[str, Any], rng: random.Random) -> Tuple[List[Dict[str, str]], int]:
    order = list(range(4))
    rng.shuffle(order)
    opts = [gen["options"][i] for i in order]
    return opts, order.index(gen["correct_index"])


def _attempt_once(agent_info: Dict[str, Any], question_type: str, difficulty: str,
                  feedback: Optional[str], db_path: str, rng: random.Random) -> Dict[str, Any]:
    handwritten = load_agent_questions(agent_info)
    examples = _agent_examples(agent_info, db_path)
    titles = _existing_titles(agent_info["agent_id"], db_path)

    gen = _call_structured(
        GENERATOR_SYSTEM,
        _build_generator_prompt(agent_info, question_type, difficulty, examples, titles, feedback),
        GENERATOR_SCHEMA,
    )
    code = _new_code(agent_info, [q["code"] for q in handwritten])
    result: Dict[str, Any] = {"code": code, "title": gen.get("title", ""), "question_type": question_type}

    try:
        params, _ = _validate_generated(gen, question_type)
    except Exception as exc:
        return {**result, "status": "REJECTED", "reason": f"Dữ liệu sinh ra không hợp lệ: {exc}"}

    if question_type == "mcq":
        options, correct_index = _shuffle_options(gen, rng)
        formulas = {"ABCD"[i]: o["formula"] for i, o in enumerate(options)}
        correct = "ABCD"[correct_index]
    else:
        options, formulas, correct = [], {"__target__": gen["answer_formula"]}, "__target__"

    solver = _call_structured(SOLVER_SYSTEM, _build_solver_prompt(gen["stem_symbolic"], params), SOLVER_SCHEMA)
    solver_code = solver["solver_code"]
    try:
        _check_solver_code(solver_code)
    except Exception as exc:
        return {**result, "status": "REJECTED", "reason": f"Mã bộ giải không an toàn: {exc}"}

    names = [p["name"] for p in params]
    grid = [dict(zip(names, vals)) for vals in itertools.product(*[range(p["min"], p["max"] + 1) for p in params])]
    try:
        report = _run_probe(_build_check_script(code, solver_code, names, grid, formulas, correct, strict=False))
    except Exception as exc:
        return {**result, "status": "REJECTED", "reason": str(exc)}

    valid, dropped, mismatches = _analyze(report, correct)
    if mismatches:
        return {**result, "status": "REJECTED",
                "reason": "Đáp án không khớp bộ giải độc lập tại " + "; ".join(mismatches[:4])}
    if len(valid) < MIN_VALID_POINTS:
        return {**result, "status": "REJECTED",
                "reason": f"Chỉ {len(valid)} giá trị tham số hợp lệ. " + "; ".join(dropped[:4])}
    if dropped and len(params) > 1:
        return {**result, "status": "REJECTED",
                "reason": "Có tổ hợp tham số không hợp lệ (câu 2 tham số phải hợp lệ trên toàn lưới): " + "; ".join(dropped[:4])}

    valid_values = {v[names[0]] for v in valid}
    schema = []
    for p in params:
        forbidden = sorted(set(range(p["min"], p["max"] + 1)) - valid_values) if len(params) == 1 else []
        default = p["default"] if p["default"] not in forbidden and p["min"] <= p["default"] <= p["max"] else min(valid_values)
        schema.append({
            "name": p["name"], "symbol": p["name"], "label": p["label"],
            "min": p["min"], "max": p["max"], "step": 1, "default": default, "forbidden": forbidden,
        })

    final_script = _build_check_script(code, solver_code, names, valid, formulas, correct, strict=True)
    py_res = verify_python_code(code, final_script, timeout_sec=SOLVER_TIMEOUT_SEC)
    if py_res["status"] != "VERIFIED_PASS":
        return {**result, "status": "REJECTED", "reason": f"Script kiểm chứng cuối thất bại: {py_res['output'][-600:]}"}

    now_note = f"-- {code}: câu hỏi do LLM ({LLM_MODEL}) sinh.\n-- Không có chứng minh Lean; xem script Python kiểm chứng bằng bộ giải độc lập.\n"
    question = {
        "code": code,
        "agent_id": agent_info["agent_id"],
        "agent_name": agent_info["agent_name"],
        "subject": agent_info["domain"],
        "topic": handwritten[0]["topic"] if handwritten else agent_info["role_desc"],
        "question_type": question_type,
        "difficulty": gen["difficulty"],
        "has_parameters": True,
        "parameters_schema": schema,
        "title": gen["title"],
        "stem_symbolic": gen["stem_symbolic"],
        "stem_template": gen["stem_template"],
        "options_symbolic": {"ABCD"[i]: o["latex"] for i, o in enumerate(options)},
        "parametric_formulas": {
            "options": {k: v for k, v in formulas.items() if k != "__target__"},
            "target_expr": gen["answer_formula"],
        },
        "correct_option": correct if question_type == "mcq" else "ESSAY",
        "solution_symbolic": gen["solution_markdown"],
        "rubric_points": gen["rubric_points"],
        "lean4_code": now_note,
        "lean4_status": "NOT_APPLICABLE",
        "lean4_output": "Câu hỏi do LLM sinh: không áp dụng Lean 4.",
        "lean4_elapsed_ms": 0.0,
        "python_code": final_script,
        "python_status": py_res["status"],
        "python_output": py_res["output"],
        "python_elapsed_ms": py_res["elapsed_ms"],
        "aas_score": 1.0,
        "sovereign_verdict": "LLM_VERIFIED",
        "source": "llm",
    }
    # Chưa lưu: generate_one chỉ lưu khi câu cũng đạt formalize Lean (hoặc khi người dùng tắt formalize)
    return {
        **result,
        "question": question,
        "status": "ACCEPTED",
        "valid_points": len(valid),
        "forbidden": schema[0]["forbidden"] if len(schema) == 1 else [],
        "solver_notes": solver.get("notes", ""),
    }


def _formalize_generated(question: Dict[str, Any], db_path: str) -> Dict[str, Any]:
    """Formalize một câu vừa sinh khi câu CHƯA được lưu (persist=False): người gọi chỉ lưu câu khi VERIFIED_PASS."""
    from lean_formalizer import formalize_question

    try:
        r = formalize_question(question["code"], db_path=db_path, question=question, persist=False)
    except Exception as exc:
        return {"status": "ERROR", "attempts": 0, "summary": f"{type(exc).__name__}: {exc}"}
    review = r.get("review") or {}
    # Mệnh đề biên dịch được nhưng giám khảo kết luận bản diễn đạt lại không khớp đề (điều kiện 5 của QT15)
    # => vấn đề nằm ở cách hiểu đề (đề mơ hồ, thiếu giả thiết), không ở chứng minh
    if (r["status"] == "UNCONFIRMED" and r.get("pipeline", {}).get("compiled_total")
            and review.get("faithful") is False and review.get("issues")):
        r["unfaithful_issues"] = review["issues"]
    return r


def generate_one(agent_info: Dict[str, Any], question_type: str, difficulty: str,
                 max_attempts: int = 2, db_path: str = DB_PATH, seed: Optional[int] = None,
                 formalize_lean: bool = False) -> Dict[str, Any]:
    rng = random.Random(seed)
    feedback = None
    history: List[str] = []
    t0 = time.perf_counter()
    res: Dict[str, Any] = {}
    for attempt in range(1, max_attempts + 1):
        try:
            res = _attempt_once(agent_info, question_type, difficulty, feedback, db_path, rng)
        except Exception as exc:
            res = {"code": "", "title": "", "question_type": question_type, "status": "ERROR",
                   "reason": f"{type(exc).__name__}: {exc}"}
        elapsed = round((time.perf_counter() - t0) * 1000.0, 2)
        log_verification(
            question_code=res.get("code") or f"{agent_info['agent_code']}-LLM",
            agent_id=agent_info["agent_id"],
            verifier_type="LLM_GENERATE+INDEPENDENT_SOLVER",
            status="LLM_" + res["status"],
            execution_ms=elapsed,
            output_log=f"Lần {attempt}: {res.get('title', '')}\n{res.get('reason', 'Đạt kiểm chứng độc lập')}",
            merkle_hash="",
            db_path=db_path,
        )
        # Câu chỉ được lưu vào CSDL khi vừa đúng đáp án (bộ giải độc lập) vừa có chứng minh Lean + Mathlib
        # (VERIFIED_PASS). Formalize theo quy trình: chuẩn hóa -> truy xuất -> phân tích -> nhiều ứng viên + đồng thuận.
        if res["status"] == "ACCEPTED":
            question = res.pop("question")
            if formalize_lean:
                lean = _formalize_generated(question, db_path)
                res["lean_mathlib"] = {k: lean[k] for k in ("status", "attempts", "summary")}
                if lean["status"] == "VERIFIED_PASS":
                    upsert_question(question, db_path=db_path)
                    update_mathlib_result(question["code"], lean_code=lean["lean_code"], status=lean["status"],
                                          output=lean["output"], review=lean["review"].get("issues", ""), db_path=db_path)
                elif lean["status"] == "ERROR":
                    res = {**res, "status": "ERROR", "reason": f"Lỗi khi formalize: {lean['summary']}"}
                elif lean["status"] == "DISPROVED":  # 6b: Lean chứng minh được đáp án sai -> loại câu, sinh câu thay thế
                    res = {**res, "status": "REJECTED",
                           "reason": f"Lean chứng minh được đáp án SAI ({lean['summary'][:300]}). Hãy sinh câu khác và "
                                     f"tính lại đáp án cẩn thận."}
                elif lean.get("unfaithful_issues"):  # giám khảo: bản diễn đạt lại của mệnh đề không khớp đề
                    res = {**res, "status": "REJECTED",
                           "reason": f"Khi formalize, giám khảo cho rằng đề mơ hồ hoặc thiếu giả thiết: "
                                     f"{lean['unfaithful_issues']}. Hãy viết lại đề rõ ràng, đủ giả thiết."}
                else:
                    # FAILED (mệnh đề đã xác nhận nhưng không chứng minh được) hoặc UNCONFIRMED (không mệnh đề nào đạt
                    # đủ năm điều kiện): hủy lượt sinh của agent này, không sinh câu mới
                    res = {**res, "status": "ABANDONED", "reason": f"Hủy ({lean['status']}): {lean['summary'][:400]}"}
                log_verification(
                    question_code=question["code"], agent_id=agent_info["agent_id"],
                    verifier_type="LLM_GENERATE+LEAN_FORMALIZE", status="LLM_" + res["status"],
                    execution_ms=round((time.perf_counter() - t0) * 1000.0, 2),
                    output_log=f"Lần {attempt}: {res.get('reason', lean['summary'])}", merkle_hash="", db_path=db_path,
                )
            else:
                # Người dùng tắt formalize: lưu câu chỉ đạt chuẩn tính toán (lean4_mathlib_status = NOT_RUN)
                upsert_question(question, db_path=db_path)
        if res["status"] == "ACCEPTED":
            break
        history.append(f"Lần {attempt}: {res.get('reason', '')}")
        if res["status"] in ("ERROR", "ABANDONED"):
            break
        feedback = res.get("reason")

    res["attempts"] = attempt
    res["history"] = history
    res["agent_id"] = agent_info["agent_id"]
    res["agent_name"] = agent_info["agent_name"]
    res["elapsed_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)
    return res


def generate_questions(
    agent_ids: Optional[List[int]] = None,
    count_per_agent: int = 1,
    question_type: str = "mixed",
    difficulty: str = "Vận dụng",
    max_attempts: int = 2,
    db_path: str = DB_PATH,
    formalize_lean: bool = False,
) -> Dict[str, Any]:
    """Chạy song song: mỗi agent được chọn sinh `count_per_agent` câu theo chủ đề của mình."""
    agents = [a for a in AGENTS_REGISTRY if not agent_ids or a["agent_id"] in agent_ids]
    jobs = []
    for a in agents:
        for i in range(count_per_agent):
            qtype = question_type if question_type in ("mcq", "essay") else ("mcq" if i % 3 != 2 else "essay")
            jobs.append((a, qtype))

    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(20, max(1, len(jobs)))) as ex:
        results = list(ex.map(
            lambda j: generate_one(j[0], j[1], difficulty, max_attempts, db_path, formalize_lean=formalize_lean), jobs
        ))
    wall_ms = round((time.perf_counter() - t0) * 1000.0, 2)

    accepted = [r for r in results if r["status"] == "ACCEPTED"]
    if accepted:
        commit_merkle_node(
            node_type="LLM_QUESTIONS_GENERATED",
            parent_hashes=[],
            payload={
                "model": LLM_MODEL,
                "requested": len(jobs),
                "accepted_codes": [r["code"] for r in accepted],
                "rejected": len(results) - len(accepted),
            },
        )
    return {
        "model": LLM_MODEL,
        "requested": len(jobs),
        "accepted": len(accepted),
        "rejected": len(results) - len(accepted),
        "wall_clock_ms": wall_ms,
        "results": results,
    }
