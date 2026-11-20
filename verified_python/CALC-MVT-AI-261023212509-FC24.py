# -*- coding: utf-8 -*-
# Kiểm chứng tự động cho câu hỏi do LLM sinh: CALC-MVT-AI-261023212509-FC24
# Hàm solve() do một lượt gọi LLM độc lập viết, chỉ nhìn thấy đề bài (không thấy đáp án),
# tính trực tiếp bằng SymPy rồi đối chiếu với công thức đáp án lưu trong ngân hàng câu hỏi.
import json
import math
import sympy as sp

# ===================== BỘ GIẢI ĐỘC LẬP =====================
import sympy as sp

def solve(m, k):
    x = sp.symbols('x', real=True)
    f = sp.sqrt(x**2 + 2*m*x + 3)
    a1 = sp.limit(f/x, x, sp.oo)
    b1 = sp.limit(f - a1*x, x, sp.oo)
    a2 = sp.limit(f/x, x, -sp.oo)
    b2 = sp.limit(f - a2*x, x, -sp.oo)
    # intersection of asymptotes
    xi = sp.solve(sp.Eq(a1*x + b1, a2*x + b2), x)[0]
    yi = a1*xi + b1
    P = (xi, yi)
    Q = (k, a1*k + b1)
    R = (k, a2*k + b2)
    area = sp.Abs((Q[0]-P[0])*(R[1]-P[1]) - (R[0]-P[0])*(Q[1]-P[1])) / 2
    return sp.nsimplify(sp.simplify(area))
# ===================== ĐỐI CHIẾU =====================
PARAM_NAMES = ['m', 'k']
GRID = [{'m': 1, 'k': 1}, {'m': 1, 'k': 2}, {'m': 1, 'k': 3}, {'m': 1, 'k': 4}, {'m': 1, 'k': 5}, {'m': 1, 'k': 6}, {'m': 2, 'k': 1}, {'m': 2, 'k': 2}, {'m': 2, 'k': 3}, {'m': 2, 'k': 4}, {'m': 2, 'k': 5}, {'m': 2, 'k': 6}, {'m': 3, 'k': 1}, {'m': 3, 'k': 2}, {'m': 3, 'k': 3}, {'m': 3, 'k': 4}, {'m': 3, 'k': 5}, {'m': 3, 'k': 6}, {'m': 4, 'k': 1}, {'m': 4, 'k': 2}, {'m': 4, 'k': 3}, {'m': 4, 'k': 4}, {'m': 4, 'k': 5}, {'m': 4, 'k': 6}, {'m': 5, 'k': 1}, {'m': 5, 'k': 2}, {'m': 5, 'k': 3}, {'m': 5, 'k': 4}, {'m': 5, 'k': 5}, {'m': 5, 'k': 6}]
FORMULAS = {'A': '2*(k+m)**2', 'B': '(k+m)**2', 'C': '(k+m)**2/2', 'D': '(k-m)**2'}
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
    print(f"VERIFIED_OK: CALC-MVT-AI-261023212509-FC24 ({len(report)} điểm tham số khớp bộ giải độc lập)")
