"""
Agent-14: Đại số — Không gian Vector, Cơ sở & Tọa độ
Sinh & kiểm chứng câu hỏi Tổ hợp tuyến tính, Độc lập/Phụ thuộc tuyến tính,
Cơ sở và Ma trận chuyển cơ sở có tham số (SymPy + NumPy + Core Lean 4).
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 14,
    "agent_code": "AGENT-14",
    "agent_name": "Agent-14 (Đại số: Không gian Vector, Cơ sở & Tọa độ)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Tổ hợp tuyến tính, Độc lập/Phụ thuộc tuyến tính, Cơ sở và Ma trận chuyển cơ sở có tham số",
}


def get_questions() -> list[dict]:
    return [
        {
            "code": "ALG-VEC-01",
            "agent_id": 14,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian Vector, Độc lập tuyến tính & Chuyển cơ sở có tham số",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Biểu diễn tổ hợp tuyến tính trong không gian con sinh bởi hệ vector",
            "stem_symbolic": (
                "Trong không gian vector $\\mathbb{R}^3$, cho hệ hai vector độc lập tuyến tính "
                "$u_1 = (1, 2, -1)$, $u_2 = (2, 3, 1)$ và vector phụ thuộc tham số "
                "$v_m = (4m + 3, 7m + 4, 3 - m)$ với $m \\in \\{2, 3, \\dots, 9\\}$. "
                "Biết rằng $v_m$ thuộc không gian con $W = \\text{span}\\{u_1, u_2\\}$ với biểu diễn "
                "duy nhất $v_m = \\alpha_1 u_1 + \\alpha_2 u_2$. Tính tổng các hệ số $S(m) = \\alpha_1 + \\alpha_2$."
            ),
            "stem_template": (
                "Trong không gian vector $\\mathbb{R}^3$, cho hệ hai vector độc lập tuyến tính "
                "$u_1 = (1, 2, -1)$, $u_2 = (2, 3, 1)$ và vector $v_{{{m}}} = (4\\cdot {m} + 3, 7\\cdot {m} + 4, 3 - {m})$ "
                "(ứng với tham số $m = {m}$). Biết rằng $v_{{{m}}} = \\alpha_1 u_1 + \\alpha_2 u_2$, "
                "hãy tính tổng hệ số $S({m}) = \\alpha_1 + \\alpha_2$."
            ),
            "options_symbolic": {
                "A": "$S(m) = 3m + 1$",
                "B": "$S(m) = 3m - 1$",
                "C": "$S(m) = 3m + 2$",
                "D": "$S(m) = 2m - 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "3*m + 1",
                    "B": "3*m - 1",
                    "C": "3*m + 2",
                    "D": "2*m - 1",
                },
                "target_expr": "3*m + 1",
            },
            "correct_option": "A",
            "solution_symbolic": (
                "Thiết lập hệ phương trình tuyến tính từ đẳng thức vector $\\alpha_1 u_1 + \\alpha_2 u_2 = v_m$:\n"
                "$$\\begin{cases} \\alpha_1 + 2\\alpha_2 = 4m + 3 \\\\ 2\\alpha_1 + 3\\alpha_2 = 7m + 4 \\\\ -\\alpha_1 + \\alpha_2 = 3 - m \\end{cases}$$\n"
                "Từ phương trình (1) và (3), cộng vế theo vế ta được $3\\alpha_2 = 3m + 6 \\implies \\alpha_2 = m + 2$.\n"
                "Thay vào phương trình (3) suy ra $\\alpha_1 = \\alpha_2 - (3 - m) = (m + 2) - 3 + m = 2m - 1$.\n"
                "Kiểm tra lại với phương trình (2): $2(2m - 1) + 3(m + 2) = 7m + 4$ (nghiệm đúng với mọi $m$).\n"
                "Vậy $S(m) = \\alpha_1 + \\alpha_2 = (2m - 1) + (m + 2) = 3m + 1$. Chọn đáp án A."
            ),
            "rubric_points": [
                "Lập đúng hệ 3 phương trình tuyến tính cho 2 ẩn số (alpha_1, alpha_2): 0.5 điểm",
                "Giải tìm được alpha_1 = 2m - 1 và alpha_2 = m + 2, kiểm tra điều kiện tương thích phương trình thứ 3: 0.25 điểm",
                "Tính đúng tổng S(m) = 3m + 1: 0.25 điểm",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-VEC-01 (Linear Combination in R^3)\n"
                "def u1 : Int × Int × Int := (1, 2, -1)\n"
                "def u2 : Int × Int × Int := (2, 3, 1)\n\n"
                "def linComb (a1 a2 : Int) : Int × Int × Int :=\n"
                "  (a1 * 1 + a2 * 2, a1 * 2 + a2 * 3, a1 * (-1) + a2 * 1)\n\n"
                "def targetVec (m : Int) : Int × Int × Int :=\n"
                "  (4 * m + 3, 7 * m + 4, 3 - m)\n\n"
                "theorem alg_vec_01_m3 : linComb (2 * 3 - 1) (3 + 2) = targetVec 3 := by decide\n"
                "theorem alg_vec_01_sum_m3 : (2 * 3 - 1) + (3 + 2) = 3 * 3 + 1 := by omega\n"
                "theorem alg_vec_01_sum_general (m : Int) : (2 * m - 1) + (m + 2) = 3 * m + 1 := by omega\n\n"
                "#eval (linComb (2 * 3 - 1) (3 + 2), targetVec 3, 3 * 3 + 1)\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m = sp.Symbol('m', integer=True)\n"
                "A = sp.Matrix([[1, 2], [2, 3], [-1, 1]])\n"
                "v_m = sp.Matrix([4*m + 3, 7*m + 4, 3 - m])\n"
                "alpha1, alpha2 = sp.symbols('alpha1 alpha2')\n"
                "sol = sp.solve(A * sp.Matrix([alpha1, alpha2]) - v_m, (alpha1, alpha2))\n"
                "sum_expr = sp.simplify(sol[alpha1] + sol[alpha2])\n"
                "assert sp.simplify(sum_expr - (3*m + 1)) == 0, f'Symbolic mismatch: {sum_expr}'\n\n"
                "for m_val in range(2, 10):\n"
                "    A_np = np.array([[1.0, 2.0], [2.0, 3.0], [-1.0, 1.0]])\n"
                "    v_np = np.array([4*m_val + 3, 7*m_val + 4, 3 - m_val], dtype=float)\n"
                "    coeffs, residuals, rank, _ = np.linalg.lstsq(A_np, v_np, rcond=None)\n"
                "    assert rank == 2 and np.allclose(A_np @ coeffs, v_np)\n"
                "    assert np.isclose(np.sum(coeffs), 3*m_val + 1)\n\n"
                "print(f'VERIFIED_OK: ALG-VEC-01 S(m) = {sum_expr}, m=3 -> {sum_expr.subs(m, 3)}')\n"
            ),
        },
        {
            "code": "ALG-VEC-02",
            "agent_id": 14,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian Vector, Độc lập tuyến tính & Chuyển cơ sở có tham số",
            "question_type": "mcq",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "default_val": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Độc lập tuyến tính, Cơ sở và Tọa độ của vector theo cơ sở có tham số",
            "stem_symbolic": (
                "Trong không gian vector $\\mathbb{R}^3$, cho hệ ba vector phụ thuộc tham số $m \\in \\{2, 3, \\dots, 9\\}$:\n"
                "$e_1 = (1, 0, 1)$, $e_2 = (1, 1, m)$, $e_3 = (2, 1, m + 2)$.\n"
                "Hệ $\\mathcal{B}_m = \\{e_1, e_2, e_3\\}$ luôn độc lập tuyến tính và lập thành một cơ sở của $\\mathbb{R}^3$. "
                "Tìm tổng các tọa độ $Q(m) = x_1 + x_2 + x_3$ của vector "
                "$x = (3m + 4, m + 3, m^2 + 6m + 2)$ trong cơ sở $\\mathcal{B}_m$."
            ),
            "stem_template": (
                "Trong không gian vector $\\mathbb{R}^3$ với tham số $m = {m}$, cho cơ sở "
                "$\\mathcal{{B}}_{{{m}}} = \\{{e_1, e_2, e_3\\}}$ gồm $e_1 = (1, 0, 1)$, $e_2 = (1, 1, {m})$, $e_3 = (2, 1, {m} + 2)$. "
                "Tìm tổng các tọa độ $Q({m}) = x_1 + x_2 + x_3$ của vector "
                "$x = (3\\cdot {m} + 4, {m} + 3, {m}^2 + 6\\cdot {m} + 2)$ đối với cơ sở $\\mathcal{{B}}_{{{m}}}$."
            ),
            "options_symbolic": {
                "A": "$Q(m) = 2m + 3$",
                "B": "$Q(m) = 2m + 1$",
                "C": "$Q(m) = 2m + 5$",
                "D": "$Q(m) = 3m + 4$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m + 3",
                    "B": "2*m + 1",
                    "C": "2*m + 5",
                    "D": "3*m + 4",
                },
                "target_expr": "2*m + 3",
            },
            "correct_option": "A",
            "solution_symbolic": (
                "Lập ma trận cột cơ sở $P_m = \\begin{pmatrix} 1 & 1 & 2 \\\\ 0 & 1 & 1 \\\\ 1 & m & m+2 \\end{pmatrix}$. "
                "Ta có $\\det(P_m) = 1(m+2 - m) - 1(0 - 1) + 2(0 - 1) = 2 + 1 - 2 = 1 \\neq 0$ với mọi $m$, "
                "do đó $\\mathcal{B}_m$ luôn là một cơ sở của $\\mathbb{R}^3$.\n"
                "Tọa độ $[x]_{\\mathcal{B}_m} = (x_1, x_2, x_3)^T$ thỏa mãn $P_m [x]_{\\mathcal{B}_m} = x^T$:\n"
                "$$\\begin{cases} x_1 + x_2 + 2x_3 = 3m + 4 \\\\ x_2 + x_3 = m + 3 \\\\ x_1 + m x_2 + (m+2)x_3 = m^2 + 6m + 2 \\end{cases}$$\n"
                "Từ phương trình (1) và (2) suy ra $x_1 + x_3 = (3m + 4) - (m + 3) = 2m + 1 \\implies x_1 = 2m + 1 - x_3$, "
                "và $x_2 = m + 3 - x_3$.\n"
                "Thay vào phương trình (3): $(2m + 1 - x_3) + m(m + 3 - x_3) + (m+2)x_3 = m^2 + 5m + 1 + x_3 = m^2 + 6m + 2$\n"
                "$\\implies x_3 = m + 1 \\implies x_2 = 2, \\; x_1 = m$.\n"
                "Vậy $[x]_{\\mathcal{B}_m} = (m, 2, m+1)^T$ và tổng tọa độ là $Q(m) = m + 2 + (m + 1) = 2m + 3$. Chọn đáp án A."
            ),
            "rubric_points": [
                "Chứng minh det(P_m) = 1 != 0 với mọi m nên hệ độc lập tuyến tính và là cơ sở: 0.25 điểm",
                "Giải hệ phương trình tọa độ P_m X = x tìm được (x_1, x_2, x_3) = (m, 2, m+1): 0.5 điểm",
                "Tính đúng tổng tọa độ Q(m) = 2m + 3: 0.25 điểm",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-VEC-02 (Basis & Coordinates in R^3)\n"
                "def detPm (m : Int) : Int :=\n"
                "  1 * (1 * (m + 2) - 1 * m) - 1 * (0 * (m + 2) - 1 * 1) + 2 * (0 * m - 1 * 1)\n\n"
                "def coordReconstruct (m x1 x2 x3 : Int) : Int × Int × Int :=\n"
                "  (x1 + x2 + 2 * x3, x2 + x3, x1 + m * x2 + (m + 2) * x3)\n\n"
                "theorem alg_vec_02_det_m3 : detPm 3 = 1 := by decide\n"
                "theorem alg_vec_02_coords_m3 :\n"
                "    coordReconstruct 3 3 2 4 = (3 * 3 + 4, 3 + 3, 3 * 3 + 6 * 3 + 2) := by decide\n"
                "theorem alg_vec_02_sum (m : Int) : m + 2 + (m + 1) = 2 * m + 3 := by omega\n\n"
                "#eval (detPm 3, coordReconstruct 3 3 2 4, 2 * 3 + 3)\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m = sp.Symbol('m', integer=True)\n"
                "P_m = sp.Matrix([[1, 1, 2], [0, 1, 1], [1, m, m + 2]])\n"
                "assert sp.simplify(P_m.det()) == 1, 'Determinant must be identically 1'\n"
                "x_vec = sp.Matrix([3*m + 4, m + 3, m**2 + 6*m + 2])\n"
                "coords = sp.simplify(P_m.inv() * x_vec)\n"
                "assert coords == sp.Matrix([m, 2, m + 1]), f'Unexpected coords: {coords}'\n"
                "q_expr = sp.simplify(sum(coords))\n"
                "assert sp.simplify(q_expr - (2*m + 3)) == 0\n\n"
                "for m_val in range(2, 10):\n"
                "    P_np = np.array([[1, 1, 2], [0, 1, 1], [1, m_val, m_val + 2]], dtype=float)\n"
                "    x_np = np.array([3*m_val + 4, m_val + 3, m_val**2 + 6*m_val + 2], dtype=float)\n"
                "    c_np = np.linalg.solve(P_np, x_np)\n"
                "    assert np.allclose(c_np, [m_val, 2, m_val + 1])\n"
                "    assert np.isclose(np.sum(c_np), 2*m_val + 3)\n\n"
                "print(f'VERIFIED_OK: ALG-VEC-02 det=1, coords={list(coords)}, Q(m)={q_expr}')\n"
            ),
        },
        {
            "code": "ALG-VEC-03",
            "agent_id": 14,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian Vector, Độc lập tuyến tính & Chuyển cơ sở có tham số",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Tự luận: Ma trận chuyển cơ sở và công thức đổi tọa độ trong R^3",
            "stem_symbolic": (
                "Trong không gian vector $\\mathbb{R}^3$, xét cơ sở tam giác trên "
                "$\\mathcal{B} = \\{u_1 = (1, 0, 0),\\; u_2 = (1, 1, 0),\\; u_3 = (1, 1, 1)\\}$ và hệ ba vector phụ thuộc tham số $m \\in \\{2, 3, \\dots, 9\\}$:\n"
                "$\\mathcal{B}'_m = \\{v_1 = (2, 1, 0),\\; v_2 = (2, 2, 1),\\; v_3 = (2m + 3, m + 3, 2)\\}$.\n"
                "a) Tìm ma trận chuyển cơ sở $C_{\\mathcal{B} \\to \\mathcal{B}'_m}$ từ cơ sở $\\mathcal{B}$ sang hệ $\\mathcal{B}'_m$ và chứng minh $\\det(C_{\\mathcal{B} \\to \\mathcal{B}'_m}) = 1$ với mọi $m$.\n"
                "b) Cho vector $w \\in \\mathbb{R}^3$ có tọa độ trong cơ sở $\\mathcal{B}'_m$ là $[w]_{\\mathcal{B}'_m} = (1, 1, 1)^T$. "
                "Tìm tọa độ $[w]_{\\mathcal{B}}$ và tính tổng ba thành phần tọa độ $R(m)$ của $[w]_{\\mathcal{B}}$."
            ),
            "stem_template": (
                "Trong không gian vector $\\mathbb{R}^3$ với tham số $m = {m}$, xét cơ sở "
                "$\\mathcal{{B}} = \\{{u_1 = (1, 0, 0),\\; u_2 = (1, 1, 0),\\; u_3 = (1, 1, 1)\\}}$ và hệ vector "
                "$\\mathcal{{B}}'_{{{m}}} = \\{{v_1 = (2, 1, 0),\\; v_2 = (2, 2, 1),\\; v_3 = (2\\cdot {m} + 3, {m} + 3, 2)\\}}$.\n"
                "a) Tìm ma trận chuyển cơ sở $C_{{\\mathcal{{B}} \\to \\mathcal{{B}}'_{{{m}}}}}$ và chứng minh $\\det(C_{{\\mathcal{{B}} \\to \\mathcal{{B}}'_{{{m}}}}}) = 1$.\n"
                "b) Với $[w]_{{\\mathcal{{B}}'_{{{m}}}}} = (1, 1, 1)^T$, hãy xác định $[w]_{{\\mathcal{{B}}}}$ và tính tổng các tọa độ $R({m})$ của $[w]_{{\\mathcal{{B}}}}$."
            ),
            "options_symbolic": {
                "A": "$R(m) = 2m + 7$",
                "B": "$R(m) = 2m + 5$",
                "C": "$R(m) = 2m + 3$",
                "D": "$R(m) = 3m + 8$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m + 7",
                    "B": "2*m + 5",
                    "C": "2*m + 3",
                    "D": "3*m + 8",
                },
                "target_expr": "2*m + 7",
            },
            "correct_option": "A",
            "solution_symbolic": (
                "a) Đặt ma trận các cột cơ sở $U = \\begin{pmatrix} 1 & 1 & 1 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 1 \\end{pmatrix}$ "
                "và $V_m = \\begin{pmatrix} 2 & 2 & 2m+3 \\\\ 1 & 2 & m+3 \\\\ 0 & 1 & 2 \\end{pmatrix}$.\n"
                "Vì $U^{-1} = \\begin{pmatrix} 1 & -1 & 0 \\\\ 0 & 1 & -1 \\\\ 0 & 0 & 1 \\end{pmatrix}$, ma trận chuyển cơ sở từ $\\mathcal{B}$ sang $\\mathcal{B}'_m$ là:\n"
                "$$C_{\\mathcal{B} \\to \\mathcal{B}'_m} = U^{-1} V_m = \\begin{pmatrix} 1 & 0 & m \\\\ 1 & 1 & m+1 \\\\ 0 & 1 & 2 \\end{pmatrix}$$\n"
                "Ta có $\\det(C_{\\mathcal{B} \\to \\mathcal{B}'_m}) = 1\\cdot(2 - (m+1)) - 0 + m\\cdot(1 - 0) = 1 \\neq 0$ với mọi $m$, nên $\\mathcal{B}'_m$ là một cơ sở của $\\mathbb{R}^3$.\n\n"
                "b) Theo công thức đổi tọa độ $[w]_{\\mathcal{B}} = C_{\\mathcal{B} \\to \\mathcal{B}'_m} [w]_{\\mathcal{B}'_m}$, với $[w]_{\\mathcal{B}'_m} = (1, 1, 1)^T$:\n"
                "$$[w]_{\\mathcal{B}} = \\begin{pmatrix} 1 & 0 & m \\\\ 1 & 1 & m+1 \\\\ 0 & 1 & 2 \\end{pmatrix} \\begin{pmatrix} 1 \\\\ 1 \\\\ 1 \\end{pmatrix} = \\begin{pmatrix} m + 1 \\\\ m + 3 \\\\ 3 \\end{pmatrix}$$\n"
                "Tổng các thành phần tọa độ của $[w]_{\\mathcal{B}}$ là $R(m) = (m + 1) + (m + 3) + 3 = 2m + 7$."
            ),
            "rubric_points": [
                "Tìm đúng ma trận nghịch đảo U^{-1} và tính đúng ma trận chuyển cơ sở C_{B -> B'_m} = U^{-1} V_m: 0.4 điểm",
                "Tính định thức det(C_{B -> B'_m}) = 1 != 0, kết luận B'_m là cơ sở với mọi m: 0.2 điểm",
                "Áp dụng công thức đổi tọa độ [w]_B = C_{B -> B'_m} [w]_{B'_m} tìm được (m+1, m+3, 3)^T: 0.2 điểm",
                "Tính đúng tổng tọa độ R(m) = 2m + 7: 0.2 điểm",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-VEC-03 (Transition Matrix & Coordinate Change)\n"
                "def detTransition (m : Int) : Int :=\n"
                "  1 * (1 * 2 - (m + 1) * 1) - 0 * (1 * 2 - (m + 1) * 0) + m * (1 * 1 - 1 * 0)\n\n"
                "def wCoordsB (m : Int) : Int × Int × Int :=\n"
                "  (1 + 0 + m, 1 + 1 + (m + 1), 0 + 1 + 2)\n\n"
                "def sumCoordsB (m : Int) : Int :=\n"
                "  (m + 1) + (m + 3) + 3\n\n"
                "theorem alg_vec_03_det (m : Int) : detTransition m = 1 := by unfold detTransition; omega\n"
                "theorem alg_vec_03_sum (m : Int) : sumCoordsB m = 2 * m + 7 := by unfold sumCoordsB; omega\n"
                "theorem alg_vec_03_m3 : sumCoordsB 3 = 13 := by decide\n\n"
                "#eval (detTransition 3, wCoordsB 3, sumCoordsB 3)\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m = sp.Symbol('m', integer=True)\n"
                "U = sp.Matrix([[1, 1, 1], [0, 1, 1], [0, 0, 1]])\n"
                "V_m = sp.Matrix([[2, 2, 2*m + 3], [1, 2, m + 3], [0, 1, 2]])\n"
                "C_m = sp.simplify(U.inv() * V_m)\n"
                "expected_C = sp.Matrix([[1, 0, m], [1, 1, m + 1], [0, 1, 2]])\n"
                "assert C_m == expected_C, f'Mismatch transition matrix: {C_m}'\n"
                "assert sp.simplify(C_m.det()) == 1, 'det(C_m) must be 1'\n"
                "w_Bp = sp.Matrix([1, 1, 1])\n"
                "w_B = sp.simplify(C_m * w_Bp)\n"
                "r_expr = sp.simplify(sum(w_B))\n"
                "assert sp.simplify(r_expr - (2*m + 7)) == 0\n\n"
                "for m_val in range(2, 10):\n"
                "    U_np = np.array([[1, 1, 1], [0, 1, 1], [0, 0, 1]], dtype=float)\n"
                "    V_np = np.array([[2, 2, 2*m_val + 3], [1, 2, m_val + 3], [0, 1, 2]], dtype=float)\n"
                "    C_np = np.linalg.inv(U_np) @ V_np\n"
                "    assert np.isclose(np.linalg.det(C_np), 1.0)\n"
                "    w_B_np = C_np @ np.ones(3)\n"
                "    assert np.allclose(w_B_np, [m_val + 1, m_val + 3, 3])\n"
                "    assert np.isclose(np.sum(w_B_np), 2*m_val + 7)\n\n"
                "print(f'VERIFIED_OK: ALG-VEC-03 det(C)=1, [w]_B={list(w_B)}, R(m)={r_expr}')\n"
            ),
        },
    ]
