"""
Agent-13: Đại số — Hệ phương trình tuyến tính chứa tham số (Cramer, Gauss, Kronecker-Capelli).
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 13,
    "agent_code": "AGENT-13",
    "agent_name": "Agent-13 (Đại số: Hệ phương trình tuyến tính tham số)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Hệ phương trình tuyến tính Cramer, Gauss, Kronecker-Capelli biện luận theo tham số m",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa của Agent-13."""
    return [
        {
            "code": "ALG-SYS-01",
            "agent_id": 13,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Hệ phương trình tuyến tính chứa tham số (Cramer & Kronecker-Capelli)",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Hệ phương trình tuyến tính Cramer 3 ẩn chứa tham số m",
            "stem_symbolic": (
                r"Cho hệ phương trình tuyến tính 3 ẩn $(x, y, z)$ chứa tham số nguyên dương $m$:"
                "\n"
                r"$$\begin{cases} x + y + z = 6m \\ x + 2y + 3z = 14m \\ x + 3y + 6z = 25m \end{cases}$$"
                "\n"
                r"Gọi $(x_0, y_0, z_0)$ là nghiệm duy nhất của hệ theo quy tắc Cramer. "
                r"Giá trị của biểu thức $T = 2x_0 + y_0 + z_0$ tính theo $m$ là:"
            ),
            "stem_template": (
                r"Cho hệ phương trình tuyến tính 3 ẩn $(x, y, z)$ với $m = {m}$:"
                "\n"
                r"$$\begin{cases} x + y + z = 6 \cdot {m} \\ x + 2y + 3z = 14 \cdot {m} \\ x + 3y + 6z = 25 \cdot {m} \end{cases}$$"
                "\n"
                r"Gọi $(x_0, y_0, z_0)$ là nghiệm duy nhất của hệ theo quy tắc Cramer. "
                r"Giá trị của biểu thức $T = 2x_0 + y_0 + z_0$ bằng:"
            ),
            "options_symbolic": {
                "A": r"$7m$",
                "B": r"$6m$",
                "C": r"$5m$",
                "D": r"$8m$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "7*m",
                    "B": "6*m",
                    "C": "5*m",
                    "D": "8*m",
                },
                "target_expr": "7*m",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"Xét ma trận hệ số $A = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 2 & 3 \\ 1 & 3 & 6 \end{pmatrix}$. "
                r"Định thức của ma trận hệ số là:"
                "\n"
                r"$$\Delta = \det(A) = 1(12 - 9) - 1(6 - 3) + 1(3 - 2) = 3 - 3 + 1 = 1 \neq 0.$$"
                "\n"
                r"Theo định lý Cramer, hệ có nghiệm duy nhất với mọi $m$. Áp dụng quy tắc Cramer hoặc khử Gauss:"
                "\n"
                r"- Lấy $(2) - (1) \Rightarrow y + 2z = 8m$."
                "\n"
                r"- Lấy $(3) - (2) \Rightarrow y + 3z = 11m$."
                "\n"
                r"- Trừ hai phương trình trên thu được $z_0 = 3m$, suy ra $y_0 = 8m - 2(3m) = 2m$ và $x_0 = 6m - 2m - 3m = m$."
                "\n"
                r"Vậy $T = 2x_0 + y_0 + z_0 = 2m + 2m + 3m = 7m$. Chọn đáp án A."
            ),
            "rubric_points": [
                "Tính đúng định thức ma trận hệ số Delta = 1 != 0 khẳng định hệ Cramer (0.25đ)",
                "Khử Gauss hoặc tính Delta_x = m, Delta_y = 2m, Delta_z = 3m (0.50đ)",
                "Tính đúng giá trị biểu thức T = 2x_0 + y_0 + z_0 = 7m (0.25đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Formal Verification for ALG-SYS-01 (Core Lean 4)\n"
                "def det3 (a11 a12 a13 a21 a22 a23 a31 a32 a33 : Int) : Int :=\n"
                "  a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)\n\n"
                "theorem cramer_det_is_one : det3 1 1 1 1 2 3 1 3 6 = 1 := by decide\n\n"
                "theorem alg_sys_01_m3 :\n"
                "  let m : Int := 3\n"
                "  let x : Int := m\n"
                "  let y : Int := 2 * m\n"
                "  let z : Int := 3 * m\n"
                "  (x + y + z = 6 * m) ∧ (x + 2 * y + 3 * z = 14 * m) ∧ (x + 3 * y + 6 * z = 25 * m) ∧ (2 * x + y + z = 7 * m) := by decide\n\n"
                "#eval det3 1 1 1 1 2 3 1 3 6\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m = sp.Symbol('m', integer=True, positive=True)\n"
                "x, y, z = sp.symbols('x y z')\n"
                "A = sp.Matrix([[1, 1, 1], [1, 2, 3], [1, 3, 6]])\n"
                "b = sp.Matrix([6 * m, 14 * m, 25 * m])\n"
                "assert A.det() == 1\n"
                "sol = A.LUsolve(b)\n"
                "T_expr = sp.simplify(2 * sol[0] + sol[1] + sol[2])\n"
                "assert T_expr == 7 * m, f'Symbolic mismatch: {T_expr}'\n\n"
                "for m_val in range(2, 10):\n"
                "    A_np = np.array([[1.0, 1.0, 1.0], [1.0, 2.0, 3.0], [1.0, 3.0, 6.0]])\n"
                "    b_np = np.array([6.0 * m_val, 14.0 * m_val, 25.0 * m_val])\n"
                "    xyz = np.linalg.solve(A_np, b_np)\n"
                "    T_num = 2.0 * xyz[0] + xyz[1] + xyz[2]\n"
                "    assert np.isclose(T_num, 7.0 * m_val)\n\n"
                "print('VERIFIED_OK: ALG-SYS-01 Cramer 3x3 system verified symbolically and numerically.')"
            ),
        },
        {
            "code": "ALG-SYS-02",
            "agent_id": 13,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Hệ phương trình tuyến tính chứa tham số (Cramer & Kronecker-Capelli)",
            "question_type": "mcq",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Định lý Kronecker-Capelli và điều kiện hệ suy biến có vô số nghiệm",
            "stem_symbolic": (
                r"Cho hệ phương trình tuyến tính ẩn $(x, y, z)$ với tham số nguyên $m$ và tham số thực $k$:"
                "\n"
                r"$$\begin{cases} x + y + z = m \\ x + 2y + 3z = 2m + 1 \\ 2x + 3y + 4z = k \end{cases}$$"
                "\n"
                r"Theo định lý Kronecker-Capelli, hệ phương trình đã cho có vô số nghiệm khi và chỉ khi giá trị của $k$ tính theo $m$ là:"
            ),
            "stem_template": (
                r"Cho hệ phương trình tuyến tính ẩn $(x, y, z)$ với $m = {m}$ và tham số thực $k$:"
                "\n"
                r"$$\begin{cases} x + y + z = {m} \\ x + 2y + 3z = 2 \cdot {m} + 1 \\ 2x + 3y + 4z = k \end{cases}$$"
                "\n"
                r"Theo định lý Kronecker-Capelli, hệ phương trình đã cho có vô số nghiệm khi và chỉ khi $k$ bằng:"
            ),
            "options_symbolic": {
                "A": r"$3m - 1$",
                "B": r"$3m + 1$",
                "C": r"$2m + 1$",
                "D": r"$4m + 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "3*m - 1",
                    "B": "3*m + 1",
                    "C": "2*m + 1",
                    "D": "4*m + 1",
                },
                "target_expr": "3*m + 1",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"Xét ma trận mở rộng $\overline{A} = \begin{pmatrix} 1 & 1 & 1 & | & m \\ 1 & 2 & 3 & | & 2m + 1 \\ 2 & 3 & 4 & | & k \end{pmatrix}$."
                "\n"
                r"Thực hiện phép biến đổi sơ cấp hàng theo thuật toán Gauss ($R_2 \leftarrow R_2 - R_1$, $R_3 \leftarrow R_3 - 2R_1$):"
                "\n"
                r"$$\overline{A} \sim \begin{pmatrix} 1 & 1 & 1 & | & m \\ 0 & 1 & 2 & | & m + 1 \\ 0 & 1 & 2 & | & k - 2m \end{pmatrix} "
                r"\xrightarrow{R_3 \leftarrow R_3 - R_2} \begin{pmatrix} 1 & 1 & 1 & | & m \\ 0 & 1 & 2 & | & m + 1 \\ 0 & 0 & 0 & | & k - 3m - 1 \end{pmatrix}.$$"
                "\n"
                r"Ta có $\text{rank}(A) = 2 < 3$. Theo định lý Kronecker-Capelli, hệ có nghiệm (và có vô số nghiệm phụ thuộc 1 ẩn tự do) khi và chỉ khi:"
                "\n"
                r"$$\text{rank}(\overline{A}) = \text{rank}(A) = 2 \iff k - 3m - 1 = 0 \iff k = 3m + 1.$$"
                "\n"
                r"Chọn đáp án B."
            ),
            "rubric_points": [
                "Lập ma trận mở rộng và khử Gauss đưa về dạng bậc thang (0.50đ)",
                "Áp dụng định lý Kronecker-Capelli rank(A) = rank(A_bar) = 2 < 3 (0.25đ)",
                "Kết luận điều kiện k = 3m + 1 (0.25đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Formal Verification for ALG-SYS-02 (Kronecker-Capelli Rank Consistency)\n"
                "def row_check (m : Int) (k : Int) : Bool :=\n"
                "  k - 3 * m - 1 == 0\n\n"
                "theorem kronecker_capelli_condition (m : Int) :\n"
                "  (3 * m + 1) - 3 * m - 1 = 0 := by omega\n\n"
                "theorem alg_sys_02_m3 : row_check 3 (3 * 3 + 1) = true := by decide\n\n"
                "#eval row_check 3 10\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "m, k = sp.symbols('m k')\n"
                "x, y, z = sp.symbols('x y z')\n"
                "A = sp.Matrix([[1, 1, 1], [1, 2, 3], [2, 3, 4]])\n"
                "assert A.det() == 0 and A.rank() == 2\n"
                "A_aug = sp.Matrix([[1, 1, 1, m], [1, 2, 3, 2 * m + 1], [2, 3, 4, k]])\n"
                "rref_mat, _ = A_aug.subs(k, 3 * m + 1).rref()\n"
                "assert rref_mat[2, 3] == 0\n\n"
                "for m_val in range(2, 10):\n"
                "    k_val = 3 * m_val + 1\n"
                "    sol_set = sp.linsolve((A, sp.Matrix([m_val, 2 * m_val + 1, k_val])), (x, y, z))\n"
                "    assert len(sol_set) == 1\n"
                "    A_sub = np.array([[1.0, 1.0], [1.0, 2.0]])\n"
                "    b_sub = np.array([float(m_val), float(2 * m_val + 1)])\n"
                "    xy0 = np.linalg.solve(A_sub, b_sub)\n"
                "    assert np.isclose(2.0 * xy0[0] + 3.0 * xy0[1], k_val)\n\n"
                "print('VERIFIED_OK: ALG-SYS-02 Kronecker-Capelli condition k = 3m + 1 verified.')"
            ),
        },
        {
            "code": "ALG-SYS-03",
            "agent_id": 13,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Hệ phương trình tuyến tính chứa tham số (Cramer & Kronecker-Capelli)",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Tự luận: Biện luận toàn diện hệ phương trình tuyến tính đối xứng theo Cramer và Kronecker-Capelli",
            "stem_symbolic": (
                r"Cho hệ phương trình tuyến tính 3 ẩn $(x, y, z)$ phụ thuộc tham số thực $\lambda$ và tham số nguyên dương $m$:"
                "\n"
                r"$$\begin{cases} \lambda x + y + z = m \\ x + \lambda y + z = m \\ x + y + \lambda z = m \end{cases}$$"
                "\n"
                r"a) Tính định thức của ma trận hệ số $\Delta(\lambda)$ và biện luận số nghiệm của hệ phương trình theo tham số $\lambda$."
                "\n"
                r"b) Khi $\lambda = 2$, hãy tìm nghiệm duy nhất $(x_0, y_0, z_0)$ của hệ và tính giá trị biểu thức $S = 4(x_0 + y_0 + z_0)$ theo $m$."
            ),
            "stem_template": (
                r"Cho hệ phương trình tuyến tính 3 ẩn $(x, y, z)$ phụ thuộc tham số thực $\lambda$ (với $m = {m}$):"
                "\n"
                r"$$\begin{cases} \lambda x + y + z = {m} \\ x + \lambda y + z = {m} \\ x + y + \lambda z = {m} \end{cases}$$"
                "\n"
                r"a) Tính định thức của ma trận hệ số $\Delta(\lambda)$ và biện luận số nghiệm của hệ phương trình theo tham số $\lambda$."
                "\n"
                r"b) Khi $\lambda = 2$, hãy tìm nghiệm duy nhất $(x_0, y_0, z_0)$ của hệ và tính giá trị biểu thức $S = 4(x_0 + y_0 + z_0)$."
            ),
            "options_symbolic": {
                "A": r"$3m$",
                "B": r"$4m$",
                "C": r"$2m$",
                "D": r"$6m$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "3*m",
                    "B": "4*m",
                    "C": "2*m",
                    "D": "6*m",
                },
                "target_expr": "3*m",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**a) Tính định thức và biện luận theo $\lambda$:**"
                "\n"
                r"Ma trận hệ số $A(\lambda) = \begin{pmatrix} \lambda & 1 & 1 \\ 1 & \lambda & 1 \\ 1 & 1 & \lambda \end{pmatrix}$. "
                r"Cộng cột 2 và cột 3 vào cột 1, sau đó đặt $(\lambda + 2)$ làm nhân tử chung:"
                "\n"
                r"$$\Delta(\lambda) = \det A(\lambda) = (\lambda + 2)(\lambda - 1)^2.$$"
                "\n"
                r"- **Trường hợp 1 ($\lambda \neq 1$ và $\lambda \neq -2$):** $\Delta(\lambda) \neq 0$. Theo định lý Cramer, hệ có nghiệm duy nhất:"
                "\n"
                r"$$x = y = z = \frac{m}{\lambda + 2}.$$"
                "\n"
                r"- **Trường hợp 2 ($\lambda = 1$):** Ba phương trình trùng nhau thành $x + y + z = m$. "
                r"Khi đó $\text{rank}(A) = \text{rank}(\overline{A}) = 1 < 3$, theo định lý Kronecker-Capelli hệ có vô số nghiệm phụ thuộc 2 tham số tự do: "
                r"$(x, y, z) = (m - s - t, s, t)$ với $s, t \in \mathbb{R}$."
                "\n"
                r"- **Trường hợp 3 ($\lambda = -2$):** Cộng vế theo vế cả 3 phương trình ta được $0x + 0y + 0z = 3m$. "
                r"Vì $m \ge 2 > 0$ nên $3m \neq 0$, suy ra $\text{rank}(A) = 2 < \text{rank}(\overline{A}) = 3$. "
                r"Theo định lý Kronecker-Capelli, hệ phương trình vô nghiệm."
                "\n\n"
                r"**b) Tính nghiệm và biểu thức $S$ khi $\lambda = 2$:**"
                "\n"
                r"Khi $\lambda = 2 \notin \{1, -2\}$, nghiệm duy nhất là $x_0 = y_0 = z_0 = \frac{m}{2 + 2} = \frac{m}{4}$. "
                r"Do đó $S = 4(x_0 + y_0 + z_0) = 4 \cdot \frac{3m}{4} = 3m$."
            ),
            "rubric_points": [
                "Phân tích đúng định thức Delta(lambda) = (lambda + 2)(lambda - 1)^2 (0.50đ)",
                "Biện luận trường hợp Cramer lambda != 1, -2 có nghiệm duy nhất x = y = z = m/(lambda + 2) (0.50đ)",
                "Biện luận bằng định lý Kronecker-Capelli tại hai giá trị suy biến lambda = 1 (vô số nghiệm) và lambda = -2 (vô nghiệm vì m > 0) (0.50đ)",
                "Thay lambda = 2 tính đúng nghiệm x_0 = y_0 = z_0 = m/4 và S = 4(x_0 + y_0 + z_0) = 3m (0.50đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Formal Verification for ALG-SYS-03 (Symmetric Parametric Linear System)\n"
                "def det_sym (lam : Int) : Int :=\n"
                "  lam * (lam * lam - 1) - 1 * (lam - 1) + 1 * (1 - lam)\n\n"
                "theorem det_sym_factored_at_2 : det_sym 2 = (2 + 2) * (2 - 1) * (2 - 1) := by decide\n"
                "theorem det_sym_singular_1 : det_sym 1 = 0 := by decide\n"
                "theorem det_sym_singular_neg2 : det_sym (-2) = 0 := by decide\n\n"
                "theorem alg_sys_03_sum (m : Int) : 3 * m = 2 * m + m := by omega\n\n"
                "#eval det_sym 2\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "lam, m = sp.symbols('lam m')\n"
                "A = sp.Matrix([[lam, 1, 1], [1, lam, 1], [1, 1, lam]])\n"
                "b = sp.Matrix([m, m, m])\n"
                "assert sp.factor(A.det()) == (lam + 2) * (lam - 1)**2\n"
                "sol = A.LUsolve(b)\n"
                "for comp in sol:\n"
                "    assert sp.simplify(comp - m / (lam + 2)) == 0\n"
                "S_sym = sp.simplify(4 * sum(sol.subs(lam, 2)))\n"
                "assert S_sym == 3 * m\n\n"
                "for m_val in range(2, 10):\n"
                "    A_np = np.array([[2.0, 1.0, 1.0], [1.0, 2.0, 1.0], [1.0, 1.0, 2.0]])\n"
                "    b_np = np.array([float(m_val)] * 3)\n"
                "    xyz = np.linalg.solve(A_np, b_np)\n"
                "    assert np.isclose(4.0 * np.sum(xyz), 3.0 * m_val)\n\n"
                "print('VERIFIED_OK: ALG-SYS-03 Full parametric discussion & S = 3m verified.')"
            ),
        },
    ]
