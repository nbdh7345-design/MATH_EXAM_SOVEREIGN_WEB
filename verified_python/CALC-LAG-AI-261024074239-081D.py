# -*- coding: utf-8 -*-
# Kiểm chứng tự động cho câu hỏi do LLM sinh: CALC-LAG-AI-261024074239-081D
# Hàm solve() do một lượt gọi LLM độc lập viết, chỉ nhìn thấy đề bài (không thấy đáp án),
# tính trực tiếp bằng SymPy rồi đối chiếu với công thức đáp án lưu trong ngân hàng câu hỏi.
import json
import math
import sympy as sp

# ===================== BỘ GIẢI ĐỘC LẬP =====================
import sympy as sp

def solve(m):
    x = sp.symbols('x', positive=True)
    m_ = sp.Integer(m)
    # Thay y = m/x vào f: g(x) = x + 4m/x, với x > 0
    g = x + 4 * m_ / x
    # Điểm tới hạn: g'(x) = 0
    crit = sp.solve(sp.diff(g, x), x)
    crit = [c for c in crit if c.is_positive]
    # Kiểm tra đây là cực tiểu (đạo hàm cấp 2 > 0) và lấy giá trị nhỏ nhất
    vals = []
    for c in crit:
        if sp.simplify(sp.diff(g, x, 2).subs(x, c)) > 0:
            vals.append(sp.simplify(g.subs(x, c)))
    # Giới hạn tại biên (x -> 0+ và x -> +inf) đều bằng +inf nên min là giá trị cực tiểu
    return sp.nsimplify(sp.simplify(min(vals, key=lambda v: float(v))))
# ===================== ĐỐI CHIẾU =====================
PARAM_NAMES = ['m']
GRID = [{'m': 2}, {'m': 3}, {'m': 4}, {'m': 5}, {'m': 6}, {'m': 7}, {'m': 8}, {'m': 9}]
FORMULAS = {'A': '4*sqrt(m)', 'B': '2*sqrt(m)', 'C': '8*sqrt(m)', 'D': '4*m**2'}
CORRECT = 'A'
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
    print(f"VERIFIED_OK: CALC-LAG-AI-261024074239-081D ({len(report)} điểm tham số khớp bộ giải độc lập)")
