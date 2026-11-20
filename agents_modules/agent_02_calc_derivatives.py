"""
Agent-02: Giải tích — Đạo hàm cấp cao & Cực trị hàm một biến chứa tham số.
Sinh và kiểm chứng tự động (SymPy + NumPy + Lean 4 Core) 3 câu hỏi chuẩn:
- CALC-DER-01 (MCQ): Đạo hàm cấp cao theo công thức Leibniz
- CALC-DER-02 (MCQ): Cực trị hàm bậc ba chứa tham số m
- CALC-DER-03 (Essay): Khảo sát cực trị & điểm uốn hàm trùng phương chứa tham số m
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 2,
    "agent_code": "AGENT-02",
    "agent_name": "Agent-02 (Giải tích: Đạo hàm cấp cao & Cực trị 1 biến)",
    "domain": "Giải tích",
    "role_desc": "Sinh & kiểm chứng câu hỏi Đạo hàm cấp cao Leibnitz, Tiếp tuyến & Cực trị hàm 1 biến chứa tham số",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi (2 MCQ, 1 Essay) của Agent-02."""
    return [
        {
            "code": "CALC-DER-01",
            "agent_id": 2,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Đạo hàm cấp cao & Cực trị hàm một biến",
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
                    "label": "Tham số m",
                }
            },
            "title": "Đạo hàm cấp 4 theo công thức Leibniz tại x = 0",
            "stem_symbolic": (
                r"Cho hàm số $f(x) = x^2 e^{mx}$ với tham số nguyên dương $m \in [2, 9]$. "
                r"Áp dụng công thức Leibniz cho đạo hàm cấp cao của tích hai hàm số, "
                r"giá trị của đạo hàm cấp 4 tại $x = 0$, tức là $f^{(4)}(0)$, bằng:"
            ),
            "stem_template": (
                r"Cho hàm số $f(x) = x^2 e^{{{m}}x}$ (với $m = {m}$). "
                r"Áp dụng công thức Leibniz, hãy tính giá trị của đạo hàm cấp 4 tại $x = 0$, tức là $f^{{(4)}}(0)$."
            ),
            "options_symbolic": {
                "A": r"$12m^2$",
                "B": r"$6m^2$",
                "C": r"$24m^2$",
                "D": r"$12m^4$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "12*m**2",
                    "B": "6*m**2",
                    "C": "24*m**2",
                    "D": "12*m**4",
                },
                "target_expr": "12*m**2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết (Công thức Leibniz):**" "\n\n"
                r"Đặt $u(x) = x^2$ và $v(x) = e^{mx}$. Ta có các đạo hàm của $u(x)$:" "\n"
                r"$$u(0) = 0, \quad u'(0) = 0, \quad u''(0) = 2, \quad u^{(k)}(x) = 0 \;\; (\forall k \ge 3).$$" "\n"
                r"Đạo hàm cấp $j$ của $v(x)$ là $v^{(j)}(x) = m^j e^{mx} \implies v^{(j)}(0) = m^j$." "\n\n"
                r"Theo công thức Leibniz cho đạo hàm cấp $n = 4$ tại $x = 0$:" "\n"
                r"$$f^{(4)}(0) = \sum_{k=0}^{4} \binom{4}{k} u^{(k)}(0) v^{(4-k)}(0) "
                r"= \binom{4}{2} u''(0) v''(0) = 6 \cdot 2 \cdot m^2 = 12m^2.$$" "\n"
                r"Vậy đáp án đúng là **A** ($12m^2$)."
            ),
            "rubric_points": 1.0,
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-DER-01: Leibniz 4th derivative coefficient\n"
                "def binom4_2 : Nat := 6\n"
                "def u_second_deriv : Nat := 2\n"
                "def f4_at_zero (m : Nat) : Nat := binom4_2 * u_second_deriv * (m ^ 2)\n\n"
                "theorem calc_der_01_m3 : f4_at_zero 3 = 108 := by decide\n"
                "theorem calc_der_01_m5 : f4_at_zero 5 = 300 := by decide\n"
                "theorem calc_der_01_formula (m : Nat) : f4_at_zero m = 12 * (m ^ 2) := by rfl\n\n"
                "#eval f4_at_zero 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "x, m = sp.symbols('x m', real=True)\n"
                "f_expr = (x**2) * sp.exp(m * x)\n"
                "d4_symbolic = sp.simplify(sp.diff(f_expr, x, 4).subs(x, 0))\n"
                "expected_symbolic = 12 * m**2\n"
                "assert sp.simplify(d4_symbolic - expected_symbolic) == 0, f'Symbolic mismatch: {d4_symbolic}'\n\n"
                "# Kiểm chứng sai phân hữu hạn bậc 4 trên lưới tham số m in [2..9]\n"
                "h = 1e-3\n"
                "for m_val in range(2, 10):\n"
                "    fn = lambda t: (t**2) * np.exp(m_val * t)\n"
                "    num_d4 = (fn(-2*h) - 4*fn(-h) + 6*fn(0.0) - 4*fn(h) + fn(2*h)) / (h**4)\n"
                "    exact_val = float(12 * (m_val**2))\n"
                "    assert abs(num_d4 - exact_val) / exact_val < 1e-4, f'Grid failure at m={m_val}: {num_d4} vs {exact_val}'\n\n"
                "print('VERIFIED_OK: CALC-DER-01 symbolic diff & finite-difference grid [2..9] passed (12*m**2)')\n"
            ),
        },
        {
            "code": "CALC-DER-02",
            "agent_id": 2,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Đạo hàm cấp cao & Cực trị hàm một biến",
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
                    "label": "Tham số m",
                }
            },
            "title": "Hiệu giá trị cực đại và cực tiểu của hàm bậc ba chứa tham số",
            "stem_symbolic": (
                r"Cho hàm số $f(x) = x^3 - 3mx^2 + 4m^3$ với tham số nguyên dương $m \in [2, 9]$. "
                r"Gọi $y_{\text{CĐ}}$ và $y_{\text{CT}}$ lần lượt là giá trị cực đại và giá trị cực tiểu của hàm số trên $\mathbb{R}$. "
                r"Hiệu số $\Delta y = y_{\text{CĐ}} - y_{\text{CT}}$ tính theo $m$ bằng:"
            ),
            "stem_template": (
                r"Cho hàm số $f(x) = x^3 - 3({m})x^2 + 4({m})^3$ (với $m = {m}$). "
                r"Tính hiệu số $\Delta y = y_{{\text{{CĐ}}}} - y_{{\text{{CT}}}}$ giữa giá trị cực đại và giá trị cực tiểu của hàm số."
            ),
            "options_symbolic": {
                "A": r"$2m^3$",
                "B": r"$4m^3$",
                "C": r"$8m^3$",
                "D": r"$6m^3$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m**3",
                    "B": "4*m**3",
                    "C": "8*m**3",
                    "D": "6*m**3",
                },
                "target_expr": "4*m**3",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"1. Tính đạo hàm bậc nhất và bậc hai theo $x$:" "\n"
                r"$$f'(x) = 3x^2 - 6mx = 3x(x - 2m), \quad f''(x) = 6x - 6m.$$" "\n"
                r"2. Phương trình $f'(x) = 0 \iff x = 0$ hoặc $x = 2m$ (do $m \ge 2 > 0$)." "\n"
                r"- Tại $x = 0$: $f''(0) = -6m < 0 \implies x = 0$ là điểm cực đại, $y_{\text{CĐ}} = f(0) = 4m^3$." "\n"
                r"- Tại $x = 2m$: $f''(2m) = 6m > 0 \implies x = 2m$ là điểm cực tiểu, "
                r"$y_{\text{CT}} = f(2m) = (2m)^3 - 3m(2m)^2 + 4m^3 = 8m^3 - 12m^3 + 4m^3 = 0$." "\n\n"
                r"3. Do đó hiệu số giá trị cực trị là:" "\n"
                r"$$\Delta y = y_{\text{CĐ}} - y_{\text{CT}} = 4m^3 - 0 = 4m^3.$$" "\n"
                r"Vậy đáp án đúng là **B** ($4m^3$)."
            ),
            "rubric_points": 1.0,
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-DER-02: Cubic Extrema Gap\n"
                "def f_cubic (m x : Int) : Int := x^3 - 3 * m * (x^2) + 4 * (m^3)\n"
                "def df_cubic (m x : Int) : Int := 3 * (x^2) - 6 * m * x\n"
                "def delta_y (m : Int) : Int := f_cubic m 0 - f_cubic m (2 * m)\n\n"
                "theorem calc_der_02_crit_0 : (List.range 10).all (fun k => df_cubic (Int.ofNat (k + 1)) 0 == 0) = true := by decide\n"
                "theorem calc_der_02_m3 : delta_y 3 = 108 := by decide\n"
                "theorem calc_der_02_m4 : delta_y 4 = 256 := by decide\n\n"
                "#eval delta_y 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "x = sp.Symbol('x', real=True)\n"
                "m = sp.Symbol('m', positive=True)\n"
                "f_expr = x**3 - 3*m*x**2 + 4*m**3\n"
                "df = sp.diff(f_expr, x)\n"
                "d2f = sp.diff(f_expr, x, 2)\n"
                "crit_pts = sp.solve(df, x)\n"
                "y_max = f_expr.subs(x, 0)\n"
                "y_min = sp.simplify(f_expr.subs(x, 2*m))\n"
                "delta_sym = sp.simplify(y_max - y_min)\n"
                "assert sp.simplify(delta_sym - 4*m**3) == 0, f'Expected 4*m**3, got {delta_sym}'\n\n"
                "# Kiểm chứng số học và sai phân đạo hàm trên lưới tham số m in [2..9]\n"
                "h = 1e-6\n"
                "for m_val in range(2, 10):\n"
                "    fn = lambda t: t**3 - 3*m_val*(t**2) + 4*(m_val**3)\n"
                "    df_0 = (fn(h) - fn(-h)) / (2*h)\n"
                "    df_2m = (fn(2*m_val + h) - fn(2*m_val - h)) / (2*h)\n"
                "    assert abs(df_0) < 1e-7 and abs(df_2m) < 1e-6\n"
                "    gap = fn(0.0) - fn(2.0 * m_val)\n"
                "    assert abs(gap - 4*(m_val**3)) < 1e-8\n\n"
                "print('VERIFIED_OK: CALC-DER-02 symbolic extrema & numerical grid [2..9] passed (4*m**3)')\n"
            ),
        },
        {
            "code": "CALC-DER-03",
            "agent_id": 2,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Đạo hàm cấp cao & Cực trị hàm một biến",
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
                    "label": "Tham số m",
                }
            },
            "title": "Khảo sát cực trị hàm trùng phương và bất biến đại số tại các điểm dừng",
            "stem_symbolic": (
                r"Cho hàm số trùng phương $f(x) = x^4 - 2m^2 x^2 + m^4$ với tham số nguyên dương $m \in [2, 9]$. "
                r"Hãy xác định tất cả các điểm cực đại, cực tiểu của hàm số; tính giá trị cực đại $y_{\text{CĐ}} = f(0)$ "
                r"và tổng bình phương hoành độ hai điểm cực tiểu $S_x = x_1^2 + x_2^2$. "
                r"Từ đó chứng minh biểu thức đặc trưng $T(m) = y_{\text{CĐ}} + m^2(x_1^2 + x_2^2) = 3m^4$."
            ),
            "stem_template": (
                r"Cho hàm số $f(x) = x^4 - 2({m})^2 x^2 + ({m})^4$ (với $m = {m}$). "
                r"Tìm các điểm cực đại, cực tiểu của hàm số và tính giá trị biểu thức "
                r"$T({m}) = y_{{\text{{CĐ}}}} + {m}^2(x_1^2 + x_2^2)$, trong đó $x_1, x_2$ là hoành độ hai điểm cực tiểu."
            ),
            "options_symbolic": {
                "A": r"$m^4$",
                "B": r"$2m^4$",
                "C": r"$3m^4$",
                "D": r"$4m^4$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**4",
                    "B": "2*m**4",
                    "C": "3*m**4",
                    "D": "4*m**4",
                },
                "target_expr": "3*m**4",
            },
            "correct_option": "C",
            "solution_symbolic": (
                r"**Lời giải tự luận chi tiết:**" "\n\n"
                r"**Bước 1 (Đạo hàm cấp 1 và điểm dừng - 0.5 điểm):**" "\n"
                r"Ta có $f(x) = (x^2 - m^2)^2$. Đạo hàm cấp 1 và cấp 2 là:" "\n"
                r"$$f'(x) = 4x^3 - 4m^2 x = 4x(x - m)(x + m), \quad f''(x) = 12x^2 - 4m^2.$$" "\n"
                r"Giải $f'(x) = 0 \iff x_0 = 0, \; x_1 = -m, \; x_2 = m$ (vì $m \ge 2 > 0$)." "\n\n"
                r"**Bước 2 (Phân loại cực trị bằng đạo hàm cấp 2 - 0.75 điểm):**" "\n"
                r"- Tại $x_0 = 0$: $f''(0) = -4m^2 < 0 \implies x_0 = 0$ là điểm cực đại và $y_{\text{CĐ}} = f(0) = m^4$." "\n"
                r"- Tại $x_{1,2} = \pm m$: $f''(\pm m) = 12m^2 - 4m^2 = 8m^2 > 0 \implies x_1 = -m, x_2 = m$ là hai điểm cực tiểu "
                r"với $y_{\text{CT}} = f(\pm m) = 0$." "\n\n"
                r"**Bước 3 (Tính đại lượng bất biến $T(m)$ - 0.75 điểm):**" "\n"
                r"Tổng bình phương hoành độ hai điểm cực tiểu là $x_1^2 + x_2^2 = (-m)^2 + m^2 = 2m^2$." "\n"
                r"Suy ra:" "\n"
                r"$$T(m) = y_{\text{CĐ}} + m^2(x_1^2 + x_2^2) = m^4 + m^2(2m^2) = 3m^4.$$"
            ),
            "rubric_points": 2.0,
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-DER-03: Quartic Biquadratic Extrema Invariant\n"
                "def f_quartic (m x : Int) : Int := x^4 - 2 * (m^2) * (x^2) + (m^4)\n"
                "def T_invariant (m : Int) : Int := f_quartic m 0 + (m^2) * ((-m)^2 + (m^2))\n\n"
                "theorem calc_der_03_min_val : (List.range 10).all (fun k => let m := Int.ofNat (k + 1); f_quartic m m == 0) = true := by decide\n"
                "theorem calc_der_03_m2 : T_invariant 2 = 48 := by decide\n"
                "theorem calc_der_03_m3 : T_invariant 3 = 243 := by decide\n\n"
                "#eval T_invariant 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "x = sp.Symbol('x', real=True)\n"
                "m = sp.Symbol('m', positive=True)\n"
                "f_expr = x**4 - 2*(m**2)*(x**2) + m**4\n"
                "df = sp.diff(f_expr, x)\n"
                "d2f = sp.diff(f_expr, x, 2)\n"
                "roots = sorted(sp.solve(df, x), key=str)\n"
                "assert sp.simplify(d2f.subs(x, 0) - (-4*m**2)) == 0\n"
                "assert sp.simplify(d2f.subs(x, m) - (8*m**2)) == 0\n"
                "T_sym = sp.simplify(f_expr.subs(x, 0) + (m**2) * ((-m)**2 + m**2))\n"
                "assert sp.simplify(T_sym - 3*m**4) == 0, f'Mismatch: {T_sym}'\n\n"
                "# Kiểm chứng đạo hàm cấp 2 bằng sai phân hữu hạn trên lưới m in [2..9]\n"
                "h = 1e-4\n"
                "for m_val in range(2, 10):\n"
                "    fn = lambda t: (t**4) - 2*(m_val**2)*(t**2) + (m_val**4)\n"
                "    d2_at_0 = (fn(h) - 2*fn(0.0) + fn(-h)) / (h**2)\n"
                "    d2_at_m = (fn(m_val + h) - 2*fn(m_val) + fn(m_val - h)) / (h**2)\n"
                "    assert abs(d2_at_0 - (-4 * m_val**2)) < 1e-3\n"
                "    assert abs(d2_at_m - (8 * m_val**2)) < 1e-2\n"
                "    T_num = fn(0.0) + (m_val**2) * ((-m_val)**2 + (m_val**2))\n"
                "    assert abs(T_num - 3*(m_val**4)) < 1e-8\n\n"
                "print('VERIFIED_OK: CALC-DER-03 quartic extrema & finite-difference grid [2..9] passed (3*m**4)')\n"
            ),
        },
    ]
