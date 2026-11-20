# -*- coding: utf-8 -*-
"""
parametric_engine.py - Động cơ Tính Toán & Biến Thiên Tham Số Động (Symbolic & Numerical Parameter Engine)
Hỗ trợ:
1. Biểu diễn câu hỏi trắc nghiệm và tự luận chứa tham số ký hiệu (m, a, b, alpha, k...).
2. Tính toán tự động giá trị chính xác (Exact Symbolic/Rational/Radical LaTeX qua SymPy) và xấp xỉ số học
   của đề bài, 4 phương án A, B, C, D và lời giải khi người dùng nhập bất kỳ bộ tham số nào.
3. Sinh ngẫu nhiên bộ tham số mới đảm bảo điều kiện miền xác định và 4 phương án A, B, C, D đôi một phân biệt.
"""

import json
import math
import random
import re
from typing import Any, Dict, List, Optional, Tuple
import sympy as sp


SAFE_SYMPY_LOCALS = {
    "pi": sp.pi,
    "E": sp.E,
    "e": sp.E,
    "oo": sp.oo,
    "sqrt": sp.sqrt,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "cot": sp.cot,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "exp": sp.exp,
    "ln": sp.log,
    "log": sp.log,
    "Rational": sp.Rational,
    "factorial": sp.factorial,
    "binomial": sp.binomial,
    "Abs": sp.Abs,
    "abs": sp.Abs,
}


def parse_sympy_expr(expr_str: str, param_symbols: Dict[str, sp.Symbol]) -> sp.Expr:
    local_dict = dict(SAFE_SYMPY_LOCALS)
    local_dict.update(param_symbols)
    return sp.sympify(expr_str, locals=local_dict)


def format_sympy_latex(val: sp.Expr) -> str:
    try:
        simplified = sp.simplify(val)
        return sp.latex(simplified)
    except Exception:
        return str(val)


def _normalize_schema(schema: Any) -> List[Dict[str, Any]]:
    if isinstance(schema, str):
        try:
            schema = json.loads(schema)
        except Exception:
            schema = []
    if isinstance(schema, dict):
        out = []
        for k, v in schema.items():
            if isinstance(v, dict):
                item = dict(v)
                item.setdefault("name", k)
                item.setdefault("symbol", k)
                out.append(item)
        return out
    if isinstance(schema, list):
        return [x for x in schema if isinstance(x, dict)]
    return []


_MATH_SEGMENT = re.compile(r"(\$\$.*?\$\$|\$[^$]+?\$)", re.DOTALL)
_TEXT_CMD = re.compile(r"\\(?:text|mathrm|operatorname|textbf|mbox)\s*\{[^{}]*\}")
_LATEX_TOKEN = re.compile(r"\\[A-Za-z]+|[A-Za-z]")


def substitute_params_latex(text: str, values: Dict[str, Any]) -> str:
    """Thay giá trị tham số vào các công thức toán ($...$, $$...$$) của một đoạn văn bản LaTeX/Markdown.
    Chỉ thay chữ cái đứng riêng là tên tham số (không đụng lệnh LaTeX, \\text{...}, chữ ngoài công thức); thêm dấu nhân
    khi đứng sau số/chữ (2m -> 2 \\cdot 5), bọc ngoặc nhọn sau ^ hoặc _ (u^m -> u^{12}), bọc ngoặc tròn khi âm.
    Bỏ qua tham số trùng tên biến chạy (\\sum_{k=...}, dk) để không thay nhầm."""
    names = {}
    for n, v in values.items():
        if len(n) != 1 or re.search(r"\\(?:sum|prod)_\{?\s*" + n + r"\s*=|\bd" + n + r"\b", text):
            continue
        names[n] = v

    if not names:
        return text

    def fix_math(seg: str) -> str:
        kept: List[str] = []
        seg = _TEXT_CMD.sub(lambda m: kept.append(m.group(0)) or f"\x00{len(kept) - 1}\x00", seg)
        out, last = [], 0
        for m in _LATEX_TOKEN.finditer(seg):
            tok = m.group(0)
            if tok not in names:
                continue
            v = names[tok]
            val = f"({v})" if isinstance(v, (int, float)) and v < 0 else str(v)
            prev = seg[m.start() - 1] if m.start() > 0 else ""
            if prev in "^_":
                val = "{" + val + "}"
            elif prev.isalnum():
                val = r" \cdot " + val
            out += [seg[last:m.start()], val]
            last = m.end()
        out.append(seg[last:])
        seg = "".join(out)
        return re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], seg)

    return _MATH_SEGMENT.sub(lambda m: fix_math(m.group(0)), text)


