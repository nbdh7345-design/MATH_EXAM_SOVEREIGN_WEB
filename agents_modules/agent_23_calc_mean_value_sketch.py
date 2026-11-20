# -*- coding: utf-8 -*-
"""
Agent-23: Giải tích — Các định lý giá trị trung bình (Rolle, Lagrange) & Khảo sát hàm số
(tiệm cận, tính lồi lõm, điểm uốn) có tham số.
Sinh và kiểm chứng tự động (SymPy + Lean 4 Core) cho ngân hàng đề thi.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 23,
    "agent_code": "AGENT-23",
    "agent_name": "Agent-23 (Giải tích: Định lý giá trị trung bình & Khảo sát hàm số)",
    "domain": "Giải tích",
    "role_desc": "Định lý Rolle, Lagrange, Tiệm cận đứng/xiên, Lồi lõm & Điểm uốn có tham số",
}

_PARAM_M = [
    {
        "name": "m",
        "symbol": "m",
        "default": 3,
        "min": 2,
        "max": 9,
        "step": 1,
        "label": "Tham số nguyên dương m",
    }
]


def get_questions() -> list[dict]:
    """Trả về 3 câu hỏi chuẩn hóa (2 MCQ, 1 Essay) có tham số m thuộc [2..9]."""
    return [
        # =====================================================================
        # CÂU 1: CALC-MVT-01 (MCQ - Thông hiểu)
        # =====================================================================
        {
            "code": "CALC-MVT-01",
            "agent_id": 23,
            "agent_name": "Agent-23 (Giải tích: Định lý giá trị trung bình & Khảo sát hàm số)",
            "subject": "Giải tích",
            "topic": "Định lý giá trị trung bình & Khảo sát hàm số",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Điểm trung gian trong định lý Lagrange cho hàm bậc ba",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$ và hàm số $f(x) = x^3$ trên đoạn $[0, m]$. "
                r"Điểm $c \in (0, m)$ thỏa mãn kết luận của định lý Lagrange "
                r"$f(m) - f(0) = f'(c)\,(m - 0)$ là"
            ),
            "stem_template": (
                r"Cho hàm số $f(x) = x^3$ trên đoạn $[0, {m}]$. Tìm điểm $c \in (0, {m})$ thỏa mãn kết luận "
                r"của định lý Lagrange $f({m}) - f(0) = f'(c)\,({m} - 0)$."
            ),
            "options_symbolic": {
                "A": r"$c = \dfrac{m\sqrt{3}}{3}$",
                "B": r"$c = \dfrac{m}{2}$",
                "C": r"$c = \dfrac{m}{3}$",
                "D": r"$c = \dfrac{m\sqrt{2}}{2}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m*sqrt(3)/3",
                    "B": "m/2",
                    "C": "m/3",
                    "D": "m*sqrt(2)/2",
                },
                "target_expr": "m*sqrt(3)/3",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"$f$ liên tục trên $[0, m]$, khả vi trên $(0, m)$ nên định lý Lagrange áp dụng được. "
                r"Ta có $f'(c) = 3c^2$ và" "\n"
                r"$$\frac{f(m) - f(0)}{m - 0} = \frac{m^3}{m} = m^2 \implies 3c^2 = m^2 \implies c = \pm\frac{m}{\sqrt{3}}.$$" "\n"
                r"Chỉ nghiệm $c = \dfrac{m}{\sqrt{3}} = \dfrac{m\sqrt{3}}{3} \in (0, m)$ được nhận. Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Kiểm tra điều kiện áp dụng định lý Lagrange (0.2 điểm)",
                "Lập đúng phương trình 3c^2 = m^2 (0.4 điểm)",
                "Loại nghiệm âm, kết luận c = m/sqrt(3) thuộc (0, m) (0.4 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MVT-01 (Lagrange mean value point)\n"
                "-- 3 c^2 = m^2. Squares of the options scaled by 36: A = 12 m^2, B = 9 m^2, C = 4 m^2, D = 18 m^2\n"
                "def optionSq36 (m : Nat) : List Nat := [12 * m ^ 2, 9 * m ^ 2, 4 * m ^ 2, 18 * m ^ 2]\n"
                "def slope (m : Nat) : Nat := m ^ 3 / m\n\n"
                "theorem calc_mvt_01_slope :\n"
                "    (List.range 8).all (fun k => let m := k + 2; slope m == m ^ 2) = true := by decide\n"
                "theorem calc_mvt_01_answer :\n"
                "    (List.range 8).all (fun k => let m := k + 2;\n"
                "      3 * (12 * m ^ 2) == 36 * m ^ 2 && 12 * m ^ 2 < 36 * m ^ 2) = true := by decide\n"
                "theorem calc_mvt_01_distinct :\n"
                "    (List.range 8).all (fun k => let m := k + 2; (optionSq36 m).Nodup) = true := by decide\n\n"
                "#eval optionSq36 3\n"
            ),
            "python_code": '''import sympy as sp

c, m = sp.symbols('c m', positive=True)
f = lambda t: t**3
sols = sp.solve(sp.Eq(sp.diff(c**3, c) * m, f(m) - f(0)), c)
assert sols == [sp.sqrt(3) * m / 3], f'Unexpected Lagrange points: {sols}'

for mv in range(2, 10):
    cv = mv * sp.sqrt(3) / 3
    assert 0 < cv < mv
    assert sp.simplify(3 * cv**2 * mv - mv**3) == 0
    opts = [mv * sp.sqrt(3) / 3, sp.Rational(mv, 2), sp.Rational(mv, 3), mv * sp.sqrt(2) / 2]
    assert len({float(o) for o in opts}) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-MVT-01')
''',
        },
        # =====================================================================
        # CÂU 2: CALC-MVT-02 (MCQ - Vận dụng)
        # =====================================================================
        {
            "code": "CALC-MVT-02",
            "agent_id": 23,
            "agent_name": "Agent-23 (Giải tích: Định lý giá trị trung bình & Khảo sát hàm số)",
            "subject": "Giải tích",
            "topic": "Định lý giá trị trung bình & Khảo sát hàm số",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Tiệm cận xiên của hàm phân thức bậc hai trên bậc nhất",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Đồ thị hàm số "
                r"$$y = \frac{x^2 + m x + 1}{x - 1}$$ có tiệm cận xiên $y = a x + b$. Giá trị $a + b$ bằng"
            ),
            "stem_template": (
                r"Đồ thị hàm số $$y = \frac{x^2 + {m} x + 1}{x - 1}$$ có tiệm cận xiên $y = a x + b$. Tính $a + b$."
            ),
            "options_symbolic": {
                "A": r"$m + 1$",
                "B": r"$m$",
                "C": r"$m + 3$",
                "D": r"$m + 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m + 1",
                    "B": "m",
                    "C": "m + 3",
                    "D": "m + 2",
                },
                "target_expr": "m + 2",
            },
            "correct_option": "D",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Chia đa thức: $x^2 + m x + 1 = (x - 1)(x + m + 1) + (m + 2)$, nên" "\n"
                r"$$y = x + (m + 1) + \frac{m + 2}{x - 1}.$$" "\n"
                r"Khi $x \to \pm\infty$ thì $\dfrac{m + 2}{x - 1} \to 0$, do đó tiệm cận xiên là $y = x + m + 1$, "
                r"tức $a = 1$, $b = m + 1$ (kiểm tra lại: $a = \lim \frac{y}{x} = 1$, $b = \lim (y - x) = m + 1$)." "\n"
                r"Vậy $a + b = m + 2$. Chọn đáp án **D**. (Ngoài ra, vì $m + 2 \ne 0$, đồ thị có tiệm cận đứng $x = 1$.)"
            ),
            "rubric_points": [
                "Chia đa thức đúng: x^2 + mx + 1 = (x - 1)(x + m + 1) + (m + 2) (0.4 điểm)",
                "Xác định đúng a = lim y/x = 1 và b = lim (y - x) = m + 1 (0.4 điểm)",
                "Kết luận a + b = m + 2 (0.2 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MVT-02 (slant asymptote by polynomial division)\n"
                "-- x^2 + m x + 1 = (x - 1)(x + m + 1) + (m + 2)  =>  a = 1, b = m + 1\n"
                "def numer (m x : Int) : Int := x ^ 2 + m * x + 1\n"
                "def divided (m x : Int) : Int := (x - 1) * (x + m + 1) + (m + 2)\n"
                "def optionsAB (m : Int) : List Int := [m + 1, m, m + 3, m + 2]\n\n"
                "theorem calc_mvt_02_division :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      (List.range 21).all (fun j => let x : Int := j - 10; numer m x == divided m x)) = true := by decide\n"
                "theorem calc_mvt_02_answer :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      1 + (m + 1) == m + 2 && m + 2 != 0 && (optionsAB m).Nodup) = true := by decide\n\n"
                "#eval divided 3 5\n"
            ),
            "python_code": '''import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
y = (x**2 + m * x + 1) / (x - 1)
a = sp.limit(y / x, x, sp.oo)
b = sp.limit(y - a * x, x, sp.oo)
assert a == 1 and sp.simplify(b - (m + 1)) == 0, f'Asymptote mismatch: a={a}, b={b}'
assert sp.limit(y / x, x, -sp.oo) == 1 and sp.simplify(sp.limit(y - x, x, -sp.oo) - (m + 1)) == 0
q, r = sp.div(sp.Poly(x**2 + m * x + 1, x), sp.Poly(x - 1, x))
assert sp.simplify(q.as_expr() - (x + m + 1)) == 0 and sp.simplify(r.as_expr() - (m + 2)) == 0

for mv in range(2, 10):
    yv = lambda t: (t**2 + mv * t + 1) / (t - 1)
    assert abs(yv(1e7) - (1e7 + mv + 1)) < 1e-5
    opts = [mv + 1, mv, mv + 3, mv + 2]
    assert len(set(opts)) == 4

print('VERIFIED_OK: CALC-MVT-02')
''',
        },
        # =====================================================================
        # CÂU 3: CALC-MVT-03 (ESSAY - Vận dụng cao)
        # =====================================================================
        {
            "code": "CALC-MVT-03",
            "agent_id": 23,
            "agent_name": "Agent-23 (Giải tích: Định lý giá trị trung bình & Khảo sát hàm số)",
            "subject": "Giải tích",
            "topic": "Định lý giá trị trung bình & Khảo sát hàm số",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Định lý Rolle, khoảng lồi lõm và điểm uốn của hàm bậc ba có tham số",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$ và hàm số $f(x) = x^3 - 3m x^2 + 2$." "\n"
                r"a) Chứng minh rằng tồn tại $c \in (0, 3m)$ sao cho $f'(c) = 0$ và tìm $c$." "\n"
                r"b) Xác định các khoảng lồi, lõm của đồ thị hàm số." "\n"
                r"c) Tìm tọa độ điểm uốn $I(x_0, y_0)$ của đồ thị; tính $y_0$ theo $m$."
            ),
            "stem_template": (
                r"Cho hàm số $f(x) = x^3 - 3 \cdot {m} x^2 + 2$." "\n"
                r"a) Chứng minh rằng tồn tại $c \in (0, 3 \cdot {m})$ sao cho $f'(c) = 0$ và tìm $c$." "\n"
                r"b) Xác định các khoảng lồi, lõm của đồ thị hàm số." "\n"
                r"c) Tìm tọa độ điểm uốn $I(x_0, y_0)$ của đồ thị; tính $y_0$."
            ),
            "options_symbolic": {},
            "parametric_formulas": {
                "options": {},
                "target_expr": "2 - 2*m**3",
            },
            "correct_option": "ESSAY",
            "solution_symbolic": (
                r"**Lời giải chi tiết (Tự luận):**" "\n\n"
                r"**Ý a)** $f$ là đa thức nên liên tục trên $[0, 3m]$ và khả vi trên $(0, 3m)$. Ta có "
                r"$f(0) = 2$ và $f(3m) = 27m^3 - 27m^3 + 2 = 2$, nên $f(0) = f(3m)$. "
                r"Theo định lý Rolle, tồn tại $c \in (0, 3m)$ với $f'(c) = 0$. "
                r"Giải $f'(c) = 3c^2 - 6mc = 3c(c - 2m) = 0$ được $c = 2m \in (0, 3m)$." "\n\n"
                r"**Ý b)** $f''(x) = 6x - 6m$. Trên $(-\infty, m)$: $f'' < 0$ nên đồ thị lồi (lõm xuống); "
                r"trên $(m, +\infty)$: $f'' > 0$ nên đồ thị lõm (lõm lên)." "\n\n"
                r"**Ý c)** $f''$ đổi dấu khi đi qua $x_0 = m$, nên điểm uốn là $I(m, f(m))$ với" "\n"
                r"$$y_0 = f(m) = m^3 - 3m^3 + 2 = 2 - 2m^3.$$"
            ),
            "rubric_points": [
                "Kiểm tra f(0) = f(3m) = 2 và điều kiện định lý Rolle (0.25 điểm)",
                "Giải f'(c) = 0, chọn đúng c = 2m thuộc (0, 3m) (0.25 điểm)",
                "Tính f''(x) = 6x - 6m và xét dấu, kết luận đúng khoảng lồi/lõm (0.25 điểm)",
                "Kết luận điểm uốn I(m, 2 - 2m^3) (0.25 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MVT-03 (Rolle point & inflection point)\n"
                "def f (m x : Int) : Int := x ^ 3 - 3 * m * x ^ 2 + 2\n"
                "def df (m x : Int) : Int := 3 * x ^ 2 - 6 * m * x\n"
                "def d2f (m x : Int) : Int := 6 * x - 6 * m\n\n"
                "theorem calc_mvt_03_rolle :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      f m 0 == f m (3 * m) && df m (2 * m) == 0 && 0 < 2 * m && 2 * m < 3 * m) = true := by decide\n"
                "theorem calc_mvt_03_inflection :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      d2f m m == 0 && d2f m (m - 1) < 0 && d2f m (m + 1) > 0 && f m m == 2 - 2 * m ^ 3) = true := by\n"
                "  decide\n\n"
                "#eval (f 3 (2 * 3), f 3 3)\n"
            ),
            "python_code": '''import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
f = x**3 - 3 * m * x**2 + 2
assert sp.simplify(f.subs(x, 0) - f.subs(x, 3 * m)) == 0
crit = sp.solve(sp.diff(f, x), x)
inside = [c for c in crit if sp.simplify(c) != 0]
assert len(inside) == 1 and sp.simplify(inside[0] - 2 * m) == 0, f'Rolle point mismatch: {crit}'
infl = sp.solve(sp.diff(f, x, 2), x)
assert len(infl) == 1 and sp.simplify(infl[0] - m) == 0
assert sp.simplify(f.subs(x, m) - (2 - 2 * m**3)) == 0

for mv in range(2, 10):
    fv = f.subs(m, mv)
    d2 = sp.diff(fv, x, 2)
    assert d2.subs(x, mv - sp.Rational(1, 2)) < 0 and d2.subs(x, mv + sp.Rational(1, 2)) > 0
    assert fv.subs(x, mv) == 2 - 2 * mv**3

print('VERIFIED_OK: CALC-MVT-03')
''',
        },
    ]
