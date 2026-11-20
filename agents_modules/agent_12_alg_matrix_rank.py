# -*- coding: utf-8 -*-
"""
Agent-12: Đại số — Hạng của ma trận phụ thuộc tham số (Matrix Rank with Parameters)
Sinh & kiểm chứng câu hỏi Biện luận hạng của ma trận rank(A(m)) bằng biến đổi sơ cấp Gauss và định thức con.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 12,
    "agent_code": "AGENT-12",
    "agent_name": "Agent-12 (Đại số: Hạng của ma trận theo tham số)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Biện luận hạng của ma trận rank(A(m)) bằng biến đổi sơ cấp Gauss và định thức con",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa (2 MCQ, 1 Essay) về hạng của ma trận theo tham số."""
    return [
        {
            "code": "ALG-RNK-01",
            "agent_id": 12,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Hạng của ma trận phụ thuộc tham số",
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
                    "label": "Tham số nguyên m",
                }
            },
            "title": "Tìm tham số để ma trận cỡ 3x4 đạt hạng cực tiểu bằng khử Gauss",
            "stem_symbolic": (
                r"Cho ma trận thực $A(k) \in M_{3\times 4}(\mathbb{R})$ phụ thuộc tham số thực $k$ "
                r"(với hằng số nguyên $m \ge 2$):"
                "\n"
                r"$$A(k) = \begin{pmatrix} 1 & 2 & -1 & m \\ 2 & 5 & 1 & 2m+1 \\ 3 & 7 & k - 2m & 3m+1 \end{pmatrix}$$"
                "\n"
                r"Tìm giá trị của $k$ theo $m$ để $\operatorname{rank}(A(k)) = 2$."
            ),
            "stem_template": (
                r"Cho ma trận thực $A(k) \in M_{3\times 4}(\mathbb{R})$ phụ thuộc tham số thực $k$ "
                r"(với $m = {m}$):"
                "\n"
                r"$$A(k) = \begin{pmatrix} 1 & 2 & -1 & {m} \\ 2 & 5 & 1 & 2\cdot {m}+1 \\ 3 & 7 & k - 2\cdot {m} & 3\cdot {m}+1 \end{pmatrix}$$"
                "\n"
                r"Tìm giá trị của $k$ để $\operatorname{rank}(A(k)) = 2$."
            ),
            "options_symbolic": {
                "A": r"$k = 2m$",
                "B": r"$k = m - 1$",
                "C": r"$k = 3m + 1$",
                "D": r"$k = m^2 + 2m + 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m",
                    "B": "m - 1",
                    "C": "3*m + 1",
                    "D": "m**2 + 2*m + 2",
                },
                "target_expr": "2*m",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"Thực hiện biến đổi sơ cấp theo hàng (khử Gauss) trên ma trận $A(k)$:" "\n"
                r"- Bước 1: $R_2 \leftarrow R_2 - 2R_1$ và $R_3 \leftarrow R_3 - 3R_1$, ta thu được:" "\n"
                r"$$A(k) \sim \begin{pmatrix} 1 & 2 & -1 & m \\ 0 & 1 & 3 & 1 \\ 0 & 1 & k - 2m + 3 & 1 \end{pmatrix}$$" "\n"
                r"- Bước 2: $R_3 \leftarrow R_3 - R_2$, ta đưa ma trận về dạng bậc thang:" "\n"
                r"$$U(k) = \begin{pmatrix} 1 & 2 & -1 & m \\ 0 & 1 & 3 & 1 \\ 0 & 0 & k - 2m & 0 \end{pmatrix}$$" "\n"
                r"- Ma trận con cấp 2 ở góc trên bên trái $\begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix}$ có định thức bằng $1 \ne 0$, "
                r"do đó $\operatorname{rank}(A(k)) \ge 2$ với mọi $k, m$." "\n"
                r"- Để $\operatorname{rank}(A(k)) = 2$, hàng thứ 3 của $U(k)$ phải bằng véctơ không, tức là $k - 2m = 0 \iff k = 2m$."
            ),
            "rubric_points": [
                {"step": "Khử Gauss hàng 2 và hàng 3 về dạng trung gian", "points": 0.4},
                {"step": "Đưa về ma trận bậc thang U(k) với phần tử chốt (3,3) là k - 2m", "points": 0.4},
                {"step": "Kết luận điều kiện rank(A(k)) = 2 khi và chỉ khi k = 2m", "points": 0.2},
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-RNK-01 (no Mathlib, no sorry)\n"
                "def pivot33 (k m : Int) : Int := (k - 2 * m + 3) - 3\n\n"
                "def rank3x4 (k m : Int) : Nat :=\n"
                "  if pivot33 k m == 0 then 2 else 3\n\n"
                "theorem alg_rnk_01_critical_rank (m : Int) :\n"
                "    rank3x4 (2 * m) m = 2 := by\n"
                "  unfold rank3x4 pivot33\n"
                "  have h : (2 * m - 2 * m + 3 - 3 == 0) = true := by\n"
                "    simp\n"
                "  rw [h]\n"
                "  rfl\n\n"
                "theorem alg_rnk_01_m3_decide : rank3x4 6 3 = 2 ∧ rank3x4 7 3 = 3 := by decide\n\n"
                "#eval (List.range 8).map (fun i => let m := Int.ofNat (i + 2); (m, rank3x4 (2 * m) m, rank3x4 (2 * m + 1) m))\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "def verify_alg_rnk_01():\n"
                "    k, m = sp.symbols('k m')\n"
                "    for m_val in range(2, 10):\n"
                "        k_crit = 2 * m_val\n"
                "        A_sym_crit = sp.Matrix([\n"
                "            [1, 2, -1, m_val],\n"
                "            [2, 5, 1, 2 * m_val + 1],\n"
                "            [3, 7, k_crit - 2 * m_val, 3 * m_val + 1]\n"
                "        ])\n"
                "        A_sym_noncrit = sp.Matrix([\n"
                "            [1, 2, -1, m_val],\n"
                "            [2, 5, 1, 2 * m_val + 1],\n"
                "            [3, 7, (k_crit + 1) - 2 * m_val, 3 * m_val + 1]\n"
                "        ])\n"
                "        assert A_sym_crit.rank() == 2, f'SymPy rank failed at m={m_val}'\n"
                "        assert A_sym_noncrit.rank() == 3, f'SymPy noncrit rank failed at m={m_val}'\n"
                "        A_np_crit = np.array(A_sym_crit.tolist(), dtype=float)\n"
                "        A_np_noncrit = np.array(A_sym_noncrit.tolist(), dtype=float)\n"
                "        assert np.linalg.matrix_rank(A_np_crit) == 2\n"
                "        assert np.linalg.matrix_rank(A_np_noncrit) == 3\n"
                "    print('VERIFIED_OK: ALG-RNK-01 passed across m in [2..9]')\n\n"
                "if __name__ == '__main__':\n"
                "    verify_alg_rnk_01()\n"
            ),
        },
        {
            "code": "ALG-RNK-02",
            "agent_id": 12,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Hạng của ma trận phụ thuộc tham số",
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
                    "label": "Tham số nguyên m",
                }
            },
            "title": "Biện luận hạng của ma trận vuông cấp 3 qua định thức con và tổng bình phương nghiệm suy biến",
            "stem_symbolic": (
                r"Cho ma trận vuông $A(\lambda) \in M_{3\times 3}(\mathbb{R})$ phụ thuộc tham số thực $\lambda$ "
                r"(với hằng số nguyên $m \ge 2$):"
                "\n"
                r"$$A(\lambda) = \begin{pmatrix} 1 & 1 & 1 \\ 1 & \lambda & 1 \\ 1 & 1 & \lambda^2 - m\lambda + 1 \end{pmatrix}$$"
                "\n"
                r"Gọi $S$ là tập hợp tất cả các giá trị thực của $\lambda$ để $\operatorname{rank}(A(\lambda)) = 2$. "
                r"Tính tổng bình phương các phần tử của tập hợp $S$, tức là $P(m) = \sum_{\lambda \in S} \lambda^2$."
            ),
            "stem_template": (
                r"Cho ma trận vuông $A(\lambda) \in M_{3\times 3}(\mathbb{R})$ phụ thuộc tham số thực $\lambda$ "
                r"(với $m = {m}$):"
                "\n"
                r"$$A(\lambda) = \begin{pmatrix} 1 & 1 & 1 \\ 1 & \lambda & 1 \\ 1 & 1 & \lambda^2 - {m}\lambda + 1 \end{pmatrix}$$"
                "\n"
                r"Gọi $S$ là tập hợp tất cả các giá trị thực của $\lambda$ để $\operatorname{rank}(A(\lambda)) = 2$. "
                r"Tính tổng bình phương các phần tử của tập hợp $S$."
            ),
            "options_symbolic": {
                "A": r"$m^2$",
                "B": r"$m^2 + 1$",
                "C": r"$m^2 + m + 1$",
                "D": r"$m^2 + 2m + 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2",
                    "B": "m**2 + 1",
                    "C": "m**2 + m + 1",
                    "D": "m**2 + 2*m + 2",
                },
                "target_expr": "m**2 + 1",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"Thực hiện biến đổi sơ cấp theo hàng $R_2 \leftarrow R_2 - R_1$ và $R_3 \leftarrow R_3 - R_1$:" "\n"
                r"$$A(\lambda) \sim U(\lambda) = \begin{pmatrix} 1 & 1 & 1 \\ 0 & \lambda - 1 & 0 \\ 0 & 0 & \lambda(\lambda - m) \end{pmatrix}$$" "\n"
                r"- Định thức của ma trận là $\det(A(\lambda)) = (\lambda - 1)\lambda(\lambda - m)$." "\n"
                r"- Vì $m \ge 2$, phương trình $\det(A(\lambda)) = 0$ có đúng 3 nghiệm thực phân biệt: $\lambda_1 = 0, \lambda_2 = 1, \lambda_3 = m$." "\n"
                r"- Kiểm tra hạng tại từng nghiệm qua các phần tử đường chéo của $U(\lambda)$:" "\n"
                r"  + Với $\lambda = 0$: đường chéo là $(1, -1, 0) \implies \operatorname{rank}(A(0)) = 2$." "\n"
                r"  + Với $\lambda = 1$: đường chéo là $(1, 0, 1 - m)$ với $1 - m \ne 0 \implies \operatorname{rank}(A(1)) = 2$." "\n"
                r"  + Với $\lambda = m$: đường chéo là $(1, m - 1, 0)$ với $m - 1 \ne 0 \implies \operatorname{rank}(A(m)) = 2$." "\n"
                r"- Do đó $S = \{0, 1, m\}$ và tổng bình phương các phần tử của $S$ là $0^2 + 1^2 + m^2 = m^2 + 1$."
            ),
            "rubric_points": [
                {"step": "Biến đổi Gauss đưa A(lambda) về ma trận tam giác trên U(lambda)", "points": 0.4},
                {"step": "Giải det(A(lambda)) = 0 và kiểm chứng định thức con cấp 2 khác 0 tại 0, 1, m", "points": 0.4},
                {"step": "Tính tổng bình phương P(m) = 0^2 + 1^2 + m^2 = m^2 + 1", "points": 0.2},
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-RNK-02 (no Mathlib, no sorry)\n"
                "def detU (lam m : Int) : Int := (lam - 1) * lam * (lam - m)\n\n"
                "def rankU (lam m : Int) : Nat :=\n"
                "  let d2 := if lam - 1 == 0 then 0 else 1\n"
                "  let d3 := if lam * (lam - m) == 0 then 0 else 1\n"
                "  1 + d2 + d3\n\n"
                "def sumSqS (m : Int) : Int := 0 * 0 + 1 * 1 + m * m\n\n"
                "theorem alg_rnk_02_m3 : rankU 0 3 = 2 ∧ rankU 1 3 = 2 ∧ rankU 3 3 = 2 ∧ sumSqS 3 = 10 := by decide\n\n"
                "theorem alg_rnk_02_formula (m : Int) : sumSqS m = m * m + 1 := by\n"
                "  unfold sumSqS\n"
                "  omega\n\n"
                "#eval (List.range 8).map (fun i => let m := Int.ofNat (i + 2); (m, rankU 0 m, rankU 1 m, rankU m m, sumSqS m))\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "def verify_alg_rnk_02():\n"
                "    lam = sp.Symbol('lam')\n"
                "    for m_val in range(2, 10):\n"
                "        A_lam = sp.Matrix([\n"
                "            [1, 1, 1],\n"
                "            [1, lam, 1],\n"
                "            [1, 1, lam**2 - m_val * lam + 1]\n"
                "        ])\n"
                "        roots = sp.solve(sp.det(A_lam), lam)\n"
                "        rank2_vals = []\n"
                "        for r in roots:\n"
                "            A_sub = A_lam.subs(lam, r)\n"
                "            rk_sym = A_sub.rank()\n"
                "            rk_np = np.linalg.matrix_rank(np.array(A_sub.tolist(), dtype=float))\n"
                "            assert rk_sym == rk_np == 2, f'Mismatch at m={m_val}, r={r}'\n"
                "            rank2_vals.append(int(r))\n"
                "        assert sorted(rank2_vals) == [0, 1, m_val]\n"
                "        assert sum(x**2 for x in rank2_vals) == m_val**2 + 1\n"
                "    print('VERIFIED_OK: ALG-RNK-02 passed across m in [2..9]')\n\n"
                "if __name__ == '__main__':\n"
                "    verify_alg_rnk_02()\n"
            ),
        },
        {
            "code": "ALG-RNK-03",
            "agent_id": 12,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Hạng của ma trận phụ thuộc tham số",
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
                    "label": "Tham số nguyên m",
                }
            },
            "title": "Biện luận toàn diện hạng của ma trận 3x4 có phân tầng suy biến bậc 1, 2, 3",
            "stem_symbolic": (
                r"Cho ma trận thực $A(\lambda) \in M_{3\times 4}(\mathbb{R})$ phụ thuộc tham số thực $\lambda$ "
                r"(với hằng số nguyên $m \ge 2$):"
                "\n"
                r"$$A(\lambda) = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & \lambda - m + 1 & 1 & (\lambda - m)(\lambda - m - 1) + 1 \\ 1 & 1 & (\lambda - m)(\lambda - 2m) + 1 & (\lambda - m)(\lambda - 2m) + 1 \end{pmatrix}$$"
                "\n"
                r"a) Biện luận hạng $\operatorname{rank}(A(\lambda))$ theo mọi giá trị thực của $\lambda$." "\n"
                r"b) Gọi $\lambda_1$ là giá trị duy nhất của $\lambda$ để $\operatorname{rank}(A(\lambda)) = 1$ và $\lambda_2$ là giá trị duy nhất của $\lambda$ để $\operatorname{rank}(A(\lambda)) = 2$. "
                r"Tính giá trị biểu thức đặc trưng $T(m) = \lambda_1 + 2\lambda_2$."
            ),
            "stem_template": (
                r"Cho ma trận thực $A(\lambda) \in M_{3\times 4}(\mathbb{R})$ phụ thuộc tham số thực $\lambda$ "
                r"(với $m = {m}$):"
                "\n"
                r"$$A(\lambda) = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & \lambda - {m} + 1 & 1 & (\lambda - {m})(\lambda - {m} - 1) + 1 \\ 1 & 1 & (\lambda - {m})(\lambda - 2\cdot {m}) + 1 & (\lambda - {m})(\lambda - 2\cdot {m}) + 1 \end{pmatrix}$$"
                "\n"
                r"a) Biện luận hạng $\operatorname{rank}(A(\lambda))$ theo mọi giá trị thực của $\lambda$." "\n"
                r"b) Gọi $\lambda_1$ là giá trị duy nhất của $\lambda$ để $\operatorname{rank}(A(\lambda)) = 1$ và $\lambda_2$ là giá trị duy nhất của $\lambda$ để $\operatorname{rank}(A(\lambda)) = 2$. "
                r"Tính giá trị biểu thức đặc trưng $T = \lambda_1 + 2\lambda_2$."
            ),
            "options_symbolic": {
                "A": r"$T(m) = 3m$",
                "B": r"$T(m) = 4m + 1$",
                "C": r"$T(m) = 5m$",
                "D": r"$T(m) = 6m - 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "3*m",
                    "B": "4*m + 1",
                    "C": "5*m",
                    "D": "6*m - 1",
                },
                "target_expr": "5*m",
            },
            "correct_option": "C",
            "solution_symbolic": (
                r"**Lời giải tự luận chi tiết:**" "\n"
                r"1. **Đưa về dạng bậc thang bằng phép biến đổi sơ cấp Gauss:**" "\n"
                r"   Thực hiện $R_2 \leftarrow R_2 - R_1$ và $R_3 \leftarrow R_3 - R_1$, ta thu được ma trận bậc thang tương đương dòng:" "\n"
                r"   $$U(\lambda) = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 0 & \lambda - m & 0 & (\lambda - m)(\lambda - m - 1) \\ 0 & 0 & (\lambda - m)(\lambda - 2m) & (\lambda - m)(\lambda - 2m) \end{pmatrix}$$" "\n"
                r"2. **Biện luận theo tham số thực $\lambda$ (với $m \ge 2 \implies m \ne 2m$):**" "\n"
                r"   - **Trường hợp 1 ($\lambda = m$):** Cả hàng 2 và hàng 3 của $U(m)$ đều triệt tiêu thành $(0, 0, 0, 0)$, trong khi hàng 1 khác không. Do đó $\operatorname{rank}(A(m)) = 1$." "\n"
                r"   - **Trường hợp 2 ($\lambda = 2m$):** Khi đó $\lambda - m = m \ne 0$ nhưng $(\lambda - m)(\lambda - 2m) = 0$. Hàng 3 của $U(2m)$ bằng không, còn định thức con cấp 2 tạo bởi cột 1, 2 của hàng 1, 2 bằng $m \ne 0$. Do đó $\operatorname{rank}(A(2m)) = 2$." "\n"
                r"   - **Trường hợp 3 ($\lambda \notin \{m, 2m\}$):** Cả 3 phần tử chốt ở cột 1, 2, 3 là $1$, $\lambda - m \ne 0$, và $(\lambda - m)(\lambda - 2m) \ne 0$ đều khác không. Định thức con cấp 3 tạo bởi 3 cột đầu tiên bằng $(\lambda - m)^2(\lambda - 2m) \ne 0$. Do đó $\operatorname{rank}(A(\lambda)) = 3$." "\n"
                r"3. **Tính biểu thức đặc trưng:**" "\n"
                r"   Ta có $\lambda_1 = m$ và $\lambda_2 = 2m$, suy ra $T(m) = \lambda_1 + 2\lambda_2 = m + 2(2m) = 5m$."
            ),
            "rubric_points": [
                {"step": "Biến đổi sơ cấp hàng R2 <- R2 - R1 và R3 <- R3 - R1 thu được ma trận bậc thang U(lambda)", "points": 0.35},
                {"step": "Biện luận 3 trường hợp đầy đủ: lambda = m (rank 1), lambda = 2m (rank 2), và lambda != m, 2m (rank 3)", "points": 0.45},
                {"step": "Xác định đúng lambda_1 = m, lambda_2 = 2m và tính T(m) = 5m", "points": 0.20},
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-RNK-03 (no Mathlib, no sorry)\n"
                "def rankStratified (lam m : Int) : Nat :=\n"
                "  let r2_nonzero := (lam - m != 0)\n"
                "  let r3_nonzero := ((lam - m) * (lam - 2 * m) != 0)\n"
                "  1 + (if r2_nonzero then 1 else 0) + (if r3_nonzero then 1 else 0)\n\n"
                "def characteristicT (m : Int) : Int := m + 2 * (2 * m)\n\n"
                "theorem alg_rnk_03_m3 :\n"
                "    rankStratified 3 3 = 1 ∧ rankStratified 6 3 = 2 ∧ rankStratified 4 3 = 3 ∧ characteristicT 3 = 15 := by\n"
                "  decide\n\n"
                "theorem alg_rnk_03_target (m : Int) : characteristicT m = 5 * m := by\n"
                "  unfold characteristicT\n"
                "  omega\n\n"
                "#eval (List.range 8).map (fun i => let m := Int.ofNat (i + 2); (m, rankStratified m m, rankStratified (2 * m) m, rankStratified (m + 1) m, characteristicT m))\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "def verify_alg_rnk_03():\n"
                "    lam = sp.Symbol('lam')\n"
                "    for m_val in range(2, 10):\n"
                "        A_lam = sp.Matrix([\n"
                "            [1, 1, 1, 1],\n"
                "            [1, lam - m_val + 1, 1, (lam - m_val) * (lam - m_val - 1) + 1],\n"
                "            [1, 1, (lam - m_val) * (lam - 2 * m_val) + 1, (lam - m_val) * (lam - 2 * m_val) + 1]\n"
                "        ])\n"
                "        for test_lam, expected_rank in [(m_val, 1), (2 * m_val, 2), (m_val + 1, 3), (0, 3)]:\n"
                "            A_sub = A_lam.subs(lam, test_lam)\n"
                "            rk_sym = A_sub.rank()\n"
                "            rk_np = np.linalg.matrix_rank(np.array(A_sub.tolist(), dtype=float))\n"
                "            assert rk_sym == expected_rank, f'SymPy rank mismatch at m={m_val}, lam={test_lam}'\n"
                "            assert rk_np == expected_rank, f'NumPy rank mismatch at m={m_val}, lam={test_lam}'\n"
                "        lam1, lam2 = m_val, 2 * m_val\n"
                "        assert lam1 + 2 * lam2 == 5 * m_val\n"
                "    print('VERIFIED_OK: ALG-RNK-03 passed across m in [2..9]')\n\n"
                "if __name__ == '__main__':\n"
                "    verify_alg_rnk_03()\n"
            ),
        },
    ]
