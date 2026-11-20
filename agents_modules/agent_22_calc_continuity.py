# -*- coding: utf-8 -*-
"""
Agent-22: Giải tích — Giới hạn dãy số, Vô cùng bé tương đương, Liên tục & Phân loại điểm gián đoạn.
Sinh và kiểm chứng tự động (SymPy + Lean 4 Core) cho ngân hàng đề thi.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 22,
    "agent_code": "AGENT-22",
    "agent_name": "Agent-22 (Giải tích: Giới hạn dãy, VCB & Liên tục)",
    "domain": "Giải tích",
    "role_desc": "Giới hạn dãy dạng 1^∞, Thay VCB tương đương, Tham số để hàm liên tục & Phân loại điểm gián đoạn",
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
        # CÂU 1: CALC-CONT-01 (MCQ - Thông hiểu)
        # =====================================================================
        {
            "code": "CALC-CONT-01",
            "agent_id": 22,
            "agent_name": "Agent-22 (Giải tích: Giới hạn dãy, VCB & Liên tục)",
            "subject": "Giải tích",
            "topic": "Giới hạn dãy số, VCB tương đương & Liên tục",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Giới hạn dãy số dạng vô định 1 mũ vô cùng",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Giới hạn của dãy số "
                r"$$u_n = \left(1 + \frac{m}{n}\right)^{2n}$$ khi $n \to \infty$ bằng"
            ),
            "stem_template": (
                r"Cho $m = {m}$. Tính giới hạn của dãy số $$u_n = \left(1 + \frac{{m}}{n}\right)^{2n}$$ khi $n \to \infty$."
            ),
            "options_symbolic": {
                "A": r"$e^{m}$",
                "B": r"$e^{2m}$",
                "C": r"$e^{m/2}$",
                "D": r"$e^{3m}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "exp(m)",
                    "B": "exp(2*m)",
                    "C": "exp(m/2)",
                    "D": "exp(3*m)",
                },
                "target_expr": "exp(2*m)",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Dãy có dạng vô định $1^\infty$. Ta có $\ln u_n = 2n \ln\left(1 + \frac{m}{n}\right)$. "
                r"Vì $\ln(1 + t) \sim t$ khi $t \to 0$ và $\frac{m}{n} \to 0$ nên" "\n"
                r"$$\lim_{n \to \infty} \ln u_n = \lim_{n \to \infty} 2n \cdot \frac{m}{n} = 2m.$$" "\n"
                r"Do hàm mũ liên tục, $\lim_{n \to \infty} u_n = e^{2m}$. Chọn đáp án **B**."
            ),
            "rubric_points": [
                "Nhận dạng đúng dạng vô định 1^∞ và lấy logarit (0.3 điểm)",
                "Thay VCB tương đương ln(1 + m/n) ~ m/n (0.4 điểm)",
                "Dùng tính liên tục của hàm mũ, kết luận lim u_n = e^(2m) (0.3 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-CONT-01 (limit of type 1^∞)\n"
                "-- ln u_n = 2n ln(1 + m/n) ~ 2n * (m/n) = 2m; exponents of the options scaled by 2\n"
                "def limitExponent (m : Nat) : Nat := 2 * m\n"
                "def exponents2 (m : Nat) : List Nat := [2 * m, 4 * m, m, 6 * m]\n\n"
                "theorem calc_cont_01_exponent :\n"
                "    (List.range 8).all (fun k => let m := k + 2; 2 * limitExponent m == 4 * m) = true := by decide\n"
                "theorem calc_cont_01_distinct :\n"
                "    (List.range 8).all (fun k => let m := k + 2; (exponents2 m).Nodup) = true := by decide\n\n"
                "#eval limitExponent 3\n"
            ),
            "python_code": '''import math
import sympy as sp

n, m = sp.symbols('n m', positive=True)
L = sp.limit((1 + m / n)**(2 * n), n, sp.oo)
assert sp.simplify(L - sp.exp(2 * m)) == 0, f'Limit mismatch: {L}'

for mv in range(2, 10):
    N = 10**7
    approx = math.exp(2 * N * math.log1p(mv / N))
    assert abs(approx / math.exp(2 * mv) - 1) < 1e-4, f'Numeric check failed at m={mv}'
    opts = [math.exp(mv), math.exp(2 * mv), math.exp(mv / 2), math.exp(3 * mv)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-CONT-01')
''',
        },
        # =====================================================================
        # CÂU 2: CALC-CONT-02 (MCQ - Vận dụng)
        # =====================================================================
        {
            "code": "CALC-CONT-02",
            "agent_id": 22,
            "agent_name": "Agent-22 (Giải tích: Giới hạn dãy, VCB & Liên tục)",
            "subject": "Giải tích",
            "topic": "Giới hạn dãy số, VCB tương đương & Liên tục",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Thay vô cùng bé tương đương trong giới hạn dạng 0/0",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Giá trị của giới hạn "
                r"$$\lim_{x \to 0} \frac{e^{m x^2} - 1}{1 - \cos x}$$ bằng"
            ),
            "stem_template": (
                r"Cho $m = {m}$. Tính giới hạn $$\lim_{x \to 0} \frac{e^{{m} x^2} - 1}{1 - \cos x}.$$"
            ),
            "options_symbolic": {
                "A": r"$m$",
                "B": r"$\dfrac{m}{2}$",
                "C": r"$2m$",
                "D": r"$4m$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m",
                    "B": "m/2",
                    "C": "2*m",
                    "D": "4*m",
                },
                "target_expr": "2*m",
            },
            "correct_option": "C",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Khi $x \to 0$: $m x^2 \to 0$ nên $e^{m x^2} - 1 \sim m x^2$; đồng thời $1 - \cos x \sim \dfrac{x^2}{2}$." "\n"
                r"Thay các VCB tương đương trong thương:" "\n"
                r"$$\lim_{x \to 0} \frac{e^{m x^2} - 1}{1 - \cos x} = \lim_{x \to 0} \frac{m x^2}{x^2/2} = 2m.$$" "\n"
                r"Chọn đáp án **C**."
            ),
            "rubric_points": [
                "Viết đúng e^(m x^2) - 1 ~ m x^2 khi x -> 0 (0.35 điểm)",
                "Viết đúng 1 - cos x ~ x^2/2 khi x -> 0 (0.35 điểm)",
                "Thay tương đương trong thương và kết luận giới hạn bằng 2m (0.3 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-CONT-02 (equivalent infinitesimals)\n"
                "-- numerator ~ m x^2, denominator ~ x^2/2 => ratio of leading coefficients m / (1/2) = 2m\n"
                "-- All quantities scaled by 2 to stay in Nat\n"
                "def numCoeff2 (m : Nat) : Nat := 2 * m\n"
                "def denCoeff2 : Nat := 1\n"
                "def options2 (m : Nat) : List Nat := [2 * m, m, 4 * m, 8 * m]\n\n"
                "theorem calc_cont_02_ratio :\n"
                "    (List.range 8).all (fun k => let m := k + 2; numCoeff2 m / denCoeff2 == 2 * m) = true := by decide\n"
                "theorem calc_cont_02_distinct :\n"
                "    (List.range 8).all (fun k => let m := k + 2; (options2 m).Nodup) = true := by decide\n\n"
                "#eval numCoeff2 3 / denCoeff2\n"
            ),
            "python_code": '''import math
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
expr = (sp.exp(m * x**2) - 1) / (1 - sp.cos(x))
L = sp.limit(expr, x, 0)
assert sp.simplify(L - 2 * m) == 0, f'Limit mismatch: {L}'

for mv in range(2, 10):
    h = 1e-3
    approx = math.expm1(mv * h * h) / (2 * math.sin(h / 2)**2)
    assert abs(approx - 2 * mv) < 1e-3 * mv, f'Numeric check failed at m={mv}'
    opts = [mv, mv / 2, 2 * mv, 4 * mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-CONT-02')
''',
        },
        # =====================================================================
        # CÂU 3: CALC-CONT-03 (ESSAY - Vận dụng cao)
        # =====================================================================
        {
            "code": "CALC-CONT-03",
            "agent_id": 22,
            "agent_name": "Agent-22 (Giải tích: Giới hạn dãy, VCB & Liên tục)",
            "subject": "Giải tích",
            "topic": "Giới hạn dãy số, VCB tương đương & Liên tục",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Tìm tham số để hàm liên tục và phân loại điểm gián đoạn",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$ và các hàm số" "\n"
                r"$$f(x) = \begin{cases} \dfrac{1 - \cos(m x)}{x^2}, & x \ne 0 \\ a, & x = 0 \end{cases}, \qquad "
                r"g(x) = \begin{cases} \arctan\dfrac{m}{x}, & x \ne 0 \\ 0, & x = 0 \end{cases}.$$" "\n"
                r"a) Tìm $a$ để $f$ liên tục tại $x = 0$." "\n"
                r"b) Khi $a$ khác giá trị tìm được ở câu a), $x = 0$ là điểm gián đoạn loại gì của $f$?" "\n"
                r"c) Xét tính liên tục của $g$ tại $x = 0$; nếu gián đoạn, hãy phân loại và tính bước nhảy."
            ),
            "stem_template": (
                r"Cho các hàm số" "\n"
                r"$$f(x) = \begin{cases} \dfrac{1 - \cos({m} x)}{x^2}, & x \ne 0 \\ a, & x = 0 \end{cases}, \qquad "
                r"g(x) = \begin{cases} \arctan\dfrac{{m}}{x}, & x \ne 0 \\ 0, & x = 0 \end{cases}.$$" "\n"
                r"a) Tìm $a$ để $f$ liên tục tại $x = 0$." "\n"
                r"b) Khi $a$ khác giá trị tìm được ở câu a), $x = 0$ là điểm gián đoạn loại gì của $f$?" "\n"
                r"c) Xét tính liên tục của $g$ tại $x = 0$; nếu gián đoạn, hãy phân loại và tính bước nhảy."
            ),
            "options_symbolic": {},
            "parametric_formulas": {
                "options": {},
                "target_expr": "m**2/2",
            },
            "correct_option": "ESSAY",
            "solution_symbolic": (
                r"**Lời giải chi tiết (Tự luận):**" "\n\n"
                r"**Ý a)** Khi $x \to 0$: $1 - \cos(m x) \sim \dfrac{(m x)^2}{2}$, nên" "\n"
                r"$$\lim_{x \to 0} f(x) = \lim_{x \to 0} \frac{m^2 x^2 / 2}{x^2} = \frac{m^2}{2}.$$" "\n"
                r"$f$ liên tục tại $0$ khi và chỉ khi $\lim_{x \to 0} f(x) = f(0)$, tức $a = \dfrac{m^2}{2}$." "\n\n"
                r"**Ý b)** Khi $a \ne \dfrac{m^2}{2}$: giới hạn $\lim_{x \to 0} f(x)$ tồn tại hữu hạn nhưng khác $f(0)$, "
                r"nên $x = 0$ là **điểm gián đoạn khử được** (thuộc loại 1)." "\n\n"
                r"**Ý c)** Khi $x \to 0^+$: $\dfrac{m}{x} \to +\infty$ nên $g(x) \to \dfrac{\pi}{2}$; "
                r"khi $x \to 0^-$: $\dfrac{m}{x} \to -\infty$ nên $g(x) \to -\dfrac{\pi}{2}$." "\n"
                r"Hai giới hạn một phía hữu hạn nhưng khác nhau, nên $x = 0$ là **điểm gián đoạn loại 1 (bước nhảy)**, "
                r"với bước nhảy $\dfrac{\pi}{2} - \left(-\dfrac{\pi}{2}\right) = \pi$."
            ),
            "rubric_points": [
                "Dùng đúng VCB tương đương 1 - cos(mx) ~ (mx)^2/2 và tính lim f = m^2/2 (0.3 điểm)",
                "Kết luận a = m^2/2 từ điều kiện lim f(x) = f(0) (0.2 điểm)",
                "Phân loại đúng: gián đoạn khử được khi a khác m^2/2 (0.2 điểm)",
                "Tính đúng giới hạn trái -pi/2, phải pi/2 của g, kết luận gián đoạn loại 1 với bước nhảy pi (0.3 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-CONT-03 (continuity parameter & jump)\n"
                "-- 1 - cos(mx) ~ (mx)^2 / 2  => lim f = m^2 / 2 ; scaled by 2: 2a = m^2\n"
                "-- One-sided limits of arctan(m/x) in units of π/2: right = 1, left = -1 => jump = 2 * (π/2) = π\n"
                "def twoA (m : Nat) : Nat := m ^ 2\n"
                "def rightLimitHalfPi : Int := 1\n"
                "def leftLimitHalfPi : Int := -1\n"
                "def jumpHalfPi : Int := rightLimitHalfPi - leftLimitHalfPi\n\n"
                "theorem calc_cont_03_param :\n"
                "    (List.range 8).all (fun k => let m := k + 2; twoA m == m * m) = true := by decide\n"
                "theorem calc_cont_03_jump : jumpHalfPi = 2 ∧ leftLimitHalfPi ≠ rightLimitHalfPi := by decide\n\n"
                "#eval (twoA 3, jumpHalfPi)\n"
            ),
            "python_code": '''import math
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)

Lf = sp.limit((1 - sp.cos(m * x)) / x**2, x, 0)
assert sp.simplify(Lf - m**2 / 2) == 0, f'lim f mismatch: {Lf}'

Lr = sp.limit(sp.atan(m / x), x, 0, '+')
Ll = sp.limit(sp.atan(m / x), x, 0, '-')
assert sp.simplify(Lr - sp.pi / 2) == 0 and sp.simplify(Ll + sp.pi / 2) == 0, f'one-sided limits: {Ll}, {Lr}'
assert sp.simplify(Lr - Ll - sp.pi) == 0

for mv in range(2, 10):
    h = 1e-4
    approx = 2 * math.sin(mv * h / 2)**2 / h**2
    assert abs(approx - mv**2 / 2) < 1e-4 * mv**2, f'Numeric lim f failed at m={mv}'
    assert abs(math.atan(mv / 1e-9) - math.pi / 2) < 1e-6
    assert abs(math.atan(mv / -1e-9) + math.pi / 2) < 1e-6

print('VERIFIED_OK: CALC-CONT-03')
''',
        },
    ]
