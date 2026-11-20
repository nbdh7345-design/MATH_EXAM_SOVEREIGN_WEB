# -*- coding: utf-8 -*-
"""
Agent-25: Giải tích — Tích phân hàm hữu tỷ, tích phân cận biến thiên & tích phân tam thức bậc hai có tham số.
Sinh và kiểm chứng tự động (SymPy + mpmath + Lean 4 Core) cho ngân hàng đề thi.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 25,
    "agent_code": "AGENT-25",
    "agent_name": "Agent-25 (Giải tích: Nguyên hàm & Tích phân cận biến thiên)",
    "domain": "Giải tích",
    "role_desc": "Tích phân hàm hữu tỷ (tách phân thức), Tích phân cận biến thiên & Tích phân tam thức bậc hai có tham số",
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
        # CÂU 1: CALC-ANTI-01 (MCQ - Thông hiểu)
        # =====================================================================
        {
            "code": "CALC-ANTI-01",
            "agent_id": 25,
            "agent_name": "Agent-25 (Giải tích: Nguyên hàm & Tích phân cận biến thiên)",
            "subject": "Giải tích",
            "topic": "Nguyên hàm, tích phân hàm hữu tỷ & tích phân cận biến thiên",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Tích phân hàm hữu tỷ bằng phương pháp tách phân thức đơn giản",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Giá trị của tích phân "
                r"$$I(m) = \int_0^1 \frac{dx}{(x + 1)(x + m)}$$ bằng"
            ),
            "stem_template": (
                r"Cho $m = {m}$. Tính tích phân $$I = \int_0^1 \frac{dx}{(x + 1)(x + {m})}.$$"
            ),
            "options_symbolic": {
                "A": r"$\dfrac{1}{m - 1}\ln\dfrac{2m}{m + 1}$",
                "B": r"$\dfrac{1}{m + 1}\ln\dfrac{2m}{m + 1}$",
                "C": r"$\dfrac{1}{m - 1}\ln\dfrac{m + 1}{2}$",
                "D": r"$\dfrac{1}{m - 1}\ln\dfrac{m + 1}{2m}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "log(2*m/(m + 1))/(m - 1)",
                    "B": "log(2*m/(m + 1))/(m + 1)",
                    "C": "log((m + 1)/2)/(m - 1)",
                    "D": "log((m + 1)/(2*m))/(m - 1)",
                },
                "target_expr": "log(2*m/(m + 1))/(m - 1)",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Với $m \ne 1$, tách phân thức: $\dfrac{1}{(x + 1)(x + m)} = \dfrac{1}{m - 1}\left(\dfrac{1}{x + 1} - \dfrac{1}{x + m}\right)$." "\n"
                r"$$I(m) = \frac{1}{m - 1}\Big[\ln(x + 1) - \ln(x + m)\Big]_0^1 = \frac{1}{m - 1}\left(\ln 2 - \ln\frac{m + 1}{m}\right) "
                r"= \frac{1}{m - 1}\ln\frac{2m}{m + 1}.$$" "\n"
                r"Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Tách đúng phân thức với hệ số 1/(m - 1) (0.4 điểm)",
                "Tìm đúng nguyên hàm ln|x + 1| - ln|x + m| (0.3 điểm)",
                "Thay cận và rút gọn thành ln(2m/(m + 1))/(m - 1) (0.3 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-ANTI-01 (partial fractions)\n"
                "-- 1/((x+1)(x+m)) = (1/(m-1)) (1/(x+1) - 1/(x+m))  ⇔  (x + m) - (x + 1) = m - 1\n"
                "-- Log argument after evaluating at the bounds: 2 / ((m+1)/m) = 2m/(m+1)\n"
                "def numerAfterCombine (m x : Int) : Int := (x + m) - (x + 1)\n"
                "def logArgNum (m : Int) : Int := 2 * m\n"
                "def logArgDen (m : Int) : Int := m + 1\n\n"
                "theorem calc_anti_01_partial_fraction :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      (List.range 11).all (fun j => numerAfterCombine m j == m - 1)) = true := by decide\n"
                "theorem calc_anti_01_log_argument :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      logArgNum m > logArgDen m && m - 1 > 0) = true := by decide\n\n"
                "#eval (logArgNum 3, logArgDen 3)\n"
            ),
            "python_code": '''import math
import mpmath
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
pf = sp.apart(1 / ((x + 1) * (x + 3)), x)
assert sp.simplify(pf - (sp.Rational(1, 2) / (x + 1) - sp.Rational(1, 2) / (x + 3))) == 0

for mv in range(2, 10):
    I = sp.integrate(1 / ((x + 1) * (x + mv)), (x, 0, 1))
    exact = sp.log(sp.Rational(2 * mv, mv + 1)) / (mv - 1)
    assert abs(float(I - exact)) < 1e-12, f'Symbolic integral mismatch at m={mv}: {I}'
    num = mpmath.quad(lambda t: 1 / ((t + 1) * (t + mv)), [0, 1])
    assert abs(num - float(exact)) < 1e-12
    opts = [math.log(2 * mv / (mv + 1)) / (mv - 1), math.log(2 * mv / (mv + 1)) / (mv + 1),
            math.log((mv + 1) / 2) / (mv - 1), math.log((mv + 1) / (2 * mv)) / (mv - 1)]
    assert len({round(o, 12) for o in opts}) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-ANTI-01')
''',
        },
        # =====================================================================
        # CÂU 2: CALC-ANTI-02 (MCQ - Vận dụng)
        # =====================================================================
        {
            "code": "CALC-ANTI-02",
            "agent_id": 25,
            "agent_name": "Agent-25 (Giải tích: Nguyên hàm & Tích phân cận biến thiên)",
            "subject": "Giải tích",
            "topic": "Nguyên hàm, tích phân hàm hữu tỷ & tích phân cận biến thiên",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Giới hạn chứa tích phân cận biến thiên",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Giá trị của giới hạn "
                r"$$\lim_{x \to 0} \frac{1}{x^3}\int_0^x \sin(m t^2)\,dt$$ bằng"
            ),
            "stem_template": (
                r"Cho $m = {m}$. Tính giới hạn $$\lim_{x \to 0} \frac{1}{x^3}\int_0^x \sin({m} t^2)\,dt.$$"
            ),
            "options_symbolic": {
                "A": r"$m$",
                "B": r"$\dfrac{m}{6}$",
                "C": r"$\dfrac{m}{2}$",
                "D": r"$\dfrac{m}{3}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m",
                    "B": "m/6",
                    "C": "m/2",
                    "D": "m/3",
                },
                "target_expr": "m/3",
            },
            "correct_option": "D",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Đặt $\Phi(x) = \int_0^x \sin(m t^2)\,dt$. Hàm dưới dấu tích phân liên tục nên $\Phi'(x) = \sin(m x^2)$ "
                r"và $\Phi(0) = 0$; giới hạn có dạng $\frac{0}{0}$. Theo quy tắc L'Hospital:" "\n"
                r"$$\lim_{x \to 0} \frac{\Phi(x)}{x^3} = \lim_{x \to 0} \frac{\sin(m x^2)}{3x^2} = \lim_{x \to 0} \frac{m x^2}{3x^2} = \frac{m}{3}.$$" "\n"
                r"Chọn đáp án **D**."
            ),
            "rubric_points": [
                "Nhận dạng 0/0 và tính đúng đạo hàm của tích phân cận trên Phi'(x) = sin(m x^2) (0.4 điểm)",
                "Áp dụng L'Hospital và VCB sin(m x^2) ~ m x^2 (0.4 điểm)",
                "Kết luận giới hạn bằng m/3 (0.2 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-ANTI-02 (variable upper limit + L'Hospital)\n"
                "-- sin(m t^2) = m t^2 + o(t^2)  =>  ∫_0^x sin(m t^2) dt = m x^3 / 3 + o(x^3)\n"
                "-- All option values scaled by 6\n"
                "def leading6 (m : Nat) : Nat := 6 * m / 3\n"
                "def options6 (m : Nat) : List Nat := [6 * m, m, 3 * m, 2 * m]\n\n"
                "theorem calc_anti_02_leading :\n"
                "    (List.range 8).all (fun k => let m := k + 2; leading6 m == 2 * m) = true := by decide\n"
                "theorem calc_anti_02_distinct :\n"
                "    (List.range 8).all (fun k => let m := k + 2; (options6 m).Nodup) = true := by decide\n\n"
                "#eval leading6 3\n"
            ),
            "python_code": '''import mpmath
import sympy as sp

x, t = sp.symbols('x t', real=True)
m = sp.symbols('m', positive=True)
L = sp.limit(sp.sin(m * x**2) / (3 * x**2), x, 0)
assert sp.simplify(L - m / 3) == 0, f'L Hospital limit mismatch: {L}'
ser = sp.integrate(sp.series(sp.sin(m * t**2), t, 0, 8).removeO(), (t, 0, x))
assert sp.simplify(sp.limit(ser / x**3, x, 0) - m / 3) == 0

for mv in range(2, 10):
    h = mpmath.mpf('1e-3')
    num = mpmath.quad(lambda s: mpmath.sin(mv * s**2), [0, h]) / h**3
    assert abs(num - mpmath.mpf(mv) / 3) < 1e-4 * mv, f'Numeric check failed at m={mv}'
    opts = [mv, mv / 6, mv / 2, mv / 3]
    assert len(set(opts)) == 4

print('VERIFIED_OK: CALC-ANTI-02')
''',
        },
        # =====================================================================
        # CÂU 3: CALC-ANTI-03 (ESSAY - Vận dụng cao)
        # =====================================================================
        {
            "code": "CALC-ANTI-03",
            "agent_id": 25,
            "agent_name": "Agent-25 (Giải tích: Nguyên hàm & Tích phân cận biến thiên)",
            "subject": "Giải tích",
            "topic": "Nguyên hàm, tích phân hàm hữu tỷ & tích phân cận biến thiên",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Nguyên hàm và tích phân của nghịch đảo tam thức bậc hai vô nghiệm",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$." "\n"
                r"a) Tìm nguyên hàm $\displaystyle\int \frac{dx}{x^2 + 2x + m^2 + 1}$." "\n"
                r"b) Tính tích phân $\displaystyle I(m) = \int_{-1}^{m - 1} \frac{dx}{x^2 + 2x + m^2 + 1}$."
            ),
            "stem_template": (
                r"a) Tìm nguyên hàm $\displaystyle\int \frac{dx}{x^2 + 2x + {m}^2 + 1}$." "\n"
                r"b) Tính tích phân $\displaystyle I = \int_{-1}^{{m} - 1} \frac{dx}{x^2 + 2x + {m}^2 + 1}$."
            ),
            "options_symbolic": {},
            "parametric_formulas": {
                "options": {},
                "target_expr": "pi/(4*m)",
            },
            "correct_option": "ESSAY",
            "solution_symbolic": (
                r"**Lời giải chi tiết (Tự luận):**" "\n\n"
                r"**Ý a)** Tách bình phương: $x^2 + 2x + m^2 + 1 = (x + 1)^2 + m^2$. Đặt $u = x + 1$, $du = dx$:" "\n"
                r"$$\int \frac{dx}{(x + 1)^2 + m^2} = \int \frac{du}{u^2 + m^2} = \frac{1}{m}\arctan\frac{u}{m} + C "
                r"= \frac{1}{m}\arctan\frac{x + 1}{m} + C.$$" "\n\n"
                r"**Ý b)** Theo công thức Newton–Leibniz:" "\n"
                r"$$I(m) = \frac{1}{m}\left[\arctan\frac{x + 1}{m}\right]_{-1}^{m - 1} = \frac{1}{m}\left(\arctan 1 - \arctan 0\right) "
                r"= \frac{\pi}{4m}.$$"
            ),
            "rubric_points": [
                "Tách đúng bình phương (x + 1)^2 + m^2 (0.25 điểm)",
                "Đổi biến u = x + 1 và tìm đúng nguyên hàm (1/m) arctan((x + 1)/m) + C (0.35 điểm)",
                "Thay cận đúng: arctan 1 - arctan 0 (0.2 điểm)",
                "Kết luận I = pi/(4m) (0.2 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-ANTI-03 (completing the square)\n"
                "-- x^2 + 2x + m^2 + 1 = (x + 1)^2 + m^2 ; bounds map to u = 0 and u = m, i.e. u/m = 0 and 1\n"
                "-- arctan 1 - arctan 0 = π/4  =>  I = π/(4m)\n"
                "def quad (m x : Int) : Int := x ^ 2 + 2 * x + m ^ 2 + 1\n"
                "def completed (m x : Int) : Int := (x + 1) ^ 2 + m ^ 2\n\n"
                "theorem calc_anti_03_square :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      (List.range 21).all (fun j => let x : Int := j - 10; quad m x == completed m x && quad m x > 0)) = true := by\n"
                "  decide\n"
                "theorem calc_anti_03_bounds :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2; (-1 + 1) == 0 && ((m - 1) + 1) == m) = true := by decide\n\n"
                "#eval completed 3 2\n"
            ),
            "python_code": '''import mpmath
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
F = sp.atan((x + 1) / m) / m
assert sp.simplify(sp.diff(F, x) - 1 / (x**2 + 2 * x + m**2 + 1)) == 0, 'Antiderivative check failed'
I = sp.simplify(F.subs(x, m - 1) - F.subs(x, -1))
assert sp.simplify(I - sp.pi / (4 * m)) == 0, f'Integral mismatch: {I}'

for mv in range(2, 10):
    num = mpmath.quad(lambda t: 1 / (t**2 + 2 * t + mv**2 + 1), [-1, mv - 1])
    assert abs(num - mpmath.pi / (4 * mv)) < 1e-12, f'Numeric check failed at m={mv}'

print('VERIFIED_OK: CALC-ANTI-03')
''',
        },
    ]
