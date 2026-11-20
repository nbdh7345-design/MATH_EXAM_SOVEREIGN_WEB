"""
Agent-16: Đại số — Ánh xạ tuyến tính, Hạt nhân Ker(f) & Ảnh Im(f)
Sinh và kiểm chứng câu hỏi Ma trận của ánh xạ tuyến tính, Hạt nhân Ker(f), Ảnh Im(f)
và Định lý số chiều (Rank-Nullity Theorem) chứa tham số m (SymPy + Core Lean 4).
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 16,
    "agent_code": "AGENT-16",
    "agent_name": "Agent-16 (Đại số: Ánh xạ tuyến tính, Hạt nhân Ker & Ảnh Im)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Ma trận của ánh xạ tuyến tính, Hạt nhân Ker(f), Ảnh Im(f) và Định lý số chiều theo tham số",
}


def get_questions() -> list[dict]:
    return [
        {
            "code": "ALG-MAP-01",
            "agent_id": 16,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Ánh xạ tuyến tính, Hạt nhân Ker(f) & Ảnh Im(f) chứa tham số",
            "question_type": "mcq",
            "difficulty": "Thông hiểu",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Điều kiện suy biến và số chiều hạt nhân Ker(f) của ánh xạ tuyến tính",
            "stem_symbolic": (
                r"Trong không gian véc-tơ $\mathbb{R}^3$ với cơ sở chính tắc, cho ánh xạ tuyến tính "
                r"$f: \mathbb{R}^3 \to \mathbb{R}^3$ có ma trận biểu diễn chứa tham số $m$ và hằng số thực $k$: "
                r"$$A = \begin{pmatrix} 1 & 1 & m \\ 2 & 3 & 3m+1 \\ 1 & m & k \end{pmatrix}$$"
                r"Xác định giá trị của $k$ theo tham số $m$ để hạt nhân của ánh xạ tuyến tính thỏa mãn $\dim\mathrm{Ker}(f) = 1$."
            ),
            "stem_template": (
                r"Trong không gian véc-tơ $\mathbb{{R}}^3$ với cơ sở chính tắc, cho ánh xạ tuyến tính "
                r"$f: \mathbb{{R}}^3 \to \mathbb{{R}}^3$ có ma trận biểu diễn (với $m = {m}$): "
                r"$$A = \begin{{pmatrix}} 1 & 1 & {m} \\ 2 & 3 & 3\cdot {m}+1 \\ 1 & {m} & k \end{{pmatrix}}$$"
                r"Xác định giá trị của $k$ để hạt nhân của ánh xạ tuyến tính thỏa mãn $\dim\mathrm{{Ker}}(f) = 1$."
            ),
            "options_symbolic": {
                "A": r"$k = m^2 + m - 1$",
                "B": r"$k = m^2 - m + 1$",
                "C": r"$k = m^2 + 2m + 1$",
                "D": r"$k = 2m^2 + m + 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2 + m - 1",
                    "B": "m**2 - m + 1",
                    "C": "m**2 + 2*m + 1",
                    "D": "2*m**2 + m + 1",
                },
                "target_expr": "m**2 + m - 1",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải tổng quát theo tham số $m$:**" "\n\n"
                r"1. **Áp dụng Định lý số chiều (Rank-Nullity Theorem):** "
                r"Với $f: \mathbb{R}^3 \to \mathbb{R}^3$, ta có $\dim\mathrm{Ker}(f) + \dim\mathrm{Im}(f) = 3$, "
                r"trong đó $\dim\mathrm{Im}(f) = \mathrm{rank}(A)$." "\n"
                r"   Do định thức con cấp 2 ở góc trên bên trái $\Delta_2 = \begin{vmatrix} 1 & 1 \\ 2 & 3 \end{vmatrix} = 1 \neq 0$, "
                r"nên $\mathrm{rank}(A) \ge 2$ với mọi $m, k$. Do đó:" "\n"
                r"   $$\dim\mathrm{Ker}(f) = 1 \iff \mathrm{rank}(A) = 2 \iff \det(A) = 0.$$" "\n"
                r"2. **Biến đổi sơ cấp hàng trên ma trận $A$:**" "\n"
                r"   - $R_2 \leftarrow R_2 - 2R_1 \implies (0,\; 1,\; m+1)$." "\n"
                r"   - $R_3 \leftarrow R_3 - R_1 \implies (0,\; m-1,\; k-m)$." "\n"
                r"   - $R_3 \leftarrow R_3 - (m-1)R_2 \implies (0,\; 0,\; k - m - (m^2 - 1)) = (0,\; 0,\; k - m^2 - m + 1)$." "\n"
                r"3. **Kết luận:** $\det(A) = k - m^2 - m + 1 = 0 \iff k = m^2 + m - 1$. Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Liên hệ dim Ker(f) = 1 với điều kiện hạng ma trận rank(A) = 2 theo Định lý số chiều (0.5đ)",
                "Thực hiện khử Gauss hoặc khai triển định thức det(A) = k - m^2 - m + 1 (0.5đ)",
                "Giải phương trình det(A) = 0 tìm được k = m^2 + m - 1 (0.5đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Formal Verification for ALG-MAP-01 (No Mathlib, Zero Sorry)\n"
                "def det3 (a11 a12 a13 a21 a22 a23 a31 a32 a33 : Int) : Int :=\n"
                "  a11 * (a22 * a33 - a23 * a32)\n"
                "  - a12 * (a21 * a33 - a23 * a31)\n"
                "  + a13 * (a21 * a32 - a22 * a31)\n\n"
                "def kTarget (m : Int) : Int := m * m + m - 1\n\n"
                "def detMap01 (m k : Int) : Int :=\n"
                "  det3 1 1 m 2 3 (3 * m + 1) 1 m k\n\n"
                "theorem alg_map_01_m3 : detMap01 3 (kTarget 3) = 0 ∧ kTarget 3 = 11 := by decide\n"
                "theorem alg_map_01_grid : (List.range 8).all (fun i =>\n"
                "  let m := Int.ofNat (i + 2)\n"
                "  detMap01 m (kTarget m) == 0) = true := by decide\n\n"
                "#eval (kTarget 3, detMap01 3 (kTarget 3))\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "m, k = sp.symbols('m k', integer=True)\n"
                "A = sp.Matrix([\n"
                "    [1, 1, m],\n"
                "    [2, 3, 3*m + 1],\n"
                "    [1, m, k]\n"
                "])\n"
                "det_A = sp.simplify(A.det())\n"
                "k_sol = sp.solve(sp.Eq(det_A, 0), k)[0]\n"
                "assert sp.simplify(k_sol - (m**2 + m - 1)) == 0, f'Unexpected k_sol: {k_sol}'\n\n"
                "for m_val in range(2, 10):\n"
                "    k_val = int(k_sol.subs(m, m_val))\n"
                "    A_num = A.subs({m: m_val, k: k_val})\n"
                "    rk = A_num.rank()\n"
                "    nullity = len(A_num.nullspace())\n"
                "    assert rk == 2 and nullity == 1 and rk + nullity == 3\n\n"
                "print(f'VERIFIED_OK: ALG-MAP-01 k(m) = {k_sol}, m=3 -> k={k_sol.subs(m, 3)}')\n"
            ),
        },
        {
            "code": "ALG-MAP-02",
            "agent_id": 16,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Ánh xạ tuyến tính, Hạt nhân Ker(f) & Ảnh Im(f) chứa tham số",
            "question_type": "mcq",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Tìm cơ sở của Hạt nhân Ker(f) và kiểm chứng Định lý số chiều",
            "stem_symbolic": (
                r"Cho ánh xạ tuyến tính $f: \mathbb{R}^3 \to \mathbb{R}^3$ xác định bởi công thức chứa tham số $m$: "
                r"$$f(x_1, x_2, x_3) = \big(x_1 + 2x_2 + m x_3,\; 2x_1 + 5x_2 + (3m+1)x_3,\; 3x_1 + 7x_2 + (4m+1)x_3\big)$$"
                r"Gọi $d = \dim\mathrm{Im}(f)$ và $u = (a, b, 1)$ là véc-tơ cơ sở của hạt nhân $\mathrm{Ker}(f)$. "
                r"Tính giá trị của biểu thức $Q = d \cdot a - b$ theo tham số $m$."
            ),
            "stem_template": (
                r"Cho ánh xạ tuyến tính $f: \mathbb{{R}}^3 \to \mathbb{{R}}^3$ xác định bởi công thức (với $m = {m}$): "
                r"$$f(x_1, x_2, x_3) = \big(x_1 + 2x_2 + {m}x_3,\; 2x_1 + 5x_2 + (3\cdot {m}+1)x_3,\; 3x_1 + 7x_2 + (4\cdot {m}+1)x_3\big)$$"
                r"Gọi $d = \dim\mathrm{{Im}}(f)$ và $u = (a, b, 1)$ là véc-tơ cơ sở của hạt nhân $\mathrm{{Ker}}(f)$. "
                r"Tính giá trị của biểu thức $Q = d \cdot a - b$."
            ),
            "options_symbolic": {
                "A": r"$Q = 3m + 3$",
                "B": r"$Q = 3m + 5$",
                "C": r"$Q = 2m + 3$",
                "D": r"$Q = m + 3$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "3*m + 3",
                    "B": "3*m + 5",
                    "C": "2*m + 3",
                    "D": "m + 3",
                },
                "target_expr": "3*m + 5",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Lời giải tổng quát theo tham số $m$:**" "\n\n"
                r"1. **Ma trận chính tắc và số chiều ảnh $\mathrm{Im}(f)$:**" "\n"
                r"   $$A = \begin{pmatrix} 1 & 2 & m \\ 2 & 5 & 3m+1 \\ 3 & 7 & 4m+1 \end{pmatrix}$$" "\n"
                r"   Nhận thấy $R_3 = R_1 + R_2$ và định thức con $\begin{vmatrix} 1 & 2 \\ 2 & 5 \end{vmatrix} = 1 \neq 0$, "
                r"suy ra $d = \dim\mathrm{Im}(f) = \mathrm{rank}(A) = 2$ và $\dim\mathrm{Ker}(f) = 3 - 2 = 1$." "\n"
                r"2. **Tìm véc-tơ cơ sở $u = (a, b, 1) \in \mathrm{Ker}(f)$:**" "\n"
                r"   Giải hệ phương trình $A u^T = 0$ với $x_3 = 1$:" "\n"
                r"   $$\begin{cases} a + 2b + m = 0 \\ 2a + 5b + 3m + 1 = 0 \end{cases} "
                r"\iff \begin{cases} a = m + 2 \\ b = -(m + 1) \end{cases}$$" "\n"
                r"3. **Tính biểu thức $Q$:**" "\n"
                r"   $$Q = d \cdot a - b = 2(m + 2) - (-(m + 1)) = 3m + 5.$$" "\n"
                r"   Chọn đáp án **B**."
            ),
            "rubric_points": [
                "Lập ma trận chính tắc A và xác định d = dim Im(f) = rank(A) = 2 (0.5đ)",
                "Giải hệ thuần nhất tìm cơ sở Ker(f) là u = (m+2, -(m+1), 1) (0.5đ)",
                "Tính chính xác Q = d*a - b = 3m + 5 (0.5đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Formal Verification for ALG-MAP-02 (No Mathlib, Zero Sorry)\n"
                "def fMap02 (m x1 x2 x3 : Int) : Int × Int × Int :=\n"
                "  (x1 + 2 * x2 + m * x3,\n"
                "   2 * x1 + 5 * x2 + (3 * m + 1) * x3,\n"
                "   3 * x1 + 7 * x2 + (4 * m + 1) * x3)\n\n"
                "def aKer (m : Int) : Int := m + 2\n"
                "def bKer (m : Int) : Int := -(m + 1)\n"
                "def qTarget (m : Int) : Int := 2 * (aKer m) - (bKer m)\n\n"
                "theorem alg_map_02_m3 :\n"
                "    fMap02 3 (aKer 3) (bKer 3) 1 = (0, 0, 0) ∧ qTarget 3 = 14 := by decide\n\n"
                "theorem alg_map_02_grid : (List.range 8).all (fun i =>\n"
                "  let m := Int.ofNat (i + 2)\n"
                "  (fMap02 m (aKer m) (bKer m) 1 == (0, 0, 0)) && (qTarget m == 3 * m + 5)) = true := by decide\n\n"
                "#eval (aKer 3, bKer 3, qTarget 3)\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "m = sp.Symbol('m', integer=True)\n"
                "A = sp.Matrix([\n"
                "    [1, 2, m],\n"
                "    [2, 5, 3*m + 1],\n"
                "    [3, 7, 4*m + 1]\n"
                "])\n"
                "ns = A.nullspace()\n"
                "assert len(ns) == 1\n"
                "u = sp.simplify(ns[0] / ns[0][2])\n"
                "a_expr, b_expr = sp.simplify(u[0]), sp.simplify(u[1])\n"
                "assert sp.simplify(a_expr - (m + 2)) == 0\n"
                "assert sp.simplify(b_expr - (-(m + 1))) == 0\n"
                "Q_expr = sp.simplify(2 * a_expr - b_expr)\n"
                "assert sp.simplify(Q_expr - (3*m + 5)) == 0\n\n"
                "for m_val in range(2, 10):\n"
                "    A_num = A.subs(m, m_val)\n"
                "    d_val = A_num.rank()\n"
                "    ns_num = A_num.nullspace()[0]\n"
                "    ns_norm = ns_num / ns_num[2]\n"
                "    q_num = int(d_val * ns_norm[0] - ns_norm[1])\n"
                "    assert d_val == 2 and q_num == 3 * m_val + 5\n\n"
                "print(f'VERIFIED_OK: ALG-MAP-02 Q(m) = {Q_expr}, m=3 -> Q={Q_expr.subs(m, 3)}')\n"
            ),
        },
        {
            "code": "ALG-MAP-03",
            "agent_id": 16,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Ánh xạ tuyến tính, Hạt nhân Ker(f) & Ảnh Im(f) chứa tham số",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": {
                "m": {"type": "int", "default": 3, "min": 2, "max": 9, "step": 1, "label": "Tham số m"}
            },
            "title": "Bài toán tự luận tổng hợp: Cơ sở của Ker(f), Im(f) và điều kiện thuộc ảnh",
            "stem_symbolic": (
                r"Cho ánh xạ tuyến tính $f: \mathbb{R}^4 \to \mathbb{R}^3$ xác định đối với cặp cơ sở chính tắc bởi công thức chứa tham số $m$: "
                r"$$f(x_1, x_2, x_3, x_4) = \big(x_1 + 2x_2 - x_3 + m x_4,\; 2x_1 + 5x_2 + (2m+1)x_4,\; (m+2)x_1 + (2m+5)x_2 - m x_3 + (m^2+2m+1)x_4\big)$$"
                r"a) Lập ma trận chính tắc $A$ của ánh xạ tuyến tính $f$ và đưa $A$ về dạng bậc thang rút gọn (RREF)." "\n"
                r"b) Tìm số chiều và một cơ sở của $\mathrm{Ker}(f)$ và $\mathrm{Im}(f)$ theo $m$. Kiểm nghiệm Định lý số chiều." "\n"
                r"c) Tìm điều kiện của $\lambda$ (theo $m$) để véc-tơ $b = (1, 2, \lambda)^T \in \mathrm{Im}(f)$."
            ),
            "stem_template": (
                r"Cho ánh xạ tuyến tính $f: \mathbb{{R}}^4 \to \mathbb{{R}}^3$ xác định đối với cặp cơ sở chính tắc (với $m = {m}$): "
                r"$$f(x_1, x_2, x_3, x_4) = \big(x_1 + 2x_2 - x_3 + {m}x_4,\; 2x_1 + 5x_2 + (2\cdot {m}+1)x_4,\; ({m}+2)x_1 + (2\cdot {m}+5)x_2 - {m}x_3 + ({m}^2+2\cdot {m}+1)x_4\big)$$"
                r"a) Lập ma trận chính tắc $A$ của ánh xạ tuyến tính $f$ và đưa $A$ về dạng bậc thang rút gọn (RREF)." "\n"
                r"b) Tìm số chiều và một cơ sở của $\mathrm{{Ker}}(f)$ và $\mathrm{{Im}}(f)$. Kiểm nghiệm Định lý số chiều." "\n"
                r"c) Tìm điều kiện của $\lambda$ để véc-tơ $b = (1, 2, \lambda)^T \in \mathrm{{Im}}(f)$."
            ),
            "options_symbolic": {
                "A": r"$\dim\mathrm{Ker}(f)=2,\; \dim\mathrm{Im}(f)=2,\; \lambda = m + 2$",
                "B": r"$\dim\mathrm{Ker}(f)=1,\; \dim\mathrm{Im}(f)=3,\; \lambda = 2m + 1$",
                "C": r"$\dim\mathrm{Ker}(f)=2,\; \dim\mathrm{Im}(f)=2,\; \lambda = 2m + 3$",
                "D": r"$\dim\mathrm{Ker}(f)=3,\; \dim\mathrm{Im}(f)=1,\; \lambda = m - 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m + 2",
                    "B": "2*m + 1",
                    "C": "2*m + 3",
                    "D": "m - 2",
                },
                "target_expr": "m + 2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải tự luận chi tiết theo tham số $m$:**" "\n\n"
                r"**Phần a) Ma trận chính tắc $A$ và dạng bậc thang rút gọn (RREF):**" "\n"
                r"$$A = \begin{pmatrix} 1 & 2 & -1 & m \\ 2 & 5 & 0 & 2m+1 \\ m+2 & 2m+5 & -m & m^2+2m+1 \end{pmatrix}$$" "\n"
                r"Nhận thấy dòng 3 thỏa mãn $R_3 = m R_1 + R_2$. Thực hiện biến đổi sơ cấp hàng:" "\n"
                r"- $R_2 \leftarrow R_2 - 2R_1 = (0,\; 1,\; 2,\; 1)$" "\n"
                r"- $R_3 \leftarrow R_3 - m R_1 - R_2 = (0,\; 0,\; 0,\; 0)$" "\n"
                r"- $R_1 \leftarrow R_1 - 2R_2 = (1,\; 0,\; -5,\; m-2)$" "\n"
                r"Ta thu được ma trận bậc thang rút gọn:" "\n"
                r"$$\mathrm{RREF}(A) = \begin{pmatrix} 1 & 0 & -5 & m-2 \\ 0 & 1 & 2 & 1 \\ 0 & 0 & 0 & 0 \end{pmatrix}$$" "\n\n"
                r"**Phần b) Cơ sở, số chiều của $\mathrm{Ker}(f)$, $\mathrm{Im}(f)$ và Định lý số chiều:**" "\n"
                r"- Có 2 cột chốt (cột 1 và cột 2) nên $\dim\mathrm{Im}(f) = \mathrm{rank}(A) = 2$. "
                r"Cơ sở của $\mathrm{Im}(f)$ gồm 2 cột đầu của $A$: "
                r"$c_1 = (1, 2, m+2)^T,\; c_2 = (2, 5, 2m+5)^T$." "\n"
                r"- Hệ thuần nhất $Ax = 0 \iff \begin{cases} x_1 = 5x_3 + (2-m)x_4 \\ x_2 = -2x_3 - x_4 \end{cases}$." "\n"
                r"  Suy ra $\dim\mathrm{Ker}(f) = 2$ với cơ sở gồm 2 véc-tơ độc lập tuyến tính: "
                r"$u_1 = (5, -2, 1, 0)^T$ và $u_2 = (2-m, -1, 0, 1)^T$." "\n"
                r"- Kiểm nghiệm Định lý số chiều: $\dim\mathrm{Ker}(f) + \dim\mathrm{Im}(f) = 2 + 2 = 4 = \dim(\mathbb{R}^4)$." "\n\n"
                r"**Phần c) Điều kiện để $b = (1, 2, \lambda)^T \in \mathrm{Im}(f)$:**" "\n"
                r"Do mọi véc-tơ $y = (y_1, y_2, y_3)^T \in \mathrm{Im}(f)$ đều thỏa mãn hệ thức dòng $y_3 = m y_1 + y_2$, "
                r"nên $b \in \mathrm{Im}(f) \iff \lambda = m \cdot 1 + 2 = m + 2$ (khi đó $b = c_1 = f(e_1)$)."
            ),
            "rubric_points": [
                "Phần a: Viết đúng ma trận chính tắc A cỡ 3x4 và biến đổi về RREF(A) (1.0đ)",
                "Phần b: Tìm đúng cơ sở Im(f), cơ sở Ker(f) = {(5,-2,1,0), (2-m,-1,0,1)} và kiểm nghiệm dim Ker(f) + dim Im(f) = 4 (1.5đ)",
                "Phần c: Biiện luận hạng ma trận bổ sung [A|b] tìm đúng điều kiện lambda = m + 2 (0.5đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Formal Verification for ALG-MAP-03 (No Mathlib, Zero Sorry)\n"
                "def fMap03 (m x1 x2 x3 x4 : Int) : Int × Int × Int :=\n"
                "  (x1 + 2 * x2 - x3 + m * x4,\n"
                "   2 * x1 + 5 * x2 + (2 * m + 1) * x4,\n"
                "   (m + 2) * x1 + (2 * m + 5) * x2 - m * x3 + (m * m + 2 * m + 1) * x4)\n\n"
                "def lambdaTarget (m : Int) : Int := m + 2\n\n"
                "theorem alg_map_03_ker_and_im_m3 :\n"
                "    fMap03 3 5 (-2) 1 0 = (0, 0, 0)\n"
                "    ∧ fMap03 3 (2 - 3) (-1) 0 1 = (0, 0, 0)\n"
                "    ∧ fMap03 3 1 0 0 0 = (1, 2, lambdaTarget 3) := by decide\n\n"
                "theorem alg_map_03_grid : (List.range 8).all (fun i =>\n"
                "  let m := Int.ofNat (i + 2)\n"
                "  (fMap03 m 5 (-2) 1 0 == (0, 0, 0))\n"
                "  && (fMap03 m (2 - m) (-1) 0 1 == (0, 0, 0))\n"
                "  && (fMap03 m 1 0 0 0 == (1, 2, lambdaTarget m))) = true := by decide\n\n"
                "#eval (lambdaTarget 3, fMap03 3 (2 - 3) (-1) 0 1, fMap03 3 1 0 0 0)\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "m, lam = sp.symbols('m lam', integer=True)\n"
                "A = sp.Matrix([\n"
                "    [1, 2, -1, m],\n"
                "    [2, 5, 0, 2*m + 1],\n"
                "    [m + 2, 2*m + 5, -m, m**2 + 2*m + 1]\n"
                "])\n"
                "rref_A, pivots = A.rref()\n"
                "assert pivots == (0, 1)\n"
                "assert sp.simplify(rref_A[0, 3] - (m - 2)) == 0\n"
                "u1 = sp.Matrix([5, -2, 1, 0])\n"
                "u2 = sp.Matrix([2 - m, -1, 0, 1])\n"
                "assert sp.simplify(A * u1) == sp.zeros(3, 1)\n"
                "assert sp.simplify(A * u2) == sp.zeros(3, 1)\n\n"
                "for m_val in range(2, 10):\n"
                "    A_num = A.subs(m, m_val)\n"
                "    rk = A_num.rank()\n"
                "    nullity = len(A_num.nullspace())\n"
                "    assert rk == 2 and nullity == 2 and rk + nullity == 4\n"
                "    Aug = A_num.row_join(sp.Matrix([1, 2, m_val + 2]))\n"
                "    assert Aug.rank() == rk\n\n"
                "print(f'VERIFIED_OK: ALG-MAP-03 rank=2, nullity=2, lambda(m)=m+2, m=3 -> lambda={3+2}')\n"
            ),
        },
    ]
