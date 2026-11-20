"""
Agent-10: Giải tích — Phương trình vi phân cấp 1, cấp 2 & Hệ PTVP chứa tham số.
Sinh & kiểm chứng câu hỏi PTVP tuyến tính cấp 1, cấp 2, Bài toán Cauchy & Hệ PTVP
bằng SymPy (symbolic diff + numerical parameter grid) và Core Lean 4.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 10,
    "agent_code": "AGENT-10",
    "agent_name": "Agent-10 (Giải tích: Phương trình vi phân cấp 1, 2 & Hệ PTVP)",
    "domain": "Giải tích",
    "role_desc": "Sinh & kiểm chứng câu hỏi Phương trình vi phân tuyến tính cấp 1, cấp 2, Bài toán Cauchy & Hệ PTVP chứa tham số",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa của Agent-10 (2 MCQ, 1 Essay)."""
    return [
        {
            "code": "CALC-ODE-01",
            "agent_id": 10,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Phương trình vi phân & Bài toán Cauchy có tham số",
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
                    "label": "Tham số nguyên dương m",
                }
            },
            "title": "Bài toán Cauchy cho phương trình vi phân tuyến tính cấp 1 có tham số",
            "stem_symbolic": (
                r"Xét bài toán Cauchy cho phương trình vi phân tuyến tính cấp 1 chứa tham số nguyên dương $m \in [2, 9]$:"
                "\n"
                r"$$y' + m y = m^2 e^{-m x}, \quad y(0) = m$$"
                "\n"
                r"Gọi $y(x)$ là nghiệm duy nhất của bài toán trên $\mathbb{R}$. Đặt $I(m) = e^{m} \cdot y(1)$. "
                r"Biểu thức của $I(m)$ theo $m$ là:"
            ),
            "stem_template": (
                r"Xét bài toán Cauchy cho phương trình vi phân tuyến tính cấp 1 (với $m = {m}$):"
                "\n"
                r"$$y' + {m} y = {m}^2 e^{{-{m} x}}, \quad y(0) = {m}$$"
                "\n"
                r"Gọi $y(x)$ là nghiệm duy nhất của bài toán trên $\mathbb{R}$. Tính giá trị biểu thức $I({m}) = e^{{{m}}} \cdot y(1)$."
            ),
            "options_symbolic": {
                "A": r"$m^2 + m$",
                "B": r"$m^2 + 2m + 1$",
                "C": r"$2m^2 + m + 1$",
                "D": r"$m^2 - 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2 + m",
                    "B": "m**2 + 2*m + 1",
                    "C": "2*m**2 + m + 1",
                    "D": "m**2 - 1",
                },
                "target_expr": "m**2 + m",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Bước 1 (Thừa số tích phân):** Phương trình vi phân tuyến tính cấp 1 chuẩn tắc có dạng "
                r"$y' + P(x)y = Q(x)$ với $P(x) = m$ và $Q(x) = m^2 e^{-mx}$. "
                r"Thừa số tích phân là $\mu(x) = e^{\int m\,dx} = e^{mx}$."
                "\n\n"
                r"**Bước 2 (Tích phân hai vế):** Nhân hai vế với $e^{mx}$, ta được:"
                "\n"
                r"$$\frac{d}{dx}\left(e^{mx} y(x)\right) = m^2 \implies e^{mx} y(x) = m^2 x + C$$"
                "\n\n"
                r"**Bước 3 (Khử hằng số từ điều kiện đầu Cauchy):** Thay $x = 0, y(0) = m$:"
                "\n"
                r"$$e^{0} \cdot m = m^2 \cdot 0 + C \implies C = m$$"
                "\n"
                r"Do đó nghiệm của bài toán Cauchy là $y(x; m) = (m^2 x + m)e^{-mx}$."
                "\n\n"
                r"**Bước 4 (Tính giá trị tại $x = 1$):**"
                "\n"
                r"$$I(m) = e^{m} \cdot y(1) = e^{m} \cdot (m^2 \cdot 1 + m)e^{-m} = m^2 + m$$"
                "\n"
                r"Vậy đáp án đúng là **A**."
            ),
            "rubric_points": 1.0,
            "lean4_code": (
                "-- Core Lean 4 verification for CALC-ODE-01 (No Mathlib, No sorry)\n"
                "-- After multiplying by e^(mx), the polynomial factor is P(x) = m^2 * x + C.\n"
                "-- With y(0) = m => C = m, so at x = 1, I(m) = e^m * y(1) = m^2 + m.\n\n"
                "def polyFactor (m x c : Nat) : Nat := m * m * x + c\n"
                "def targetI (m : Nat) : Nat := polyFactor m 1 m\n\n"
                "theorem calc_ode_01_at_m3 : targetI 3 = 12 := by decide\n"
                "theorem calc_ode_01_formula (m : Nat) : targetI m = m * m + m := by\n"
                "  simp [targetI, polyFactor]\n\n"
                "theorem calc_ode_01_distinct_m3 :\n"
                "    targetI 3 ≠ 3 * 3 + 2 * 3 + 1 ∧\n"
                "    targetI 3 ≠ 2 * (3 * 3) + 3 + 1 ∧\n"
                "    targetI 3 ≠ 3 * 3 - 1 := by decide\n\n"
                "#eval targetI 3\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "def verify_calc_ode_01():\n"
                "    x = sp.Symbol('x', real=True)\n"
                "    m = sp.Symbol('m', integer=True, positive=True)\n"
                "    y = (m**2 * x + m) * sp.exp(-m * x)\n"
                "    ode_res = sp.simplify(sp.diff(y, x) + m * y - m**2 * sp.exp(-m * x))\n"
                "    ic_res = sp.simplify(y.subs(x, 0) - m)\n"
                "    assert ode_res == 0, f'ODE residual non-zero: {ode_res}'\n"
                "    assert ic_res == 0, f'IC residual non-zero: {ic_res}'\n"
                "    I_expr = sp.simplify(sp.exp(m) * y.subs(x, 1))\n"
                "    assert sp.simplify(I_expr - (m**2 + m)) == 0\n"
                "    for m_val in range(2, 10):\n"
                "        y_num = y.subs(m, m_val)\n"
                "        assert sp.simplify(sp.diff(y_num, x) + m_val * y_num - m_val**2 * sp.exp(-m_val * x)) == 0\n"
                "        assert int(I_expr.subs(m, m_val)) == m_val**2 + m_val\n"
                "    print('VERIFIED_OK: CALC-ODE-01 | I(3) =', int(I_expr.subs(m, 3)))\n\n"
                "if __name__ == '__main__':\n"
                "    verify_calc_ode_01()\n"
            ),
        },
        {
            "code": "CALC-ODE-02",
            "agent_id": 10,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Phương trình vi phân & Bài toán Cauchy có tham số",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": {
                "m": {
                    "type": "int",
                    "default": 3,
                    "min": 2,
                    "max": 9,
                    "step": 1,
                    "label": "Tham số nguyên dương m",
                }
            },
            "title": "Bài toán Cauchy cho phương trình vi phân tuyến tính cấp 2 hệ số hằng có tham số",
            "stem_symbolic": (
                r"Cho bài toán Cauchy đối với phương trình vi phân tuyến tính cấp 2 chứa tham số nguyên dương $m \in [2, 9]$:"
                "\n"
                r"$$y'' - 3m y' + 2m^2 y = 0, \quad y(0) = m + 1, \quad y'(0) = m^2 + 2m$$"
                "\n"
                r"Tính giá trị của nghiệm tại điểm $x_0 = \frac{\ln 2}{m}$, tức là biểu thức $S(m) = y\left(\frac{\ln 2}{m}\right)$:"
            ),
            "stem_template": (
                r"Cho bài toán Cauchy đối với phương trình vi phân tuyến tính cấp 2 (với $m = {m}$):"
                "\n"
                r"$$y'' - 3\cdot {m} y' + 2\cdot {m}^2 y = 0, \quad y(0) = {m} + 1, \quad y'(0) = {m}^2 + 2\cdot {m}$$"
                "\n"
                r"Tính giá trị $S({m}) = y\left(\frac{{\ln 2}}{{{m}}}\right)$."
            ),
            "options_symbolic": {
                "A": r"$m + 2$",
                "B": r"$2m + 4$",
                "C": r"$3m + 4$",
                "D": r"$4m + 5$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m + 2",
                    "B": "2*m + 4",
                    "C": "3*m + 4",
                    "D": "4*m + 5",
                },
                "target_expr": "2*m + 4",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Bước 1 (Phương trình đặc trưng):** Phương trình đặc trưng của PTVP thuần nhất cấp 2 là:"
                "\n"
                r"$$\lambda^2 - 3m\lambda + 2m^2 = 0 \iff (\lambda - m)(\lambda - 2m) = 0 \iff \lambda_1 = m,\; \lambda_2 = 2m$$"
                "\n"
                r"Nghiệm tổng quát có dạng $y(x) = C_1 e^{mx} + C_2 e^{2mx}$."
                "\n\n"
                r"**Bước 2 (Xác định hằng số từ điều kiện đầu Cauchy):**"
                "\n"
                r"Ta có $y'(x) = m C_1 e^{mx} + 2m C_2 e^{2mx}$. Tại $x = 0$:"
                "\n"
                r"$$\begin{cases} C_1 + C_2 = m + 1 \\ m C_1 + 2m C_2 = m^2 + 2m \end{cases} "
                r"\iff \begin{cases} C_1 + C_2 = m + 1 \\ C_1 + 2C_2 = m + 2 \end{cases} "
                r"\iff \begin{cases} C_1 = m \\ C_2 = 1 \end{cases}$$"
                "\n"
                r"Suy ra nghiệm duy nhất là $y(x; m) = m e^{mx} + e^{2mx}$."
                "\n\n"
                r"**Bước 3 (Tính giá trị tại $x_0 = \frac{\ln 2}{m}$):**"
                "\n"
                r"Vì $e^{m x_0} = e^{\ln 2} = 2$ và $e^{2m x_0} = 2^2 = 4$, ta có:"
                "\n"
                r"$$S(m) = y\left(\frac{\ln 2}{m}\right) = m \cdot 2 + 4 = 2m + 4$$"
                "\n"
                r"Vậy đáp án đúng là **B**."
            ),
            "rubric_points": 1.0,
            "lean4_code": (
                "-- Core Lean 4 verification for CALC-ODE-02 (No Mathlib, No sorry)\n"
                "-- Characteristic polynomial: r^2 - 3*m*r + 2*m^2 = (r - m)*(r - 2*m)\n"
                "-- Evaluated at e^(m*x0) = 2: S(m) = C1 * 2 + C2 * 4 where C1 = m, C2 = 1.\n\n"
                "def charPoly (m r : Int) : Int := r * r - 3 * m * r + 2 * m * m\n"
                "def targetS (m : Nat) : Nat := m * 2 + 1 * 4\n\n"
                "theorem calc_ode_02_roots_m3 : charPoly 3 3 = 0 ∧ charPoly 3 6 = 0 := by decide\n"
                "theorem calc_ode_02_at_m3 : targetS 3 = 10 := by decide\n"
                "theorem calc_ode_02_formula (m : Nat) : targetS m = 2 * m + 4 := by unfold targetS; omega\n\n"
                "#eval targetS 3\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "def verify_calc_ode_02():\n"
                "    x = sp.Symbol('x', real=True)\n"
                "    m = sp.Symbol('m', integer=True, positive=True)\n"
                "    y = m * sp.exp(m * x) + sp.exp(2 * m * x)\n"
                "    ode_res = sp.simplify(sp.diff(y, x, 2) - 3 * m * sp.diff(y, x) + 2 * m**2 * y)\n"
                "    ic0_res = sp.simplify(y.subs(x, 0) - (m + 1))\n"
                "    ic1_res = sp.simplify(sp.diff(y, x).subs(x, 0) - (m**2 + 2 * m))\n"
                "    assert ode_res == 0, f'ODE residual: {ode_res}'\n"
                "    assert ic0_res == 0, f'IC y(0) residual: {ic0_res}'\n"
                "    assert ic1_res == 0, f'IC y_prime(0) residual: {ic1_res}'\n"
                "    S_expr = sp.simplify(y.subs(x, sp.log(2) / m))\n"
                "    assert sp.simplify(S_expr - (2 * m + 4)) == 0\n"
                "    for m_val in range(2, 10):\n"
                "        assert int(S_expr.subs(m, m_val)) == 2 * m_val + 4\n"
                "    print('VERIFIED_OK: CALC-ODE-02 | S(3) =', int(S_expr.subs(m, 3)))\n\n"
                "if __name__ == '__main__':\n"
                "    verify_calc_ode_02()\n"
            ),
        },
        {
            "code": "CALC-ODE-03",
            "agent_id": 10,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Phương trình vi phân & Bài toán Cauchy có tham số",
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
                    "label": "Tham số nguyên dương m",
                }
            },
            "title": "Hệ phương trình vi phân tuyến tính cấp 1 thuần nhất & Bài toán Cauchy có tham số",
            "stem_symbolic": (
                r"Cho hệ phương trình vi phân tuyến tính cấp 1 thuần nhất chứa tham số nguyên dương $m \in [2, 9]$:"
                "\n"
                r"$$\begin{cases} x'(t) = m x(t) + m y(t) \\ y'(t) = m x(t) + m y(t) \end{cases}, \quad "
                r"x(0) = 3m, \quad y(0) = m$$"
                "\n"
                r"a) Tìm đa thức đặc trưng, các giá trị riêng và nghiệm tổng quát $(x(t), y(t))$ của hệ."
                "\n"
                r"b) Xác định nghiệm riêng thỏa mãn điều kiện đầu Cauchy và tính giá trị tích "
                r"$P(m) = x\left(\frac{\ln 2}{2m}\right) \cdot y\left(\frac{\ln 2}{2m}\right)$ theo $m$."
            ),
            "stem_template": (
                r"Cho hệ phương trình vi phân tuyến tính cấp 1 thuần nhất (với $m = {m}$):"
                "\n"
                r"$$\begin{cases} x'(t) = {m} x(t) + {m} y(t) \\ y'(t) = {m} x(t) + {m} y(t) \end{cases}, \quad "
                r"x(0) = 3\cdot {m}, \quad y(0) = {m}$$"
                "\n"
                r"a) Tìm đa thức đặc trưng, các giá trị riêng và nghiệm tổng quát $(x(t), y(t))$ của hệ."
                "\n"
                r"b) Xác định nghiệm riêng thỏa mãn điều kiện đầu Cauchy và tính giá trị tích "
                r"$P({m}) = x\left(\frac{{\ln 2}}{{2\cdot {m}}}\right) \cdot y\left(\frac{{\ln 2}}{{2\cdot {m}}}\right)$."
            ),
            "options_symbolic": {
                "A": r"$12m^2$",
                "B": r"$14m^2$",
                "C": r"$15m^2$",
                "D": r"$18m^2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "12*m**2",
                    "B": "14*m**2",
                    "C": "15*m**2",
                    "D": "18*m**2",
                },
                "target_expr": "15*m**2",
            },
            "correct_option": "C",
            "solution_symbolic": (
                r"**a) Tìm giá trị riêng và nghiệm tổng quát (1.5 điểm):**"
                "\n"
                r"Ma trận hệ số của hệ là $A = \begin{pmatrix} m & m \\ m & m \end{pmatrix}$."
                "\n"
                r"Phương trình đặc trưng: $\det(A - \lambda I) = (m-\lambda)^2 - m^2 = \lambda(\lambda - 2m) = 0$."
                "\n"
                r"- Với $\lambda_1 = 0$: hệ $(A - 0I)v = 0 \iff x + y = 0$, chọn vectơ riêng $v_1 = (1, -1)^T$."
                "\n"
                r"- Với $\lambda_2 = 2m$: hệ $(A - 2mI)v = 0 \iff -x + y = 0$, chọn vectơ riêng $v_2 = (1, 1)^T$."
                "\n"
                r"Nghiệm tổng quát của hệ là:"
                "\n"
                r"$$\begin{cases} x(t) = C_1 + C_2 e^{2mt} \\ y(t) = -C_1 + C_2 e^{2mt} \end{cases} \quad (C_1, C_2 \in \mathbb{R})$$"
                "\n\n"
                r"**b) Giải bài toán Cauchy và tính $P(m)$ (1.5 điểm):**"
                "\n"
                r"Thay điều kiện đầu $x(0) = 3m, y(0) = m$:"
                "\n"
                r"$$\begin{cases} C_1 + C_2 = 3m \\ -C_1 + C_2 = m \end{cases} \iff \begin{cases} C_1 = m \\ C_2 = 2m \end{cases}$$"
                "\n"
                r"Nghiệm riêng của bài toán Cauchy là:"
                "\n"
                r"$$\begin{cases} x(t; m) = m + 2m e^{2mt} \\ y(t; m) = -m + 2m e^{2mt} \end{cases}$$"
                "\n"
                r"Tại $t_0 = \frac{\ln 2}{2m}$, ta có $e^{2m t_0} = 2$, suy ra:"
                "\n"
                r"$$x(t_0) = m + 4m = 5m, \quad y(t_0) = -m + 4m = 3m$$"
                "\n"
                r"Do đó $P(m) = x(t_0) \cdot y(t_0) = (5m)(3m) = 15m^2$."
            ),
            "rubric_points": 3.0,
            "lean4_code": (
                "-- Core Lean 4 verification for CALC-ODE-03 (No Mathlib, No sorry)\n"
                "-- System at t0 = ln(2)/(2m) has e^(2m*t0) = 2, C1 = m, C2 = 2m.\n"
                "-- x(t0) = C1 + 2*C2 = 5m, y(t0) = -C1 + 2*C2 = 3m, P(m) = 15*m^2.\n\n"
                "def xAtT0 (m : Nat) : Nat := m + 2 * (2 * m)\n"
                "def yAtT0 (m : Nat) : Nat := 2 * (2 * m) - m\n"
                "def targetP (m : Nat) : Nat := xAtT0 m * yAtT0 m\n\n"
                "theorem calc_ode_03_components (m : Nat) : xAtT0 m = 5 * m ∧ yAtT0 m = 3 * m := by\n"
                "  unfold xAtT0 yAtT0; constructor <;> omega\n\n"
                "theorem calc_ode_03_at_m3 : targetP 3 = 135 := by decide\n\n"
                "#eval targetP 3\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "def verify_calc_ode_03():\n"
                "    t = sp.Symbol('t', real=True)\n"
                "    m = sp.Symbol('m', integer=True, positive=True)\n"
                "    x_sol = m + 2 * m * sp.exp(2 * m * t)\n"
                "    y_sol = -m + 2 * m * sp.exp(2 * m * t)\n"
                "    res1 = sp.simplify(sp.diff(x_sol, t) - (m * x_sol + m * y_sol))\n"
                "    res2 = sp.simplify(sp.diff(y_sol, t) - (m * x_sol + m * y_sol))\n"
                "    assert res1 == 0 and res2 == 0, f'System ODE residuals: {res1}, {res2}'\n"
                "    assert sp.simplify(x_sol.subs(t, 0) - 3 * m) == 0\n"
                "    assert sp.simplify(y_sol.subs(t, 0) - m) == 0\n"
                "    t0 = sp.log(2) / (2 * m)\n"
                "    P_expr = sp.simplify(x_sol.subs(t, t0) * y_sol.subs(t, t0))\n"
                "    assert sp.simplify(P_expr - 15 * m**2) == 0\n"
                "    for m_val in range(2, 10):\n"
                "        assert int(P_expr.subs(m, m_val)) == 15 * m_val**2\n"
                "    print('VERIFIED_OK: CALC-ODE-03 | P(3) =', int(P_expr.subs(m, 3)))\n\n"
                "if __name__ == '__main__':\n"
                "    verify_calc_ode_03()\n"
            ),
        },
    ]
