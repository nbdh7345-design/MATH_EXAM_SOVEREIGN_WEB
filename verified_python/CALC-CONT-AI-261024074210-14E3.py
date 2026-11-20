# -*- coding: utf-8 -*-
# Kiểm chứng tự động cho câu hỏi do LLM sinh: CALC-CONT-AI-261024074210-14E3
# Hàm solve() do một lượt gọi LLM độc lập viết, chỉ nhìn thấy đề bài (không thấy đáp án),
# tính trực tiếp bằng SymPy rồi đối chiếu với công thức đáp án lưu trong ngân hàng câu hỏi.
import json
import math
import sympy as sp

# ===================== BỘ GIẢI ĐỘC LẬP =====================
import sympy as sp

def solve(m):
    x = sp.symbols('x', positive=True)
    M = sp.Integer(m)
    # Lấy log của biểu thức: (1/x) * ln((m^x + (m+1)^x)/2)
    expr = sp.log((M**x + (M + 1)**x) / 2) / x
    L = sp.limit(expr, x, 0)
    # Giới hạn gốc = exp(L)
    result = sp.simplify(sp.exp(L))
    return result
# ===================== ĐỐI CHIẾU =====================
PARAM_NAMES = ['m']
GRID = [{'m': 2}, {'m': 3}, {'m': 4}, {'m': 5}, {'m': 6}, {'m': 7}, {'m': 8}, {'m': 9}]
FORMULAS = {'A': '(2*m+1)/2', 'B': 'sqrt(m*(m+1))', 'C': 'm*(m+1)/2', 'D': '1/sqrt(m*(m+1))'}
CORRECT = 'B'
STRICT = True

_L = {n: getattr(sp, n) for n in ("pi", "E", "oo", "sqrt", "sin", "cos", "tan", "cot", "asin", "acos",
                                   "atan", "exp", "log", "Rational", "factorial", "binomial", "Abs")}
_L.update({"e": sp.E, "ln": sp.log, "abs": sp.Abs})
SYMS = {n: sp.Symbol(n, real=True) for n in PARAM_NAMES}


def to_real(v):
    c = complex(sp.N(sp.sympify(v), 30))
    if abs(c.imag) > 1e-9 * max(1.0, abs(c.real)) or not math.isfinite(c.real):
        raise ValueError(f"giá trị không phải số thực hữu hạn: {v}")
    return c.real


def close(a, b):
    return abs(a - b) <= 1e-7 * max(1.0, abs(a), abs(b))


report = []
for point in GRID:
    row = {"point": point, "values": {}}
    try:
        row["solver"] = to_real(solve(**point))
    except Exception as exc:
        row["solver_error"] = f"{type(exc).__name__}: {exc}"
    sub = {SYMS[n]: sp.Integer(point[n]) for n in PARAM_NAMES}
    for key, f in FORMULAS.items():
        try:
            row["values"][key] = to_real(sp.sympify(f, locals={**_L, **SYMS}).subs(sub))
        except Exception:
            row["values"][key] = None
    report.append(row)

print("REPORT_JSON:" + json.dumps(report))

if STRICT:
    for row in report:
        p, s, v = row["point"], row.get("solver"), row["values"]
        assert s is not None, f"Bộ giải lỗi tại {p}: {row.get('solver_error')}"
        assert v[CORRECT] is not None and close(v[CORRECT], s), f"Đáp án sai tại {p}: công thức={v[CORRECT]}, bộ giải={s}"
        keys = [k for k in v if k != "__target__"]
        for k in keys:
            if k != CORRECT:
                assert v[k] is not None and not close(v[k], s), f"Phương án {k} trùng đáp án tại {p}"
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                assert not close(v[keys[i]], v[keys[j]]), f"Phương án {keys[i]} và {keys[j]} trùng nhau tại {p}"
    print(f"VERIFIED_OK: CALC-CONT-AI-261024074210-14E3 ({len(report)} điểm tham số khớp bộ giải độc lập)")
