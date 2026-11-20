"""
Agent-03: Giải tích — Tích phân xác định & Tích phân phụ thuộc tham số.
Sinh và kiểm chứng câu hỏi Tích phân xác định, Đổi biến, Tích phân từng phần
& Đạo hàm dưới dấu tích phân Leibniz có tham số m.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 3,
    "agent_code": "AGENT-03",
    "agent_name": "Agent-03 (Giải tích: Tích phân xác định & Tích phân tham số)",
    "domain": "Giải tích",
    "role_desc": "Sinh & kiểm chứng câu hỏi Tích phân xác định, Đổi biến, Tích phân từng phần & Đạo hàm dưới dấu tích phân Leibniz có tham số",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa (2 MCQ, 1 Essay) có tham số m."""
    return [
        {
            "code": "CALC-INT-01",
            "agent_id": 3,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Tích phân xác định & Tích phân phụ thuộc tham số",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": {
                "m": {
                    "type": "int",
                    "default": 3,
                    "min": 2,
                    "max": 9,
                    "step": 1,
                    "label": "Tham số m nguyên dương (m ≥ 2)",
                }
            },
            "title": "Tích phân từng phần & Đổi biến Euler–Beta có tham số",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \ge 2$. Xét tích phân xác định phụ thuộc tham số:"
                "\n"
                r"$$I(m) = \int_0^1 m^3 x (1 - x)^{m - 1} \, dx$$"
                "\n"
                r"Bằng phương pháp tích phân từng phần hoặc đổi biến $u = 1 - x$, "
                r"hãy xác định biểu thức rút gọn chính xác của $I(m)$ theo $m$."
            ),
            "stem_template": (
                r"Cho $m = {m}$. Tính giá trị chính xác của tích phân xác định:"
                "\n"
                r"$$I({m}) = \int_0^1 {m}^3 x (1 - x)^{{{m} - 1}} \, dx$$"
            ),
            "options_symbolic": {
                "A": r"\frac{m^2}{m + 1}",
                "B": r"\frac{m}{m + 1}",
                "C": r"\frac{m^2}{m - 1}",
                "D": r"\frac{m^3}{(m + 1)(m + 3)}",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2 / (m + 1)",
                    "B": "m / (m + 1)",
                    "C": "m**2 / (m - 1)",
                    "D": "m**3 / ((m + 1) * (m + 3))",
                },
                "target_expr": "m**2 / (m + 1)",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**"
                "\n\n"
                r"**Cách 1 (Đổi biến số):** Đặt $u = 1 - x \implies dx = -du$ và $x = 1 - u$. "
                r"Khi $x = 0 \implies u = 1$; khi $x = 1 \implies u = 0$. Do đó:"
                "\n"
                r"$$I(m) = m^3 \int_0^1 (1 - u) u^{m - 1} \, du = m^3 \int_0^1 \left(u^{m - 1} - u^m\right) du$$"
                "\n"
                r"$$I(m) = m^3 \left[ \frac{u^m}{m} - \frac{u^{m + 1}}{m + 1} \right]_0^1 "
                r"= m^3 \left( \frac{1}{m} - \frac{1}{m + 1} \right) = m^3 \cdot \frac{1}{m(m + 1)} = \frac{m^2}{m + 1}$$"
                "\n\n"
                r"**Cách 2 (Tích phân từng phần):** Đặt $u = x \implies du = dx$ và "
                r"$dv = (1 - x)^{m - 1} dx \implies v = -\frac{(1 - x)^m}{m}$. Ta có:"
                "\n"
                r"$$\int_0^1 x(1-x)^{m-1}dx = \left[ -\frac{x(1-x)^m}{m} \right]_0^1 + \frac{1}{m}\int_0^1 (1-x)^m dx "
                r"= 0 + \frac{1}{m(m + 1)}$$"
                "\n"
                r"Nhân thêm hệ số $m^3$, ta thu được $I(m) = \frac{m^2}{m + 1}$. Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Thực hiện đổi biến u = 1 - x hoặc đặt từng phần u = x, dv = (1 - x)^(m-1)dx đúng chuẩn: 0.5 điểm",
                "Tính đúng nguyên hàm trung gian u^m/m - u^(m+1)/(m+1) trên đoạn [0, 1]: 0.25 điểm",
                "Rút gọn đại số chính xác I(m) = m^2 / (m + 1): 0.25 điểm",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-INT-01: m^3 * (1/m - 1/(m+1)) = m^2 / (m+1)\n"
                "-- Cleared denominators identity: m^3 * ((m + 1) - m) = m^2 * m\n"
                "def lhs_cleared (m : Nat) : Nat := m^3 * ((m + 1) - m)\n"
                "def rhs_cleared (m : Nat) : Nat := m^2 * m\n\n"
                "theorem calc_int_01_m3 : lhs_cleared 3 = rhs_cleared 3 := by decide\n"
                "theorem calc_int_01_grid : List.all [2, 3, 4, 5, 6, 7, 8, 9] (fun m => lhs_cleared m == rhs_cleared m) = true := by decide\n\n"
                "#eval [2, 3, 4, 5, 6, 7, 8, 9].map (fun m => (m, m * m, m + 1))\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n"
                "from scipy.integrate import quad\n\n"
                "x = sp.Symbol('x', real=True)\n"
                "for m_val in range(2, 10):\n"
                "    integrand = (m_val**3) * x * (1 - x)**(m_val - 1)\n"
                "    sym_val = sp.integrate(integrand, (x, 0, 1))\n"
                "    expected = sp.Rational(m_val**2, m_val + 1)\n"
                "    assert sp.simplify(sym_val - expected) == 0, f'SymPy mismatch at m={m_val}'\n"
                "    num_val, _ = quad(lambda t: (m_val**3) * t * ((1.0 - t)**(m_val - 1)), 0.0, 1.0)\n"
                "    assert np.isclose(num_val, float(expected), rtol=1e-10, atol=1e-12), f'Quad mismatch at m={m_val}'\n"
                "    opts = [sp.Rational(m_val**2, m_val + 1), sp.Rational(m_val, m_val + 1),\n"
                "            sp.Rational(m_val**2, m_val - 1), sp.Rational(m_val**3, (m_val + 1) * (m_val + 3))]\n"
                "    assert len(set(opts)) == 4, f'Duplicate options at m={m_val}'\n"
                "print('VERIFIED_OK: CALC-INT-01 passed SymPy & SciPy quad across m in [2..9]')\n"
            ),
        },
        {
            "code": "CALC-INT-02",
            "agent_id": 3,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Tích phân xác định & Tích phân phụ thuộc tham số",
            "question_type": "mcq",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {
                    "type": "int",
                    "default": 3,
                    "min": 2,
                    "max": 9,
                    "step": 1,
                    "label": "Tham số m nguyên dương (m ≥ 2)",
                }
            },
            "title": "Đạo hàm dưới dấu tích phân Leibniz cho tích phân hàm Lôgarit",
            "stem_symbolic": (
                r"Cho tham số thực $m \ge 2$. Xét tích phân phụ thuộc tham số:"
                "\n"
                r"$$J(m) = \int_0^1 x^{m - 1} (\ln x)^2 \, dx$$"
                "\n"
                r"Bằng cách áp dụng quy tắc đạo hàm dưới dấu tích phân Leibniz cấp hai đối với "
                r"hàm cơ sở $F(a) = \int_0^1 x^{a - 1} \, dx = \frac{1}{a}$ $(a > 0)$ tại $a = m$, "
                r"hãy xác định giá trị của $J(m)$."
            ),
            "stem_template": (
                r"Cho $m = {m}$. Sử dụng quy tắc đạo hàm dưới dấu tích phân Leibniz (hoặc tích phân từng phần hai lần), "
                r"hãy tính tích phân:"
                "\n"
                r"$$J({m}) = \int_0^1 x^{{{m} - 1}} (\ln x)^2 \, dx$$"
            ),
            "options_symbolic": {
                "A": r"\frac{1}{m^3}",
                "B": r"\frac{2}{m^3}",
                "C": r"\frac{2}{m^2}",
                "D": r"\frac{2}{(m + 1)^3}",
            },
            "parametric_formulas": {
                "options": {
                    "A": "1 / m**3",
                    "B": "2 / m**3",
                    "C": "2 / m**2",
                    "D": "2 / (m + 1)**3",
                },
                "target_expr": "2 / m**3",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**"
                "\n\n"
                r"Xét tích phân phụ thuộc tham số $F(a) = \int_0^1 x^{a - 1} \, dx = \frac{1}{a}$ với mọi $a > 0$."
                "\n"
                r"Do hàm dưới dấu tích phân và các đạo hàm riêng theo $a$ được khống chế khả tích đều trên $\left[a_0, \infty\right)$ "
                r"với $a_0 > 0$, áp dụng định lý Leibniz lấy đạo hàm dưới dấu tích phân theo biến $a$:"
                "\n"
                r"$$F'(a) = \frac{d}{da} \int_0^1 x^{a - 1} \, dx = \int_0^1 x^{a - 1} \ln x \, dx = -\frac{1}{a^2}$$"
                "\n"
                r"Lấy đạo hàm lần thứ hai theo $a$ dưới dấu tích phân:"
                "\n"
                r"$$F''(a) = \int_0^1 x^{a - 1} (\ln x)^2 \, dx = \frac{d}{da}\left(-\frac{1}{a^2}\right) = \frac{2}{a^3}$$"
                "\n"
                r"Thay $a = m \ge 2$, ta thu được $J(m) = \frac{2}{m^3}$. Chọn đáp án **B**."
            ),
            "rubric_points": [
                "Xây dựng hàm tích phân cơ sở F(a) = int_0^1 x^(a-1) dx = 1/a (a > 0): 0.25 điểm",
                "Áp dụng quy tắc Leibniz tính đạo hàm bậc nhất F'(a) = -1/a^2: 0.5 điểm",
                "Lấy đạo hàm bậc hai F''(a) = 2/a^3 và kết luận J(m) = 2/m^3: 0.25 điểm",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-INT-02: 2nd derivative coefficient and distinctness\n"
                "def leibniz_num (k : Nat) : Nat :=\n"
                "  match k with\n"
                "  | 0 => 1\n"
                "  | n + 1 => (n + 1) * leibniz_num n\n\n"
                "theorem calc_int_02_factorial_2 : leibniz_num 2 = 2 := by rfl\n"
                "theorem calc_int_02_distinct_options :\n"
                "  List.all [2, 3, 4, 5, 6, 7, 8, 9] (fun m => (2 * (m + 1)^3 != 2 * m^3) && (2 * m^2 != 2 * m^3)) = true := by decide\n\n"
                "#eval [2, 3, 4, 5, 6, 7, 8, 9].map (fun m => (m, leibniz_num 2, m^3))\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n"
                "from scipy.integrate import quad\n\n"
                "x = sp.Symbol('x', positive=True)\n"
                "a = sp.Symbol('a', positive=True)\n"
                "F_a = sp.integrate(x**(a - 1), (x, 0, 1))\n"
                "d2F_da2 = sp.diff(F_a, a, 2)\n"
                "for m_val in range(2, 10):\n"
                "    sym_val = sp.integrate(x**(m_val - 1) * sp.log(x)**2, (x, 0, 1))\n"
                "    leibniz_val = d2F_da2.subs(a, m_val)\n"
                "    expected = sp.Rational(2, m_val**3)\n"
                "    assert sp.simplify(sym_val - expected) == 0, f'SymPy mismatch at m={m_val}'\n"
                "    assert sp.simplify(leibniz_val - expected) == 0, f'Leibniz mismatch at m={m_val}'\n"
                "    num_val, _ = quad(lambda t: (t**(m_val - 1)) * (np.log(t)**2), 0.0, 1.0)\n"
                "    assert np.isclose(num_val, float(expected), rtol=1e-9, atol=1e-12), f'Quad mismatch at m={m_val}'\n"
                "print('VERIFIED_OK: CALC-INT-02 passed SymPy, Leibniz diff & SciPy quad across m in [2..9]')\n"
            ),
        },
        {
            "code": "CALC-INT-03",
            "agent_id": 3,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Tích phân xác định & Tích phân phụ thuộc tham số",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {
                    "type": "int",
                    "default": 3,
                    "min": 2,
                    "max": 9,
                    "step": 1,
                    "label": "Tham số m nguyên dương (m ≥ 2)",
                }
            },
            "title": "Bài toán Tự luận Tổng hợp: Đổi biến số, Tích phân từng phần & Đạo hàm dưới dấu tích phân Leibniz",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \ge 2$. Xét hai tích phân phụ thuộc tham số sau:"
                "\n"
                r"$$I_1(m) = \int_0^1 x\left(1 - x^2\right)^{m - 1} \, dx, \qquad "
                r"I_2(m) = \int_0^{\infty} x^2 e^{-m x} \, dx$$"
                "\n"
                r"**a)** Sử dụng phương pháp đổi biến số $u = 1 - x^2$, hãy tính $I_1(m)$ theo $m$."
                "\n"
                r"**b)** Sử dụng quy tắc đạo hàm dưới dấu tích phân Leibniz đối với tích phân Laplace cơ sở "
                r"$L(a) = \int_0^{\infty} e^{-a x} \, dx = \frac{1}{a}$ $(a > 0)$ hoặc tích phân từng phần hai lần, "
                r"hãy tính $I_2(m)$ theo $m$."
                "\n"
                r"**c)** Tính tỷ số chuẩn hóa $S(m) = \dfrac{I_2(m)}{I_1(m)}$ theo $m$."
            ),
            "stem_template": (
                r"Cho $m = {m}$. Xét hai tích phân:"
                "\n"
                r"$$I_1({m}) = \int_0^1 x\left(1 - x^2\right)^{{{m} - 1}} \, dx, \qquad "
                r"I_2({m}) = \int_0^{{\infty}} x^2 e^{{-{m} x}} \, dx$$"
                "\n"
                r"**a)** Tính $I_1({m})$ bằng phương pháp đổi biến $u = 1 - x^2$."
                "\n"
                r"**b)** Tính $I_2({m})$ bằng quy tắc đạo hàm dưới dấu tích phân Leibniz (hoặc tích phân từng phần)."
                "\n"
                r"**c)** Xác định giá trị chính xác của tỷ số $S({m}) = \dfrac{{I_2({m})}}{{I_1({m})}}$."
            ),
            "options_symbolic": {
                "A": r"\frac{4}{m^2}",
                "B": r"\frac{2}{m^2}",
                "C": r"\frac{4}{m^3}",
                "D": r"\frac{1}{m^2}",
            },
            "parametric_formulas": {
                "options": {
                    "A": "4 / m**2",
                    "B": "2 / m**2",
                    "C": "4 / m**3",
                    "D": "1 / m**2",
                },
                "target_expr": "4 / m**2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải tự luận chi tiết:**"
                "\n\n"
                r"**Phần a) Tính $I_1(m)$ bằng đổi biến số:**"
                "\n"
                r"Đặt $u = 1 - x^2 \implies du = -2x \, dx \iff x \, dx = -\frac{1}{2} du$. "
                r"Đổi cận: khi $x = 0 \implies u = 1$; khi $x = 1 \implies u = 0$. Khi đó:"
                "\n"
                r"$$I_1(m) = \frac{1}{2} \int_0^1 u^{m - 1} \, du = \left[ \frac{u^m}{2m} \right]_0^1 = \frac{1}{2m}$$"
                "\n\n"
                r"**Phần b) Tính $I_2(m)$ bằng quy tắc Leibniz & kiểm chứng tích phân từng phần:**"
                "\n"
                r"Xét hàm $L(a) = \int_0^{\infty} e^{-a x} \, dx = \frac{1}{a}$ với $a > 0$. "
                r"Trên mọi miền $[a_0, \infty)$ với $a_0 > 0$, hàm $x^k e^{-a x} \le x^k e^{-a_0 x}$ khả tích Lebesgue trên $[0, \infty)$. "
                r"Áp dụng quy tắc đạo hàm dưới dấu tích phân Leibniz hai lần theo $a$:"
                "\n"
                r"$$L'(a) = -\int_0^{\infty} x e^{-a x} \, dx = -\frac{1}{a^2} "
                r"\implies L''(a) = \int_0^{\infty} x^2 e^{-a x} \, dx = \frac{2}{a^3}$$"
                "\n"
                r"Thay $a = m$, ta được $I_2(m) = \frac{2}{m^3}$."
                "\n\n"
                r"**Phần c) Tính tỷ số $S(m)$:**"
                "\n"
                r"$$S(m) = \frac{I_2(m)}{I_1(m)} = \frac{2 / m^3}{1 / (2m)} = \frac{4}{m^2}$$"
            ),
            "rubric_points": [
                "Phần a (0.75 điểm): Đổi biến u = 1 - x^2, đổi cận chính xác và tính được I_1(m) = 1 / (2m)",
                "Phần b (1.00 điểm): Kiểm tra điều kiện hội tụ đều và áp dụng quy tắc Leibniz cấp hai (hoặc từng phần 2 lần) thu được I_2(m) = 2 / m^3",
                "Phần c (0.25 điểm): Rút gọn chính xác tỷ số S(m) = I_2(m) / I_1(m) = 4 / m^2",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-INT-03: S(m) = (2 / m^3) / (1 / (2*m)) = 4 / m^2\n"
                "-- Cleared denominators identity: (2 * (2 * m)) * m^2 = 4 * m^3\n"
                "def s_lhs (m : Nat) : Nat := (2 * (2 * m)) * (m^2)\n"
                "def s_rhs (m : Nat) : Nat := 4 * (m^3)\n\n"
                "theorem calc_int_03_m3 : s_lhs 3 = s_rhs 3 := by decide\n"
                "theorem calc_int_03_grid : List.all [2, 3, 4, 5, 6, 7, 8, 9] (fun m => s_lhs m == s_rhs m) = true := by decide\n\n"
                "#eval [2, 3, 4, 5, 6, 7, 8, 9].map (fun m => (m, 4, m * m))\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n"
                "from scipy.integrate import quad\n\n"
                "x = sp.Symbol('x', real=True, nonnegative=True)\n"
                "for m_val in range(2, 10):\n"
                "    i1_sym = sp.integrate(x * (1 - x**2)**(m_val - 1), (x, 0, 1))\n"
                "    i2_sym = sp.integrate((x**2) * sp.exp(-m_val * x), (x, 0, sp.oo))\n"
                "    assert sp.simplify(i1_sym - sp.Rational(1, 2 * m_val)) == 0\n"
                "    assert sp.simplify(i2_sym - sp.Rational(2, m_val**3)) == 0\n"
                "    s_sym = sp.simplify(i2_sym / i1_sym)\n"
                "    expected_s = sp.Rational(4, m_val**2)\n"
                "    assert sp.simplify(s_sym - expected_s) == 0\n"
                "    i1_num, _ = quad(lambda t: t * ((1.0 - t**2)**(m_val - 1)), 0.0, 1.0)\n"
                "    i2_num, _ = quad(lambda t: (t**2) * np.exp(-m_val * t), 0.0, np.inf)\n"
                "    assert np.isclose(i2_num / i1_num, float(expected_s), rtol=1e-9, atol=1e-11)\n"
                "print('VERIFIED_OK: CALC-INT-03 passed SymPy & SciPy quad for I1, I2, S across m in [2..9]')\n"
            ),
        },
    ]
