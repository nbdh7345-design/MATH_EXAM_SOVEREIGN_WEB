# -*- coding: utf-8 -*-
"""
Agent-01: Giải tích — Giới hạn & Khai triển Taylor-Maclaurin có tham số.
Sinh và kiểm chứng tự động (SymPy + NumPy + Lean 4 Core) cho ngân hàng đề thi.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 1,
    "agent_code": "AGENT-01",
    "agent_name": "Agent-01 (Giải tích: Giới hạn & Khai triển Taylor)",
    "domain": "Giải tích",
    "role_desc": "Sinh & kiểm chứng câu hỏi Giới hạn hàm số, L'Hospital, Khai triển Taylor-Maclaurin có tham số",
}


def get_questions() -> list[dict]:
    """Trả về 3 câu hỏi chuẩn hóa (2 MCQ, 1 Essay) có tham số m thuộc [2..9]."""
    return [
        # =====================================================================
        # CÂU 1: CALC-LIM-01 (MCQ - Vận dụng)
        # =====================================================================
        {
            "code": "CALC-LIM-01",
            "agent_id": 1,
            "agent_name": "Agent-01 (Giải tích: Giới hạn & Taylor)",
            "subject": "Giải tích",
            "topic": "Giới hạn & Khai triển Taylor-Maclaurin",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": [
                {
                    "name": "m",
                    "symbol": "m",
                    "default": 3,
                    "min": 2,
                    "max": 9,
                    "step": 1,
                    "label": "Tham số nguyên dương m",
                }
            ],
            "title": "Giới hạn bậc ba kết hợp hàm mũ và lượng giác bằng khai triển Maclaurin",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \ge 2$. Giá trị của giới hạn "
                r"$$L(m) = \lim_{x \to 0} \frac{6\left(e^{m x} - 1 - \sin(m x) - \frac{m^2 x^2}{2}\right)}{x^3}$$ "
                r"bằng biểu thức nào dưới đây?"
            ),
            "stem_template": (
                r"Cho tham số $m = {m}$. Tính giá trị của giới hạn "
                r"$$L({m}) = \lim_{{x \to 0}} \frac{{6\left(e^{{{m} x}} - 1 - \sin({m} x) - \frac{{{m}^2 x^2}}{{2}}\right)}}{{x^3}}$$"
            ),
            "options_symbolic": {
                "A": r"$2m^3$",
                "B": r"$m^3$",
                "C": r"$3m^3$",
                "D": r"$4m^3$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m**3",
                    "B": "m**3",
                    "C": "3*m**3",
                    "D": "4*m**3",
                },
                "target_expr": "2*m**3",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Áp dụng khai triển Maclaurin đến cấp $3$ tại lân cận $x = 0$:" "\n"
                r"- $e^{m x} = 1 + m x + \frac{m^2 x^2}{2!} + \frac{m^3 x^3}{3!} + o(x^3) "
                r"= 1 + m x + \frac{m^2}{2}x^2 + \frac{m^3}{6}x^3 + o(x^3)$." "\n"
                r"- $\sin(m x) = m x - \frac{m^3 x^3}{3!} + o(x^3) = m x - \frac{m^3}{6}x^3 + o(x^3)$." "\n\n"
                r"Thay vào tử số của biểu thức giới hạn:" "\n"
                r"$$e^{m x} - 1 - \sin(m x) - \frac{m^2 x^2}{2} "
                r"= \left(\frac{m^3}{6} - \left(-\frac{m^3}{6}\right)\right)x^3 + o(x^3) = \frac{m^3}{3}x^3 + o(x^3).$$" "\n\n"
                r"Nhân thêm hệ số $6$ và chia cho $x^3$, ta thu được:" "\n"
                r"$$L(m) = \lim_{x \to 0} \frac{6 \cdot \frac{m^3}{3}x^3 + o(x^3)}{x^3} = 2m^3.$$" "\n"
                r"Vậy đáp án đúng là **A** ($2m^3$)."
            ),
            "rubric_points": [
                "Khai triển đúng chuỗi Maclaurin của e^(mx) đến bậc 3: 1 + mx + m^2*x^2/2 + m^3*x^3/6 + o(x^3) (0.4 điểm)",
                "Khai triển đúng chuỗi Maclaurin của sin(mx) đến bậc 3: mx - m^3*x^3/6 + o(x^3) (0.3 điểm)",
                "Rút gọn tử số và kết luận chính xác giới hạn L(m) = 2*m^3 (0.3 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-LIM-01 (Taylor coefficient arithmetic)\n"
                "-- Numerator x^3 coefficient scaled by 6: 6 * (m^3 / 6 - (-m^3 / 6)) = 2 * m^3\n"
                "def exp_coeff3_scaled6 (m : Int) : Int := m ^ 3\n"
                "def sin_coeff3_scaled6 (m : Int) : Int := -(m ^ 3)\n"
                "def limit_calc_lim_01 (m : Int) : Int := exp_coeff3_scaled6 m - sin_coeff3_scaled6 m\n\n"
                "theorem calc_lim_01_at_m3 : limit_calc_lim_01 3 = 54 := by decide\n"
                "theorem calc_lim_01_at_m5 : limit_calc_lim_01 5 = 250 := by decide\n"
                "theorem calc_lim_01_distinct_m2 : limit_calc_lim_01 2 != 2^3 ∧ limit_calc_lim_01 2 != 3*(2^3) := by decide\n\n"
                "#eval limit_calc_lim_01 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "x, m = sp.symbols('x m', real=True)\n"
                "expr = 6 * (sp.exp(m * x) - 1 - sp.sin(m * x) - (m**2 * x**2) / 2) / x**3\n"
                "lim_symbolic = sp.simplify(sp.limit(expr, x, 0))\n"
                "expected = 2 * m**3\n"
                "assert sp.simplify(lim_symbolic - expected) == 0, f'Symbolic mismatch: {lim_symbolic} != {expected}'\n\n"
                "for m_val in range(2, 10):\n"
                "    h = 1e-4\n"
                "    num_approx = 6 * (np.exp(m_val * h) - 1.0 - np.sin(m_val * h) - 0.5 * (m_val**2) * (h**2)) / (h**3)\n"
                "    exact_val = 2 * (m_val**3)\n"
                "    assert abs(num_approx - exact_val) / exact_val < 1e-2, f'Numeric check failed at m={m_val}'\n"
                "    opts = [2*m_val**3, m_val**3, 3*m_val**3, 4*m_val**3]\n"
                "    assert len(set(opts)) == 4, f'Duplicate options at m={m_val}'\n\n"
                "print('VERIFIED_OK: CALC-LIM-01')\n"
            ),
        },
        # =====================================================================
        # CÂU 2: CALC-LIM-02 (MCQ - Vận dụng cao)
        # =====================================================================
        {
            "code": "CALC-LIM-02",
            "agent_id": 1,
            "agent_name": "Agent-01 (Giải tích: Giới hạn & Taylor)",
            "subject": "Giải tích",
            "topic": "Giới hạn & Khai triển Taylor-Maclaurin",
            "question_type": "mcq",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": [
                {
                    "name": "m",
                    "symbol": "m",
                    "default": 3,
                    "min": 2,
                    "max": 9,
                    "step": 1,
                    "label": "Tham số nguyên dương m",
                }
            ],
            "title": "Giới hạn vô cùng bé bậc bốn của hiệu hàm mũ Gauss và hàm cosin",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Tính giới hạn "
                r"$$I(m) = \lim_{x \to 0} \frac{12\left(e^{-\frac{m^2 x^2}{2}} - \cos(m x)\right)}{x^4}.$$"
            ),
            "stem_template": (
                r"Cho tham số $m = {m}$. Tính giới hạn "
                r"$$I({m}) = \lim_{{x \to 0}} \frac{{12\left(e^{{-\frac{{{m}^2 x^2}}{{2}}}} - \cos({m} x)\right)}}{{x^4}}.$$"
            ),
            "options_symbolic": {
                "A": r"$\frac{m^4}{2}$",
                "B": r"$m^4$",
                "C": r"$2m^4$",
                "D": r"$3m^4$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**4/2",
                    "B": "m**4",
                    "C": "2*m**4",
                    "D": "3*m**4",
                },
                "target_expr": "m**4",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Khai triển Maclaurin đến cấp $4$ quanh $x = 0$:" "\n"
                r"1. Đặt $u = -\frac{m^2 x^2}{2}$, ta có:" "\n"
                r"$$e^{-\frac{m^2 x^2}{2}} = 1 + u + \frac{u^2}{2!} + o(x^4) "
                r"= 1 - \frac{m^2}{2}x^2 + \frac{m^4}{8}x^4 + o(x^4).$$" "\n"
                r"2. Khai triển $\cos(m x)$:" "\n"
                r"$$\cos(m x) = 1 - \frac{(m x)^2}{2!} + \frac{(m x)^4}{4!} + o(x^4) "
                r"= 1 - \frac{m^2}{2}x^2 + \frac{m^4}{24}x^4 + o(x^4).$$" "\n\n"
                r"Trừ hai khai triển cho nhau, số hạng bậc $0$ và bậc $2$ triệt tiêu hoàn toàn:" "\n"
                r"$$e^{-\frac{m^2 x^2}{2}} - \cos(m x) = \left(\frac{1}{8} - \frac{1}{24}\right)m^4 x^4 + o(x^4) "
                r"= \frac{1}{12}m^4 x^4 + o(x^4).$$" "\n\n"
                r"Do đó:" "\n"
                r"$$I(m) = \lim_{x \to 0} \frac{12 \cdot \frac{1}{12}m^4 x^4 + o(x^4)}{x^4} = m^4.$$" "\n"
                r"Chọn đáp án **B**."
            ),
            "rubric_points": [
                "Khai triển đúng hàm hợp e^(-m^2*x^2/2) = 1 - m^2*x^2/2 + m^4*x^4/8 + o(x^4) (0.4 điểm)",
                "Khai triển đúng cos(mx) = 1 - m^2*x^2/2 + m^4*x^4/24 + o(x^4) (0.3 điểm)",
                "Khử số hạng bậc hai, rút gọn hệ số 12*(1/8 - 1/24) = 1 và kết luận I(m) = m^4 (0.3 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-LIM-02 (4th-order Taylor cancellation)\n"
                "-- Scaled by 24: 12 * (3 * m^4 / 24 - 1 * m^4 / 24) = m^4\n"
                "def gauss_coeff4_scaled24 (m : Int) : Int := 3 * (m ^ 4)\n"
                "def cos_coeff4_scaled24 (m : Int) : Int := 1 * (m ^ 4)\n"
                "def limit_calc_lim_02 (m : Int) : Int :=\n"
                "  (12 * (gauss_coeff4_scaled24 m - cos_coeff4_scaled24 m)) / 24\n\n"
                "theorem calc_lim_02_at_m3 : limit_calc_lim_02 3 = 81 := by decide\n"
                "theorem calc_lim_02_at_m4 : limit_calc_lim_02 4 = 256 := by decide\n\n"
                "#eval limit_calc_lim_02 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "x, m = sp.symbols('x m', real=True)\n"
                "expr = 12 * (sp.exp(-m**2 * x**2 / 2) - sp.cos(m * x)) / x**4\n"
                "series_num = sp.series(12 * (sp.exp(-m**2 * x**2 / 2) - sp.cos(m * x)), x, 0, 5).removeO()\n"
                "lim_symbolic = sp.simplify(sp.limit(expr, x, 0))\n"
                "assert sp.simplify(lim_symbolic - m**4) == 0, f'Expected m**4, got {lim_symbolic}'\n"
                "assert sp.simplify(series_num / x**4 - m**4) == 0\n\n"
                "for m_val in range(2, 10):\n"
                "    h = 5e-3\n"
                "    num_val = 12.0 * (np.exp(-0.5 * (m_val**2) * (h**2)) - np.cos(m_val * h)) / (h**4)\n"
                "    exact_val = float(m_val**4)\n"
                "    assert abs(num_val - exact_val) / exact_val < 1e-2, f'Numeric check failed at m={m_val}'\n"
                "    opts = [0.5 * m_val**4, float(m_val**4), 2.0 * m_val**4, 3.0 * m_val**4]\n"
                "    assert len(set(opts)) == 4\n\n"
                "print('VERIFIED_OK: CALC-LIM-02')\n"
            ),
        },
        # =====================================================================
        # CÂU 3: CALC-LIM-03 (ESSAY - Vận dụng cao)
        # =====================================================================
        {
            "code": "CALC-LIM-03",
            "agent_id": 1,
            "agent_name": "Agent-01 (Giải tích: Giới hạn & Taylor)",
            "subject": "Giải tích",
            "topic": "Giới hạn & Khai triển Taylor-Maclaurin",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": [
                {
                    "name": "m",
                    "symbol": "m",
                    "default": 3,
                    "min": 2,
                    "max": 9,
                    "step": 1,
                    "label": "Tham số nguyên dương m",
                }
            ],
            "title": "Xác định tham số triệt tiêu vô cùng bé và tính giới hạn bậc bốn",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Xét giới hạn phụ thuộc các hệ số thực $a, b$:" "\n"
                r"$$J(m) = \lim_{x \to 0} \frac{4\left(\ln(1 + m x) - \sin(m x) + a x^2 + b x^3\right)}{x^4}.$$" "\n"
                r"a) Tìm các hệ số $a, b$ theo $m$ để giới hạn $J(m)$ tồn tại hữu hạn." "\n"
                r"b) Với $a, b$ vừa tìm được, hãy tính giá trị của $J(m)$ theo $m$."
            ),
            "stem_template": (
                r"Cho tham số $m = {m}$. Xét giới hạn phụ thuộc các hệ số thực $a, b$:" "\n"
                r"$$J({m}) = \lim_{{x \to 0}} \frac{{4\left(\ln(1 + {m} x) - \sin({m} x) + a x^2 + b x^3\right)}}{{x^4}}.$$" "\n"
                r"a) Tìm các hệ số $a, b$ khi $m = {m}$ để giới hạn $J({m})$ tồn tại hữu hạn." "\n"
                r"b) Với $a, b$ vừa tìm được, hãy tính giá trị chính xác của $J({m})$."
            ),
            "options_symbolic": {},
            "parametric_formulas": {
                "options": {},
                "target_expr": "-m**4",
            },
            "correct_option": "ESSAY",
            "solution_symbolic": (
                r"**Lời giải chi tiết (Tự luận):**" "\n\n"
                r"**Ý a) Xác định $a, b$ để giới hạn hữu hạn:**" "\n"
                r"Khai triển Maclaurin của $\ln(1 + m x)$ và $\sin(m x)$ đến cấp $4$ khi $x \to 0$:" "\n"
                r"$$\ln(1 + m x) = m x - \frac{m^2}{2}x^2 + \frac{m^3}{3}x^3 - \frac{m^4}{4}x^4 + o(x^4),$$" "\n"
                r"$$\sin(m x) = m x - \frac{m^3}{6}x^3 + o(x^4).$$" "\n"
                r"Khi đó tử số (chưa nhân $4$) có dạng:" "\n"
                r"$$\ln(1 + m x) - \sin(m x) + a x^2 + b x^3 "
                r"= \left(a - \frac{m^2}{2}\right)x^2 + \left(b + \frac{m^3}{3} + \frac{m^3}{6}\right)x^3 - \frac{m^4}{4}x^4 + o(x^4)$$" "\n"
                r"$$= \left(a - \frac{m^2}{2}\right)x^2 + \left(b + \frac{m^3}{2}\right)x^3 - \frac{m^4}{4}x^4 + o(x^4).$$" "\n"
                r"Do mẫu số là $x^4$, điều kiện cần và đủ để giới hạn $J(m)$ tồn tại hữu hạn là hệ số của $x^2$ và $x^3$ phải đồng thời bằng $0$:" "\n"
                r"$$\begin{cases} a - \dfrac{m^2}{2} = 0 \\ b + \dfrac{m^3}{2} = 0 \end{cases} "
                r"\iff \begin{cases} a = \dfrac{m^2}{2} \\ b = -\dfrac{m^3}{2} \end{cases}.$$" "\n\n"
                r"**Ý b) Tính giá trị giới hạn $J(m)$:**" "\n"
                r"Thay $a = \frac{m^2}{2}$ và $b = -\frac{m^3}{2}$ vào biểu thức, ta được:" "\n"
                r"$$J(m) = \lim_{x \to 0} \frac{4\left(-\frac{m^4}{4}x^4 + o(x^4)\right)}{x^4} = -m^4.$$"
            ),
            "rubric_points": [
                "Khai triển đúng Maclaurin của ln(1 + mx) và sin(mx) đến bậc 4 kèm phần dư Peano o(x^4) (0.35 điểm)",
                "Nhóm đúng các hệ số bậc 2 là (a - m^2/2) và bậc 3 là (b + m^3/2) (0.25 điểm)",
                "Giải hệ điều kiện cần & đủ tìm đúng a = m^2/2 và b = -m^3/2 (0.20 điểm)",
                "Thay vào biểu thức bậc 4 và tính đúng kết quả J(m) = -m^4 (0.20 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-LIM-03 (Essay Taylor matching)\n"
                "-- Scaled by 12 for degree 3: ln coeff is 4*m^3, -sin coeff is 2*m^3 => sum = 6*m^3 = m^3/2\n"
                "-- Scaled by 4 for degree 4: 4 * (-m^4 / 4) = -m^4\n"
                "def two_a (m : Int) : Int := m ^ 2\n"
                "def two_b (m : Int) : Int := -(m ^ 3)\n"
                "def limit_calc_lim_03 (m : Int) : Int := -(m ^ 4)\n\n"
                "theorem calc_lim_03_conditions_m3 :\n"
                "  two_a 3 = 9 ∧ two_b 3 = -27 ∧ limit_calc_lim_03 3 = -81 := by decide\n\n"
                "#eval (two_a 3, two_b 3, limit_calc_lim_03 3)\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "x, m, a, b = sp.symbols('x m a b', real=True)\n"
                "num_expr = 4 * (sp.log(1 + m * x) - sp.sin(m * x) + a * x**2 + b * x**3)\n"
                "ser = sp.series(num_expr, x, 0, 5).removeO()\n"
                "c2 = sp.Poly(ser, x).nth(2)\n"
                "c3 = sp.Poly(ser, x).nth(3)\n"
                "sol = sp.solve([c2, c3], (a, b))\n"
                "assert sp.simplify(sol[a] - m**2 / 2) == 0, f'Wrong a: {sol[a]}'\n"
                "assert sp.simplify(sol[b] + m**3 / 2) == 0, f'Wrong b: {sol[b]}'\n\n"
                "expr_sub = num_expr.subs(sol) / x**4\n"
                "lim_val = sp.simplify(sp.limit(expr_sub, x, 0))\n"
                "assert sp.simplify(lim_val - (-m**4)) == 0, f'Wrong limit: {lim_val}'\n\n"
                "for m_val in range(2, 10):\n"
                "    a_val = 0.5 * (m_val**2)\n"
                "    b_val = -0.5 * (m_val**3)\n"
                "    h = 2e-3\n"
                "    approx = 4.0 * (np.log(1.0 + m_val * h) - np.sin(m_val * h) + a_val * h**2 + b_val * h**3) / (h**4)\n"
                "    exact = -float(m_val**4)\n"
                "    assert abs(approx - exact) / abs(exact) < 5e-2, f'Numeric check failed at m={m_val}'\n\n"
                "print('VERIFIED_OK: CALC-LIM-03')\n"
            ),
        },
    ]
