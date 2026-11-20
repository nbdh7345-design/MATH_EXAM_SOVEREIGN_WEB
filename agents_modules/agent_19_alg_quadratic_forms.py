"""
Agent-19: Đại số — Dạng toàn phương, Ma trận đối xứng & Tiêu chuẩn Sylvester.
Sinh & kiểm chứng câu hỏi Dạng toàn phương, Đưa về chính tắc Lagrange/Jacobi,
và Tiêu chuẩn Sylvester xác định dương theo tham số m.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 19,
    "agent_code": "AGENT-19",
    "agent_name": "Agent-19 (Đại số: Dạng toàn phương & Tiêu chuẩn Sylvester)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Dạng toàn phương, Đưa về chính tắc Lagrange/Jacobi, Tiêu chuẩn Sylvester xác định dương theo tham số m",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa của Agent-19 (2 MCQ, 1 Essay)."""
    return [
        {
            "code": "ALG-QUAD-01",
            "agent_id": 19,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Dạng toàn phương, Ma trận đối xứng & Tiêu chuẩn Sylvester",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": {
                "m": {
                    "type": "int",
                    "default": 4,
                    "min": 2,
                    "max": 10,
                    "step": 1,
                    "label": "Tham số m",
                }
            },
            "title": "Định thức con chính cấp 3 và ma trận của dạng toàn phương",
            "stem_symbolic": (
                "Trong không gian $\\mathbb{R}^3$, xét dạng toàn phương phụ thuộc tham số $m$:\n"
                "$$Q(x_1, x_2, x_3) = 2x_1^2 + (m+2)x_2^2 + (m+1)x_3^2 + 4x_1 x_2 + 2x_2 x_3.$$\n"
                "Biểu thức định thức con chính cấp 3 ($\\Delta_3 = \\det A$) của ma trận đối xứng $A$ "
                "biểu diễn dạng toàn phương $Q$ là:"
            ),
            "stem_template": (
                "Trong không gian $\\mathbb{R}^3$, với $m = {m}$, xét dạng toàn phương:\n"
                "$$Q(x_1, x_2, x_3) = 2x_1^2 + ({m}+2)x_2^2 + ({m}+1)x_3^2 + 4x_1 x_2 + 2x_2 x_3.$$\n"
                "Giá trị định thức con chính cấp 3 ($\\Delta_3 = \\det A$) của ma trận đối xứng $A$ "
                "biểu diễn dạng toàn phương $Q$ bằng:"
            ),
            "options_symbolic": {
                "A": "$\\Delta_3 = 2m^2 + 2m - 2$",
                "B": "$\\Delta_3 = 2m^2 + 2m + 2$",
                "C": "$\\Delta_3 = 2m^2 - 2m - 2$",
                "D": "$\\Delta_3 = m^2 + 2m - 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m**2 + 2*m - 2",
                    "B": "2*m**2 + 2*m + 2",
                    "C": "2*m**2 - 2*m - 2",
                    "D": "m**2 + 2*m - 2",
                },
                "target_expr": "2*m**2 + 2*m - 2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                "Ma trận đối xứng $A$ của dạng toàn phương $Q(x_1, x_2, x_3)$ là:\n"
                "$$A = \\begin{pmatrix} 2 & 2 & 0 \\\\ 2 & m+2 & 1 \\\\ 0 & 1 & m+1 \\end{pmatrix}.$$\n"
                "Các định thức con chính dẫn đầu (leading principal minors) của $A$ lần lượt là:\n"
                "- $\\Delta_1 = 2 > 0$.\n"
                "- $\\Delta_2 = \\det\\begin{pmatrix} 2 & 2 \\\\ 2 & m+2 \\end{pmatrix} = 2(m+2) - 4 = 2m$.\n"
                "- Khai triển định thức cấp 3 theo cột 3:\n"
                "$$\\Delta_3 = \\det A = (m+1)\\Delta_2 - 1\\cdot \\det\\begin{pmatrix} 2 & 0 \\\\ 2 & 1 \\end{pmatrix} "
                "= 2m(m+1) - 2 = 2m^2 + 2m - 2.$$\n"
                "Với mọi $m \\ge 2$, $\\Delta_1 = 2 > 0$, $\\Delta_2 = 2m > 0$, $\\Delta_3 = 2m^2 + 2m - 2 > 0$, "
                "nên $Q$ xác định dương theo tiêu chuẩn Sylvester. Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Lập đúng ma trận đối xứng A của dạng toàn phương (chia đôi hệ số chéo): 0.25 điểm.",
                "Tính đúng định thức con chính cấp 2: Delta_2 = 2m: 0.25 điểm.",
                "Tính đúng định thức con chính cấp 3: Delta_3 = 2m^2 + 2m - 2 và kết luận: 0.50 điểm.",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-QUAD-01 (No Mathlib, No sorry)\n"
                "def delta1 (_m : Int) : Int := 2\n"
                "def delta2 (m : Int) : Int := 2 * (m + 2) - 2 * 2\n"
                "def delta3 (m : Int) : Int := (m + 1) * (delta2 m) - 2 * 1\n"
                "def target_delta3 (m : Int) : Int := 2 * m * m + 2 * m - 2\n\n"
                "theorem delta2_identity (m : Int) : delta2 m = 2 * m := by\n"
                "  unfold delta2\n"
                "  omega\n\n"
                "theorem delta3_at_default : delta3 4 = target_delta3 4 := by rfl\n\n"
                "theorem sylvester_pos_at_default :\n"
                "    delta1 4 > 0 ∧ delta2 4 > 0 ∧ delta3 4 > 0 := by decide\n\n"
                "#eval (delta1 4, delta2 4, delta3 4, target_delta3 4)\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m = sp.Symbol('m', real=True)\n"
                "A = sp.Matrix([\n"
                "    [2, 2, 0],\n"
                "    [2, m + 2, 1],\n"
                "    [0, 1, m + 1]\n"
                "])\n"
                "d1 = A[:1, :1].det()\n"
                "d2 = sp.expand(A[:2, :2].det())\n"
                "d3 = sp.expand(A.det())\n"
                "assert d1 == 2\n"
                "assert d2 == 2 * m\n"
                "assert d3 == 2 * m**2 + 2 * m - 2\n\n"
                "for m_val in range(2, 11):\n"
                "    A_num = np.array(A.subs(m, m_val).tolist(), dtype=float)\n"
                "    eigs = np.linalg.eigvalsh(A_num)\n"
                "    assert np.all(eigs > 0), f'Not positive definite at m={m_val}'\n\n"
                "print(f'VERIFIED_OK: ALG-QUAD-01 d1={d1}, d2={d2}, d3={d3}')\n"
            ),
        },
        {
            "code": "ALG-QUAD-02",
            "agent_id": 19,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Dạng toàn phương, Ma trận đối xứng & Tiêu chuẩn Sylvester",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": {
                "m": {
                    "type": "int",
                    "default": 4,
                    "min": 2,
                    "max": 10,
                    "step": 1,
                    "label": "Tham số m",
                }
            },
            "title": "Điều kiện tiêu chuẩn Sylvester để dạng toàn phương xác định dương",
            "stem_symbolic": (
                "Trong không gian $\\mathbb{R}^3$, xét dạng toàn phương:\n"
                "$$Q(x_1, x_2, x_3) = x_1^2 + 5x_2^2 + k x_3^2 + 4x_1 x_2 + 2m x_1 x_3 + 4m x_2 x_3$$\n"
                "với tham số nguyên $m \\ge 2$. Giá trị nguyên nhỏ nhất của $k$ để dạng toàn phương $Q$ "
                "xác định dương trên $\\mathbb{R}^3$ là:"
            ),
            "stem_template": (
                "Trong không gian $\\mathbb{R}^3$, với $m = {m}$, xét dạng toàn phương:\n"
                "$$Q(x_1, x_2, x_3) = x_1^2 + 5x_2^2 + k x_3^2 + 4x_1 x_2 + 2\\cdot {m} x_1 x_3 + 4\\cdot {m} x_2 x_3.$$\n"
                "Giá trị nguyên nhỏ nhất của $k$ để dạng toàn phương $Q$ xác định dương trên $\\mathbb{R}^3$ là:"
            ),
            "options_symbolic": {
                "A": "$k_{\\min} = m^2$",
                "B": "$k_{\\min} = m^2 + 1$",
                "C": "$k_{\\min} = 2m^2 + 1$",
                "D": "$k_{\\min} = m^2 - 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2",
                    "B": "m**2 + 1",
                    "C": "2*m**2 + 1",
                    "D": "m**2 - 1",
                },
                "target_expr": "m**2 + 1",
            },
            "correct_option": "B",
            "solution_symbolic": (
                "Ma trận đối xứng của dạng toàn phương $Q(x_1, x_2, x_3)$ là:\n"
                "$$A = \\begin{pmatrix} 1 & 2 & m \\\\ 2 & 5 & 2m \\\\ m & 2m & k \\end{pmatrix}.$$\n"
                "Các định thức con chính dẫn đầu:\n"
                "- $\\Delta_1 = 1 > 0$.\n"
                "- $\\Delta_2 = \\det\\begin{pmatrix} 1 & 2 \\\\ 2 & 5 \\end{pmatrix} = 5 - 4 = 1 > 0$.\n"
                "- $\\Delta_3 = \\det A = k - m^2$ (thực hiện biến đổi sơ cấp hàng $R_2 \\leftarrow R_2 - 2R_1$, "
                "$R_3 \\leftarrow R_3 - m R_1$ hoặc đưa về chính tắc Lagrange: "
                "$Q = (x_1 + 2x_2 + m x_3)^2 + x_2^2 + (k - m^2)x_3^2$).\n"
                "Theo tiêu chuẩn Sylvester, $Q$ xác định dương khi và chỉ khi $\\Delta_3 = k - m^2 > 0 \\iff k > m^2$.\n"
                "Vậy giá trị nguyên nhỏ nhất của $k$ là $k_{\\min} = m^2 + 1$. Chọn đáp án **B**."
            ),
            "rubric_points": [
                "Viết đúng ma trận đối xứng A hoặc tách bình phương Lagrange: 0.25 điểm.",
                "Tính đúng Delta_1 = 1, Delta_2 = 1, Delta_3 = k - m^2: 0.50 điểm.",
                "Áp dụng tiêu chuẩn Sylvester k > m^2 suy ra k_min = m^2 + 1: 0.25 điểm.",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-QUAD-02 (No Mathlib, No sorry)\n"
                "def q2_delta1 : Int := 1\n"
                "def q2_delta2 : Int := 1 * 5 - 2 * 2\n"
                "def q2_delta3 (m k : Int) : Int := k - m * m\n"
                "def k_min (m : Int) : Int := m * m + 1\n\n"
                "theorem q2_delta2_pos : q2_delta2 = 1 := by rfl\n\n"
                "theorem q2_delta3_at_kmin (m : Int) : q2_delta3 m (k_min m) = 1 := by\n"
                "  unfold q2_delta3 k_min\n"
                "  omega\n\n"
                "theorem q2_sylvester_at_default :\n"
                "    q2_delta1 > 0 ∧ q2_delta2 > 0 ∧ q2_delta3 4 (k_min 4) > 0 := by decide\n\n"
                "#eval (q2_delta1, q2_delta2, k_min 4, q2_delta3 4 (k_min 4))\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m, k = sp.symbols('m k', real=True)\n"
                "A = sp.Matrix([\n"
                "    [1, 2, m],\n"
                "    [2, 5, 2 * m],\n"
                "    [m, 2 * m, k]\n"
                "])\n"
                "d1 = A[:1, :1].det()\n"
                "d2 = sp.simplify(A[:2, :2].det())\n"
                "d3 = sp.simplify(A.det())\n"
                "assert d1 == 1 and d2 == 1 and d3 == k - m**2\n\n"
                "for m_val in range(2, 11):\n"
                "    k_val = m_val**2 + 1\n"
                "    A_pos = np.array(A.subs({m: m_val, k: k_val}).tolist(), dtype=float)\n"
                "    A_bnd = np.array(A.subs({m: m_val, k: m_val**2}).tolist(), dtype=float)\n"
                "    assert np.all(np.linalg.eigvalsh(A_pos) > 0)\n"
                "    assert np.min(np.linalg.eigvalsh(A_bnd)) <= 1e-12\n\n"
                "print(f'VERIFIED_OK: ALG-QUAD-02 d1={d1}, d2={d2}, d3={d3}, k_min=m**2+1')\n"
            ),
        },
        {
            "code": "ALG-QUAD-03",
            "agent_id": 19,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Dạng toàn phương, Ma trận đối xứng & Tiêu chuẩn Sylvester",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {
                    "type": "int",
                    "default": 4,
                    "min": 2,
                    "max": 10,
                    "step": 1,
                    "label": "Tham số m",
                }
            },
            "title": "Đưa dạng toàn phương về chính tắc Lagrange/Jacobi và kiểm định Sylvester",
            "stem_symbolic": (
                "Trong không gian $\\mathbb{R}^3$, cho dạng toàn phương phụ thuộc tham số nguyên $m \\ge 2$:\n"
                "$$Q(x_1, x_2, x_3) = x_1^2 + (m+1)x_2^2 + (m^2 + 3m - 1)x_3^2 - 2x_1 x_2 + 2m x_1 x_3.$$\n"
                "a) Lập ma trận đối xứng $A(m)$ và tính các định thức con chính dẫn đầu $\\Delta_1, \\Delta_2, \\Delta_3$.\n"
                "b) Đưa $Q$ về dạng chính tắc bằng phương pháp Lagrange và phương pháp Jacobi, "
                "từ đó chứng minh $Q$ xác định dương với mọi $m \\ge 2$."
            ),
            "stem_template": (
                "Trong không gian $\\mathbb{R}^3$, với $m = {m}$, cho dạng toàn phương:\n"
                "$$Q(x_1, x_2, x_3) = x_1^2 + ({m}+1)x_2^2 + ({m}^2 + 3\\cdot {m} - 1)x_3^2 - 2x_1 x_2 + 2\\cdot {m} x_1 x_3.$$\n"
                "a) Lập ma trận đối xứng $A({m})$ và tính các định thức con chính dẫn đầu $\\Delta_1, \\Delta_2, \\Delta_3$.\n"
                "b) Đưa $Q$ về dạng chính tắc bằng phương pháp Lagrange và phương pháp Jacobi, "
                "từ đó kiểm chứng $Q$ xác định dương."
            ),
            "options_symbolic": {
                "A": "$\\Delta_3 = 2m^2 - m, \\quad Q = y_1^2 + m y_2^2 + (2m-1)y_3^2$",
                "B": "$\\Delta_3 = 2m^2 + m, \\quad Q = y_1^2 + m y_2^2 + (2m+1)y_3^2$",
                "C": "$\\Delta_3 = m^2 - m, \\quad Q = y_1^2 + (m+1)y_2^2 + (m-1)y_3^2$",
                "D": "$\\Delta_3 = 2m^2 - 1, \\quad Q = y_1^2 + m y_2^2 + (2m-1)y_3^2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m**2 - m",
                    "B": "2*m**2 + m",
                    "C": "m**2 - m",
                    "D": "2*m**2 - 1",
                },
                "target_expr": "2*m**2 - m",
            },
            "correct_option": "A",
            "solution_symbolic": (
                "**a) Ma trận đối xứng và các định thức con chính Sylvester:**\n"
                "$$A(m) = \\begin{pmatrix} 1 & -1 & m \\\\ -1 & m+1 & 0 \\\\ m & 0 & m^2 + 3m - 1 \\end{pmatrix}.$$\n"
                "- $\\Delta_1 = 1 > 0$.\n"
                "- $\\Delta_2 = \\det\\begin{pmatrix} 1 & -1 \\\\ -1 & m+1 \\end{pmatrix} = (m+1) - 1 = m$.\n"
                "- $\\Delta_3 = \\det A(m) = m(2m - 1) = 2m^2 - m$.\n\n"
                "**b) Đưa về dạng chính tắc Lagrange & Jacobi:**\n"
                "- Nhóm các số hạng chứa $x_1$: $(x_1 - x_2 + m x_3)^2 = x_1^2 + x_2^2 + m^2 x_3^2 - 2x_1 x_2 + 2m x_1 x_3 - 2m x_2 x_3$.\n"
                "- Phần dư còn lại: $m x_2^2 + 2m x_2 x_3 + (3m - 1)x_3^2 = m(x_2 + x_3)^2 + (2m - 1)x_3^2$.\n"
                "- Đặt phép biến đổi không suy biến:\n"
                "$$\\begin{cases} y_1 = x_1 - x_2 + m x_3 \\\\ y_2 = x_2 + x_3 \\\\ y_3 = x_3 \\end{cases} \\implies "
                "Q = y_1^2 + m y_2^2 + (2m - 1)y_3^2.$$\n"
                "- Theo công thức Jacobi: $Q = \\frac{1}{\\Delta_1}z_1^2 + \\frac{\\Delta_1}{\\Delta_2}z_2^2 + \\frac{\\Delta_2}{\\Delta_3}z_3^2 "
                "= z_1^2 + \\frac{1}{m}z_2^2 + \\frac{m}{2m^2 - m}z_3^2$.\n"
                "Với mọi $m \\ge 2$, $\\Delta_1 = 1 > 0$, $\\Delta_2 = m > 0$, $\\Delta_3 = m(2m-1) > 0$, nên $Q$ xác định dương."
            ),
            "rubric_points": [
                "Lập đúng ma trận đối xứng A(m) cấp 3x3: 0.25 điểm.",
                "Tính đúng 3 định thức con chính dẫn đầu Delta_1 = 1, Delta_2 = m, Delta_3 = 2m^2 - m: 0.25 điểm.",
                "Biến đổi Lagrange hoàn chỉnh Q = (x_1 - x_2 + m x_3)^2 + m(x_2 + x_3)^2 + (2m - 1)x_3^2: 0.25 điểm.",
                "Viết dạng chính tắc Jacobi và kết luận xác định dương theo tiêu chuẩn Sylvester: 0.25 điểm.",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-QUAD-03 (No Mathlib, No sorry)\n"
                "def q3_d1 (_m : Int) : Int := 1\n"
                "def q3_d2 (m : Int) : Int := (m + 1) - 1\n"
                "def q3_d3 (m : Int) : Int := m * (2 * m - 1)\n\n"
                "def q3_form (m x1 x2 x3 : Int) : Int :=\n"
                "  x1*x1 + (m + 1)*x2*x2 + (m*m + 3*m - 1)*x3*x3 - 2*x1*x2 + 2*m*x1*x3\n\n"
                "def q3_lagrange (m x1 x2 x3 : Int) : Int :=\n"
                "  let y1 := x1 - x2 + m * x3\n"
                "  let y2 := x2 + x3\n"
                "  let y3 := x3\n"
                "  y1*y1 + m*y2*y2 + (2*m - 1)*y3*y3\n\n"
                "theorem q3_d2_id (m : Int) : q3_d2 m = m := by\n"
                "  unfold q3_d2\n"
                "  omega\n\n"
                "theorem q3_lagrange_at_default :\n"
                "    q3_form 4 3 (-2) 5 = q3_lagrange 4 3 (-2) 5 := by rfl\n\n"
                "theorem q3_sylvester_at_default :\n"
                "    q3_d1 4 > 0 ∧ q3_d2 4 > 0 ∧ q3_d3 4 > 0 := by decide\n\n"
                "#eval (q3_d1 4, q3_d2 4, q3_d3 4, q3_form 4 3 (-2) 5)\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m, x1, x2, x3 = sp.symbols('m x1 x2 x3', real=True)\n"
                "A = sp.Matrix([\n"
                "    [1, -1, m],\n"
                "    [-1, m + 1, 0],\n"
                "    [m, 0, m**2 + 3*m - 1]\n"
                "])\n"
                "d1 = A[:1, :1].det()\n"
                "d2 = sp.expand(A[:2, :2].det())\n"
                "d3 = sp.expand(A.det())\n"
                "assert d1 == 1\n"
                "assert d2 == m\n"
                "assert d3 == 2*m**2 - m\n\n"
                "X = sp.Matrix([x1, x2, x3])\n"
                "Q_mat = sp.expand((X.T * A * X)[0])\n"
                "Q_lag = sp.expand((x1 - x2 + m*x3)**2 + m*(x2 + x3)**2 + (2*m - 1)*x3**2)\n"
                "assert sp.simplify(Q_mat - Q_lag) == 0\n\n"
                "for m_val in range(2, 11):\n"
                "    A_num = np.array(A.subs(m, m_val).tolist(), dtype=float)\n"
                "    eigs = np.linalg.eigvalsh(A_num)\n"
                "    assert np.all(eigs > 0), f'Not positive definite at m={m_val}'\n\n"
                "print(f'VERIFIED_OK: ALG-QUAD-03 d1={d1}, d2={d2}, d3={d3}, Lagrange=OK')\n"
            ),
        },
    ]
