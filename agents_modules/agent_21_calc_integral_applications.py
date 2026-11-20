# -*- coding: utf-8 -*-
"""
Agent-21: Giải tích — Ứng dụng hình học của tích phân xác định có tham số.
Diện tích hình phẳng, thể tích vật thể tròn xoay, độ dài cung và diện tích trong tọa độ cực.
Sinh và kiểm chứng tự động (SymPy + mpmath + Lean 4 Core) cho ngân hàng đề thi.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 21,
    "agent_code": "AGENT-21",
    "agent_name": "Agent-21 (Giải tích: Ứng dụng của tích phân)",
    "domain": "Giải tích",
    "role_desc": "Diện tích hình phẳng, Thể tích vật tròn xoay, Độ dài cung & Diện tích trong tọa độ cực có tham số",
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
        # CÂU 1: CALC-APP-01 (MCQ - Thông hiểu)
        # =====================================================================
        {
            "code": "CALC-APP-01",
            "agent_id": 21,
            "agent_name": "Agent-21 (Giải tích: Ứng dụng của tích phân)",
            "subject": "Giải tích",
            "topic": "Ứng dụng hình học của tích phân xác định",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Diện tích hình phẳng giới hạn bởi parabol và đường thẳng qua gốc tọa độ",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Diện tích $S(m)$ của hình phẳng giới hạn bởi "
                r"parabol $y = x^2$ và đường thẳng $y = m x$ bằng"
            ),
            "stem_template": (
                r"Cho $m = {m}$. Tính diện tích $S$ của hình phẳng giới hạn bởi parabol $y = x^2$ "
                r"và đường thẳng $y = {m} x$."
            ),
            "options_symbolic": {
                "A": r"$\dfrac{m^3}{6}$",
                "B": r"$\dfrac{m^3}{3}$",
                "C": r"$\dfrac{m^3}{2}$",
                "D": r"$\dfrac{m^2}{6}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**3/6",
                    "B": "m**3/3",
                    "C": "m**3/2",
                    "D": "m**2/6",
                },
                "target_expr": "m**3/6",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Hoành độ giao điểm: $x^2 = m x \iff x = 0$ hoặc $x = m$. "
                r"Trên $[0, m]$ ta có $m x - x^2 = x(m - x) \ge 0$ nên đường thẳng nằm trên parabol." "\n\n"
                r"$$S(m) = \int_0^m (m x - x^2)\,dx = \left[\frac{m x^2}{2} - \frac{x^3}{3}\right]_0^m "
                r"= \frac{m^3}{2} - \frac{m^3}{3} = \frac{m^3}{6}.$$" "\n"
                r"Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Tìm đúng hoành độ giao điểm x = 0 và x = m (0.3 điểm)",
                "Xác định đúng hàm trên - hàm dưới mx - x^2 >= 0 trên [0, m] (0.3 điểm)",
                "Tính đúng tích phân và kết luận S = m^3/6 (0.4 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-APP-01 (area between y = x^2 and y = m x)\n"
                "-- Scaled by 6: 6 * (m^3/2 - m^3/3) = 3 m^3 - 2 m^3 = m^3\n"
                "def area6 (m : Int) : Int := 3 * m ^ 3 - 2 * m ^ 3\n"
                "def options6 (m : Int) : List Int := [m ^ 3, 2 * m ^ 3, 3 * m ^ 3, m ^ 2]\n\n"
                "theorem calc_app_01_area :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2; area6 m == m ^ 3) = true := by decide\n"
                "theorem calc_app_01_upper_line :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      (List.range (k + 3)).all (fun j => let x : Int := j; !(decide (x ≤ m)) || decide (m * x - x ^ 2 ≥ 0))) = true := by\n"
                "  decide\n"
                "theorem calc_app_01_distinct :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2; (options6 m).Nodup) = true := by decide\n\n"
                "#eval area6 3\n"
            ),
            "python_code": '''import sympy as sp

x, m = sp.symbols('x m', positive=True)
roots = sp.solve(sp.Eq(x**2, m * x), x)
assert set(roots) == {m}, f'Unexpected positive roots: {roots}'
S = sp.integrate(m * x - x**2, (x, 0, m))
assert sp.simplify(S - m**3 / 6) == 0, f'Area mismatch: {S}'

for mv in range(2, 10):
    # Kiểm tra số: tổng Riemann điểm giữa
    N = 20000
    h = mv / N
    approx = sum((mv * (h * (i + 0.5)) - (h * (i + 0.5))**2) * h for i in range(N))
    assert abs(approx - mv**3 / 6) < 1e-6 * mv**3, f'Numeric area failed at m={mv}'
    opts = [sp.Rational(mv**3, 6), sp.Rational(mv**3, 3), sp.Rational(mv**3, 2), sp.Rational(mv**2, 6)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-APP-01')
''',
        },
        # =====================================================================
        # CÂU 2: CALC-APP-02 (MCQ - Vận dụng)
        # =====================================================================
        {
            "code": "CALC-APP-02",
            "agent_id": 21,
            "agent_name": "Agent-21 (Giải tích: Ứng dụng của tích phân)",
            "subject": "Giải tích",
            "topic": "Ứng dụng hình học của tích phân xác định",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Thể tích vật thể tròn xoay sinh bởi cung parabol quay quanh trục Ox",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Gọi $D$ là hình phẳng giới hạn bởi đường cong "
                r"$y = x(m - x)$ và trục hoành. Thể tích $V(m)$ của vật thể tròn xoay sinh ra khi quay $D$ "
                r"quanh trục $Ox$ bằng"
            ),
            "stem_template": (
                r"Cho $m = {m}$. Gọi $D$ là hình phẳng giới hạn bởi đường cong $y = x({m} - x)$ và trục hoành. "
                r"Tính thể tích $V$ của vật thể tròn xoay sinh ra khi quay $D$ quanh trục $Ox$."
            ),
            "options_symbolic": {
                "A": r"$\dfrac{\pi m^5}{15}$",
                "B": r"$\dfrac{\pi m^5}{60}$",
                "C": r"$\dfrac{\pi m^5}{30}$",
                "D": r"$\dfrac{\pi m^5}{20}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "pi*m**5/15",
                    "B": "pi*m**5/60",
                    "C": "pi*m**5/30",
                    "D": "pi*m**5/20",
                },
                "target_expr": "pi*m**5/30",
            },
            "correct_option": "C",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Đường cong cắt trục hoành tại $x = 0$ và $x = m$. Theo công thức thể tích vật tròn xoay "
                r"quanh $Ox$:" "\n"
                r"$$V(m) = \pi \int_0^m x^2 (m - x)^2\,dx = \pi \int_0^m \left(m^2 x^2 - 2m x^3 + x^4\right)dx "
                r"= \pi\left(\frac{m^5}{3} - \frac{m^5}{2} + \frac{m^5}{5}\right) = \frac{\pi m^5}{30}.$$" "\n"
                r"Chọn đáp án **C**."
            ),
            "rubric_points": [
                "Xác định đúng cận x = 0, x = m (0.2 điểm)",
                "Viết đúng công thức V = pi * tích phân y^2 dx (0.3 điểm)",
                "Khai triển x^2 (m - x)^2 và tính đúng tích phân (0.3 điểm)",
                "Kết luận V = pi m^5 / 30 (0.2 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-APP-02 (solid of revolution, disc method)\n"
                "-- Scaled by 30: 30 * (m^5/3 - m^5/2 + m^5/5) = 10 m^5 - 15 m^5 + 6 m^5 = m^5\n"
                "def vol30 (m : Int) : Int := 10 * m ^ 5 - 15 * m ^ 5 + 6 * m ^ 5\n"
                "def options60 (m : Int) : List Int := [4 * m ^ 5, m ^ 5, 2 * m ^ 5, 3 * m ^ 5]\n\n"
                "theorem calc_app_02_volume :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2; vol30 m == m ^ 5) = true := by decide\n"
                "theorem calc_app_02_expand :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      (List.range 10).all (fun j => let x : Int := j;\n"
                "        x ^ 2 * (m - x) ^ 2 == m ^ 2 * x ^ 2 - 2 * m * x ^ 3 + x ^ 4)) = true := by decide\n"
                "theorem calc_app_02_distinct :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2; (options60 m).Nodup) = true := by decide\n\n"
                "#eval vol30 3\n"
            ),
            "python_code": '''import sympy as sp
import mpmath

x, m = sp.symbols('x m', positive=True)
V = sp.pi * sp.integrate((x * (m - x))**2, (x, 0, m))
assert sp.simplify(V - sp.pi * m**5 / 30) == 0, f'Volume mismatch: {V}'

for mv in range(2, 10):
    approx = mpmath.pi * mpmath.quad(lambda t: (t * (mv - t))**2, [0, mv])
    exact = mpmath.pi * mv**5 / 30
    assert abs(approx - exact) < 1e-9 * exact, f'Numeric volume failed at m={mv}'
    opts = [sp.pi * mv**5 / 15, sp.pi * mv**5 / 60, sp.pi * mv**5 / 30, sp.pi * mv**5 / 20]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-APP-02')
''',
        },
        # =====================================================================
        # CÂU 3: CALC-APP-03 (ESSAY - Vận dụng cao)
        # =====================================================================
        {
            "code": "CALC-APP-03",
            "agent_id": 21,
            "agent_name": "Agent-21 (Giải tích: Ứng dụng của tích phân)",
            "subject": "Giải tích",
            "topic": "Ứng dụng hình học của tích phân xác định",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Độ dài và diện tích của đường Cardioid trong tọa độ cực",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$ và đường Cardioid trong tọa độ cực "
                r"$$r = m(1 + \cos\theta), \quad -\pi \le \theta \le \pi.$$" "\n"
                r"a) Tính độ dài $L(m)$ của đường cong." "\n"
                r"b) Tính diện tích $S(m)$ của miền phẳng giới hạn bởi đường cong."
            ),
            "stem_template": (
                r"Cho đường Cardioid trong tọa độ cực $$r = {m}(1 + \cos\theta), \quad -\pi \le \theta \le \pi.$$" "\n"
                r"a) Tính độ dài $L$ của đường cong." "\n"
                r"b) Tính diện tích $S$ của miền phẳng giới hạn bởi đường cong."
            ),
            "options_symbolic": {},
            "parametric_formulas": {
                "options": {},
                "target_expr": "3*pi*m**2/2",
            },
            "correct_option": "ESSAY",
            "solution_symbolic": (
                r"**Lời giải chi tiết (Tự luận):**" "\n\n"
                r"**Ý a) Độ dài cung.** Ta có $r' = -m\sin\theta$ nên" "\n"
                r"$$r^2 + r'^2 = m^2\left[(1 + \cos\theta)^2 + \sin^2\theta\right] = 2m^2(1 + \cos\theta) "
                r"= 4m^2\cos^2\frac{\theta}{2}.$$" "\n"
                r"Với $\theta \in [-\pi, \pi]$ thì $\cos\frac{\theta}{2} \ge 0$, do đó" "\n"
                r"$$L(m) = \int_{-\pi}^{\pi} \sqrt{r^2 + r'^2}\,d\theta = \int_{-\pi}^{\pi} 2m\cos\frac{\theta}{2}\,d\theta "
                r"= 4m\left[\sin\frac{\theta}{2}\right]_{-\pi}^{\pi} = 8m.$$" "\n\n"
                r"**Ý b) Diện tích.** Theo công thức diện tích trong tọa độ cực:" "\n"
                r"$$S(m) = \frac{1}{2}\int_{-\pi}^{\pi} r^2\,d\theta = \frac{m^2}{2}\int_{-\pi}^{\pi}"
                r"\left(1 + 2\cos\theta + \cos^2\theta\right)d\theta = \frac{m^2}{2}\left(2\pi + 0 + \pi\right) "
                r"= \frac{3\pi m^2}{2}.$$"
            ),
            "rubric_points": [
                "Tính đúng r' và rút gọn r^2 + r'^2 = 4m^2 cos^2(theta/2) (0.25 điểm)",
                "Xử lý đúng dấu cos(theta/2) >= 0 trên [-pi, pi] và tính L = 8m (0.25 điểm)",
                "Viết đúng công thức S = 1/2 * tích phân r^2 d(theta) (0.2 điểm)",
                "Tính đúng các tích phân 1, cos, cos^2 trên một chu kỳ và kết luận S = 3 pi m^2 / 2 (0.3 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-APP-03 (Cardioid: arc length & polar area)\n"
                "-- Area: 1/2 * m^2 * (2π + 0 + π) => coefficient of π scaled by 2 is 3 m^2\n"
                "-- Length: ∫ 2m cos(θ/2) over [-π, π] = 4m (sin(π/2) - sin(-π/2)) = 8m\n"
                "def piCoeffIntegral : Nat := 2 + 0 + 1          -- ∫(1 + 2cos θ + cos²θ) = 3π\n"
                "def area2PiCoeff (m : Nat) : Nat := m ^ 2 * piCoeffIntegral\n"
                "def arcLength (m : Nat) : Nat := 4 * m * (1 + 1)\n\n"
                "theorem calc_app_03_area :\n"
                "    (List.range 8).all (fun k => let m := k + 2; area2PiCoeff m == 3 * m ^ 2) = true := by decide\n"
                "theorem calc_app_03_length :\n"
                "    (List.range 8).all (fun k => let m := k + 2; arcLength m == 8 * m) = true := by decide\n\n"
                "#eval (area2PiCoeff 3, arcLength 3)\n"
            ),
            "python_code": '''import sympy as sp
import mpmath

t = sp.symbols('theta', real=True)
m = sp.symbols('m', positive=True)
r = m * (1 + sp.cos(t))
dr = sp.diff(r, t)

# Rút gọn r^2 + r'^2 = 2 m^2 (1 + cos theta) = 4 m^2 cos^2(theta/2)
assert sp.simplify(sp.trigsimp(r**2 + dr**2) - 2 * m**2 * (1 + sp.cos(t))) == 0
for tv in [-3.0, -1.2, 0.0, 0.7, 2.5]:
    assert abs(2 * (1 + mpmath.cos(tv)) - 4 * mpmath.cos(tv / 2)**2) < 1e-12

S = sp.integrate(r**2 / 2, (t, -sp.pi, sp.pi))
assert sp.simplify(S - 3 * sp.pi * m**2 / 2) == 0, f'Area mismatch: {S}'
L = sp.integrate(2 * m * sp.cos(t / 2), (t, -sp.pi, sp.pi))
assert sp.simplify(L - 8 * m) == 0, f'Length mismatch: {L}'

for mv in range(2, 10):
    Ln = mpmath.quad(lambda th: mpmath.sqrt((mv * (1 + mpmath.cos(th)))**2 + (mv * mpmath.sin(th))**2),
                     [-mpmath.pi, 0, mpmath.pi])
    assert abs(Ln - 8 * mv) < 1e-8 * mv, f'Numeric length failed at m={mv}'
    Sn = mpmath.quad(lambda th: (mv * (1 + mpmath.cos(th)))**2 / 2, [-mpmath.pi, mpmath.pi])
    assert abs(Sn - 1.5 * mpmath.pi * mv**2) < 1e-8 * mv**2, f'Numeric area failed at m={mv}'

print('VERIFIED_OK: CALC-APP-03')
''',
        },
    ]