def evaluate_question_with_params(
    question: Dict[str, Any],
    custom_params: Optional[Dict[str, float]] = None,
    mode: str = "dual",  # "symbolic" | "numeric" | "dual"
) -> Dict[str, Any]:
    """
    Tính toán câu hỏi theo bộ tham số `custom_params`.
    - Nếu mode == 'symbolic': Giữ nguyên tham số ký hiệu m, a, b.
    - Nếu mode == 'numeric': Thay giá trị tham số vào đề bài và tính giá trị cụ thể cho 4 đáp án A, B, C, D.
    - Nếu mode == 'dual': Hiển thị cả công thức tổng quát theo tham số VÀ kết quả tính toán ứng với bộ tham số hiện hành.
    """
    schema = _normalize_schema(question.get("parameters_schema", []))

    formulas = question.get("parametric_formulas", {})
    if isinstance(formulas, str):
        try:
            formulas = json.loads(formulas)
        except Exception:
            formulas = {}

    options_sym = question.get("options_symbolic", {})
    if isinstance(options_sym, str):
        try:
            options_sym = json.loads(options_sym)
        except Exception:
            options_sym = {}

    # Xác định giá trị tham số hiện hành
    active_params: Dict[str, Any] = {}
    sym_map: Dict[str, sp.Symbol] = {}
    subs_map: Dict[sp.Symbol, Any] = {}

    for p in schema:
        pname = p.get("name", "m")
        default_val = p.get("default", 2)
        raw_val = default_val
        if custom_params and pname in custom_params and custom_params[pname] is not None:
            raw_val = custom_params[pname]

        # Chuyển về int hoặc Rational nếu nguyên/phân số đẹp
        try:
            fval = float(raw_val)
            if abs(fval - round(fval)) < 1e-9:
                ival = int(round(fval))
                active_params[pname] = ival
                sp_val = sp.Integer(ival)
            else:
                active_params[pname] = round(fval, 4)
                sp_val = sp.nsimplify(fval, rational=True, tolerance=1e-6)
        except Exception:
            active_params[pname] = default_val
            sp_val = sp.Integer(int(default_val))

        sym_obj = sp.Symbol(pname, real=True)
        sym_map[pname] = sym_obj
        subs_map[sym_obj] = sp_val

    # Thay thế vào stem_template & solution_symbolic
    stem_symbolic = question.get("stem_symbolic", "")
    stem_template = question.get("stem_template", stem_symbolic)
    solution_symbolic = question.get("solution_symbolic", "")

    stem_evaluated = stem_template
    for k, v in active_params.items():
        stem_evaluated = stem_evaluated.replace(f"{{{k}}}", str(v))
    # Lời giải được viết tổng quát theo tham số (không có chỗ trống {m} như stem_template; "{m}" trong lời giải chỉ là
    # ngoặc LaTeX): ở chế độ thay số mới thay giá trị tham số vào các công thức của lời giải
    solution_evaluated = substitute_params_latex(solution_symbolic, active_params) if mode == "numeric" else solution_symbolic

    param_summary_latex = ", ".join([f"{ p.get('symbol', p['name']) } = {active_params[p['name']]}" for p in schema])

    # Tính toán giá trị 4 phương án A, B, C, D theo tham số
    evaluated_options: Dict[str, Dict[str, Any]] = {}
    numeric_values: List[float] = []

    option_formulas = formulas.get("options", {}) if isinstance(formulas, dict) else {}
    if not option_formulas and isinstance(formulas, dict):
        # Cho phép truyền trực tiếp {"A": "...", "B": "...", "C": "...", "D": "..."}
        option_formulas = {k: v for k, v in formulas.items() if k in ("A", "B", "C", "D")}

    for opt_key in ("A", "B", "C", "D"):
        sym_text = options_sym.get(opt_key, "")
        expr_str = option_formulas.get(opt_key, "")
        eval_latex = ""
        eval_float: Optional[float] = None
        display_text = sym_text

        if expr_str and sym_map:
            try:
                expr = parse_sympy_expr(str(expr_str), sym_map)
                subbed = sp.simplify(expr.subs(subs_map))
                eval_latex = format_sympy_latex(subbed)
                try:
                    eval_float = float(subbed.evalf())
                    if math.isfinite(eval_float):
                        numeric_values.append(eval_float)
                except Exception:
                    eval_float = None

                if mode == "numeric":
                    unit_suffix = formulas.get("unit_latex", "")
                    prefix_latex = formulas.get("option_prefix_latex", "")
                    display_text = f"${prefix_latex}{eval_latex}{unit_suffix}$"
                elif mode == "dual":
                    display_text = f"{sym_text} $\\quad \\left(\\text{{với }} {param_summary_latex} \\implies {eval_latex}\\right)$"
                else:
                    display_text = sym_text
            except Exception as e:
                eval_latex = f"\\text{{Lỗi tính: {e}}}"

        evaluated_options[opt_key] = {
            "key": opt_key,
            "symbolic": sym_text,
            "formula_expr": expr_str,
            "evaluated_latex": eval_latex,
            "evaluated_float": round(eval_float, 6) if eval_float is not None and math.isfinite(eval_float) else None,
            "display": display_text,
        }

    # Tính giá trị biểu thức kết quả cho cả câu tự luận hoặc câu hỏi có target_expr
    target_evaluated_latex = ""
    target_evaluated_float = None
    target_expr_str = formulas.get("target_expr", "") if isinstance(formulas, dict) else ""
    if not target_expr_str and question.get("correct_option") in option_formulas:
        target_expr_str = option_formulas[question["correct_option"]]

    if target_expr_str and sym_map:
        try:
            t_expr = parse_sympy_expr(str(target_expr_str), sym_map)
            t_subbed = sp.simplify(t_expr.subs(subs_map))
            target_evaluated_latex = format_sympy_latex(t_subbed)
            try:
                f_v = float(t_subbed.evalf())
                if math.isfinite(f_v):
                    target_evaluated_float = round(f_v, 6)
            except Exception:
                pass
        except Exception:
            pass

    if mode == "numeric" and target_evaluated_latex and param_summary_latex:
        solution_evaluated += f"\n\n**Kết luận với ${param_summary_latex}$:** đáp số $= {target_evaluated_latex}$."

    # Kiểm tra tính phân biệt của 4 đáp án tại bộ tham số
    disjoint = True
    if len(numeric_values) == 4:
        for i in range(4):
            for j in range(i + 1, 4):
                if abs(numeric_values[i] - numeric_values[j]) < 1e-7:
                    disjoint = False
                    break

    if mode == "symbolic":
        final_stem = stem_symbolic
    elif mode == "numeric":
        if stem_evaluated != stem_symbolic:
            final_stem = stem_evaluated
        elif param_summary_latex:
            final_stem = f"{stem_symbolic}\n\n**Tính toán với bộ tham số cụ thể:** Cho ${param_summary_latex}$."
        else:
            final_stem = stem_symbolic
    else:  # dual
        if param_summary_latex:
            final_stem = f"{stem_symbolic}\n\n> **Biến thiên tham số hiện hành:** ${param_summary_latex}$"
            if target_evaluated_latex:
                final_stem += f" $\\implies$ Giá trị đáp án chuẩn tại tham số: $\\mathbf{{{target_evaluated_latex}}}$"
        else:
            final_stem = stem_symbolic

    return {
        "question_code": question.get("code"),
        "mode": mode,
        "active_parameters": active_params,
        "param_summary_latex": param_summary_latex,
        "stem_display": final_stem,
        "stem_symbolic": stem_symbolic,
        "stem_evaluated": stem_evaluated,
        "options": evaluated_options,
        "correct_option": question.get("correct_option", "A"),
        "target_evaluated_latex": target_evaluated_latex,
        "target_evaluated_float": target_evaluated_float,
        "disjoint_options": disjoint,
        "solution_display": solution_evaluated,
    }


def sample_valid_parameters(question: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
    """Sinh ngẫu nhiên bộ tham số hợp lệ sao cho 4 phương án A, B, C, D đôi một phân biệt."""
    rng = random.Random(seed)
    schema = _normalize_schema(question.get("parameters_schema", []))

    if not schema:
        return {}

    for _attempt in range(30):
        candidate: Dict[str, Any] = {}
        for p in schema:
            pname = p.get("name", "m")
            pmin = p.get("min", 2)
            pmax = p.get("max", 8)
            pstep = p.get("step", 1)
            forbidden = set(p.get("forbidden", []))
            if isinstance(pstep, int) and pstep >= 1:
                choices = [v for v in range(int(pmin), int(pmax) + 1, int(pstep)) if v not in forbidden]
                candidate[pname] = rng.choice(choices) if choices else p.get("default", 2)
            else:
                val = round(rng.uniform(float(pmin), float(pmax)), 2)
                candidate[pname] = val

        res = evaluate_question_with_params(question, candidate, mode="dual")
        if res.get("disjoint_options", True):
            return candidate

    return {p.get("name", "m"): p.get("default", 2) for p in schema}
