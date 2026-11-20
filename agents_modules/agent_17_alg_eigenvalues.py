# -*- coding: utf-8 -*-
"""
Agent-17: Đại số — Đa thức đặc trưng, Trị riêng & Vector riêng phụ thuộc tham số.
Sinh và kiểm chứng tự động (SymPy + NumPy + Core Lean 4) các bài toán:
- ALG-EIG-01 (MCQ): Tổng bình phương các trị riêng qua vết và định thức của ma trận 2x2 tham số m.
- ALG-EIG-02 (MCQ): Đa thức đặc trưng, vết và định thức của ma trận tam giác khối 3x3 tham số m.
- ALG-EIG-03 (Essay): Phân tích toàn diện đa thức đặc trưng, trị riêng, vector riêng và chéo hóa ma trận đối xứng khối 3x3 theo tham số m.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 17,
    "agent_code": "AGENT-17",
    "agent_name": "Agent-17 (Đại số: Đa thức đặc trưng, Trị riêng & Vector riêng)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Đa thức đặc trưng P(lambda; m), Trị riêng, Vector riêng và Vết/Định thức theo tham số",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa của Agent-17."""
    return [
        # =====================================================================
        # ALG-EIG-01: MCQ — Tổng bình phương các trị riêng qua Vết & Định thức
        # =====================================================================
        {
            "code": "ALG-EIG-01",
            "agent_id": 17,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Đa thức đặc trưng, Trị riêng & Vector riêng phụ thuộc tham số",
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
                    "label": "Tham số m",
                    "description": "Tham số nguyên dương m trong ma trận A(m)",
                }
            },
            "title": "Tổng bình phương các trị riêng thông qua vết và định thức của ma trận bậc 2 theo tham số m",
            "stem_symbolic": (
                r"Cho ma trận thực phụ thuộc tham số nguyên dương $m$: "
                r"$$A(m) = \begin{pmatrix} 2m & m \\ m & 2m \end{pmatrix}.$$ "
                r"Gọi $\lambda_1, \lambda_2$ là hai trị riêng của $A(m)$ (kể cả bội đại số). "
                r"Hãy xác định đa thức đặc trưng $P(\lambda; m) = \det(A(m) - \lambda I_2)$ và tính biểu thức bất biến phổ "
                r"$S(m) = \lambda_1^2 + \lambda_2^2$ theo $m$."
            ),
            "stem_template": (
                r"Cho ma trận thực với tham số $m = {m}$: "
                r"$$A({m}) = \begin{pmatrix} 2\cdot {m} & {m} \\ {m} & 2\cdot {m} \end{pmatrix}.$$ "
                r"Gọi $\lambda_1, \lambda_2$ là hai trị riêng của ma trận $A({m})$. "
                r"Giá trị của biểu thức bất biến phổ $S({m}) = \lambda_1^2 + \lambda_2^2$ (tương ứng công thức tổng quát theo $m$) là:"
            ),
            "options_symbolic": {
                "A": r"$S(m) = 10m^2$ với $\lambda_1 = m,\; \lambda_2 = 3m$",
                "B": r"$S(m) = 16m^2$ với $\lambda_1 = 2m,\; \lambda_2 = 2m$",
                "C": r"$S(m) = 8m^2$ với $\lambda_1 = 2m,\; \lambda_2 = 2m$",
                "D": r"$S(m) = 13m^2$ với $\lambda_1 = 2m,\; \lambda_2 = 3m$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "10*m**2",
                    "B": "16*m**2",
                    "C": "8*m**2",
                    "D": "13*m**2",
                },
                "target_expr": "10*m**2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Bước 1 (Tính vết và định thức của $A(m)$):** "
                r"Ta có $\operatorname{Tr}(A(m)) = 2m + 2m = 4m$ và "
                r"$\det(A(m)) = (2m)(2m) - m\cdot m = 4m^2 - m^2 = 3m^2$. "
                "\n\n"
                r"**Bước 2 (Đa thức đặc trưng và trị riêng):** "
                r"$$P(\lambda; m) = \det(A(m) - \lambda I_2) = \lambda^2 - \operatorname{Tr}(A(m))\lambda + \det(A(m)) "
                r"= \lambda^2 - 4m\lambda + 3m^2 = (\lambda - m)(\lambda - 3m).$$ "
                r"Do đó hai trị riêng của $A(m)$ là $\lambda_1 = m$ và $\lambda_2 = 3m$. "
                "\n\n"
                r"**Bước 3 (Tính tổng bình phương các trị riêng):** "
                r"Theo định lý Viète hoặc tính trực tiếp: "
                r"$$S(m) = \lambda_1^2 + \lambda_2^2 = (\lambda_1 + \lambda_2)^2 - 2\lambda_1\lambda_2 "
                r"= (\operatorname{Tr}(A(m)))^2 - 2\det(A(m)) = (4m)^2 - 2(3m^2) = 16m^2 - 6m^2 = 10m^2.$$ "
                r"Khi $m = 3$, ta có $\lambda_1 = 3, \lambda_2 = 9$ và $S(3) = 3^2 + 9^2 = 90 = 10\cdot 3^2$. Chọn đáp án **A**."
            ),
            "rubric_points": [
                {"step": "Lập đúng đa thức đặc trưng P(lambda; m) = lambda^2 - 4m*lambda + 3m^2", "points": 0.4},
                {"step": "Tìm đúng hai trị riêng lambda_1 = m và lambda_2 = 3m", "points": 0.3},
                {"step": "Tính đúng S(m) = lambda_1^2 + lambda_2^2 = 10m^2 qua vết và định thức", "points": 0.3},
            ],
            "lean4_code": """-- Core Lean 4 verification for ALG-EIG-01 (No Mathlib, No sorry)
def traceA (m : Nat) : Nat := 4 * m
def detA (m : Nat) : Nat := 3 * m * m
def eig1 (m : Nat) : Nat := m
def eig2 (m : Nat) : Nat := 3 * m

def sumSqEigDirect (m : Nat) : Nat := eig1 m * eig1 m + eig2 m * eig2 m
def sumSqEigViete (m : Nat) : Nat := traceA m * traceA m - 2 * detA m
def targetFormula (m : Nat) : Nat := 10 * m * m

theorem alg_eig_01_m3_eq : sumSqEigDirect 3 = 90 := by rfl
theorem alg_eig_01_viete_m3 : sumSqEigViete 3 = targetFormula 3 := by decide

theorem alg_eig_01_grid_check :
    (List.range 8 |>.map (fun i => i + 2) |>.all (fun m =>
      sumSqEigDirect m == targetFormula m &&
      sumSqEigViete m == targetFormula m &&
      eig1 m + eig2 m == traceA m &&
      eig1 m * eig2 m == detA m)) = true := by decide

#eval (sumSqEigDirect 3, sumSqEigViete 3, targetFormula 3)
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
lam = sp.Symbol('lam')

A = sp.Matrix([[2*m, m], [m, 2*m]])
charpoly = sp.factor(A.charpoly(lam).as_expr())
eigs = A.eigenvals()
sum_sq_sym = sp.simplify(sum(val**2 * mult for val, mult in eigs.items()))
viete_sym = sp.simplify(A.trace()**2 - 2*A.det())

assert sp.simplify(sum_sq_sym - 10*m**2) == 0, f"Symbolic mismatch: {sum_sq_sym}"
assert sp.simplify(viete_sym - 10*m**2) == 0, f"Viete mismatch: {viete_sym}"

for m_val in range(2, 10):
    A_num = np.array([[2*m_val, m_val], [m_val, 2*m_val]], dtype=float)
    eig_num = np.linalg.eigvals(A_num)
    val_num = float(np.sum(eig_num**2))
    expected = float(10 * m_val**2)
    assert np.isclose(val_num, expected, rtol=1e-9), f"Numeric mismatch at m={m_val}: {val_num} != {expected}"

print(f"VERIFIED_OK: ALG-EIG-01 | charpoly={charpoly} | S(m)={sum_sq_sym} | S(3)={sum_sq_sym.subs(m, 3)}")
""",
        },
        # =====================================================================
        # ALG-EIG-02: MCQ — Đa thức đặc trưng, Vết & Định thức ma trận khối 3x3
        # =====================================================================
        {
            "code": "ALG-EIG-02",
            "agent_id": 17,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Đa thức đặc trưng, Trị riêng & Vector riêng phụ thuộc tham số",
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
                    "description": "Tham số nguyên dương m trong ma trận khối B(m)",
                }
            },
            "title": "Định thức và tổng-tích các trị riêng của ma trận tam giác khối 3x3 phụ thuộc tham số m",
            "stem_symbolic": (
                r"Cho ma trận thực cấp $3$ phụ thuộc tham số nguyên dương $m$: "
                r"$$B(m) = \begin{pmatrix} m+1 & 1 & 0 \\ 2 & m+2 & 0 \\ 0 & 0 & 2m \end{pmatrix}.$$ "
                r"Gọi $\lambda_1, \lambda_2, \lambda_3$ là ba trị riêng của ma trận $B(m)$. "
                r"Hãy tính giá trị của biểu thức bất biến $T(m) = \lambda_1\lambda_2\lambda_3 + (\lambda_1 + \lambda_2 + \lambda_3)$ theo $m$."
            ),
            "stem_template": (
                r"Cho ma trận thực cấp $3$ với tham số $m = {m}$: "
                r"$$B({m}) = \begin{pmatrix} {m}+1 & 1 & 0 \\ 2 & {m}+2 & 0 \\ 0 & 0 & 2\cdot {m} \end{pmatrix}.$$ "
                r"Gọi $\lambda_1, \lambda_2, \lambda_3$ là ba trị riêng của $B({m})$. "
                r"Biểu thức tổng-tích trị riêng $T(m) = \lambda_1\lambda_2\lambda_3 + (\lambda_1 + \lambda_2 + \lambda_3)$ bằng:"
            ),
            "options_symbolic": {
                "A": r"$T(m) = 2m^3 + 6m^2 + 2m + 3$",
                "B": r"$T(m) = 2m^3 + 6m^2 + 4m + 3$",
                "C": r"$T(m) = 2m^3 + 3m^2 + 4m + 3$",
                "D": r"$T(m) = 2m^3 + 6m^2 + 4m - 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m**3 + 6*m**2 + 2*m + 3",
                    "B": "2*m**3 + 6*m**2 + 4*m + 3",
                    "C": "2*m**3 + 3*m**2 + 4*m + 3",
                    "D": "2*m**3 + 6*m**2 + 4*m - 1",
                },
                "target_expr": "2*m**3 + 6*m**2 + 4*m + 3",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Bước 1 (Phân tích đa thức đặc trưng theo cấu trúc khối):** "
                r"Khối trên bên trái là $B_{11}(m) = \begin{pmatrix} m+1 & 1 \\ 2 & m+2 \end{pmatrix}$ có: "
                r"$$\det(B_{11}(m) - \lambda I_2) = (m+1-\lambda)(m+2-\lambda) - 2 = \lambda^2 - (2m+3)\lambda + m(m+3) = (\lambda - m)(\lambda - (m+3)).$$ "
                r"Do đó đa thức đặc trưng của $B(m)$ là: "
                r"$$P(\lambda; m) = (2m - \lambda)(\lambda - m)(\lambda - m - 3).$$ "
                r"Ba trị riêng của $B(m)$ là $\lambda_1 = m,\; \lambda_2 = m+3,\; \lambda_3 = 2m$. "
                "\n\n"
                r"**Bước 2 (Tính vết và định thức):** "
                r"- Tổng các trị riêng: $\lambda_1 + \lambda_2 + \lambda_3 = \operatorname{Tr}(B(m)) = (m+1) + (m+2) + 2m = 4m + 3$. "
                r"- Tích các trị riêng: $\lambda_1\lambda_2\lambda_3 = \det(B(m)) = m(m+3)(2m) = 2m^3 + 6m^2$. "
                "\n\n"
                r"**Bước 3 (Kết luận):** "
                r"$$T(m) = \det(B(m)) + \operatorname{Tr}(B(m)) = 2m^3 + 6m^2 + 4m + 3.$$ "
                r"Với $m = 3$, ta có $\lambda_1 = 3, \lambda_2 = 6, \lambda_3 = 6$ và $T(3) = 108 + 15 = 123$. Chọn đáp án **B**."
            ),
            "rubric_points": [
                {"step": "Khai triển đúng đa thức đặc trưng P(lambda; m) = (2m - lambda)(lambda - m)(lambda - m - 3)", "points": 0.4},
                {"step": "Tính đúng vết Tr(B(m)) = 4m + 3 và định thức det(B(m)) = 2m^3 + 6m^2", "points": 0.4},
                {"step": "Cộng hợp nhất được T(m) = 2m^3 + 6m^2 + 4m + 3", "points": 0.2},
            ],
            "lean4_code": """-- Core Lean 4 verification for ALG-EIG-02 (No Mathlib, No sorry)
def eigB1 (m : Nat) : Nat := m
def eigB2 (m : Nat) : Nat := m + 3
def eigB3 (m : Nat) : Nat := 2 * m

def traceB (m : Nat) : Nat := (m + 1) + (m + 2) + 2 * m
def detB (m : Nat) : Nat := 2 * m * m * m + 6 * m * m
def invT (m : Nat) : Nat := eigB1 m * eigB2 m * eigB3 m + (eigB1 m + eigB2 m + eigB3 m)
def formulaB (m : Nat) : Nat := 2 * m * m * m + 6 * m * m + 4 * m + 3

theorem alg_eig_02_m3 : invT 3 = 123 := by rfl
theorem alg_eig_02_formula_m3 : invT 3 = formulaB 3 := by decide

theorem alg_eig_02_grid_check :
    (List.range 8 |>.map (fun i => i + 2) |>.all (fun m =>
      invT m == formulaB m &&
      eigB1 m + eigB2 m + eigB3 m == traceB m &&
      eigB1 m * eigB2 m * eigB3 m == detB m)) = true := by decide

#eval (invT 3, formulaB 3, traceB 3, detB 3)
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
lam = sp.Symbol('lam')

B = sp.Matrix([
    [m + 1, 1, 0],
    [2, m + 2, 0],
    [0, 0, 2*m]
])
eigs_B = B.eigenvals()
sum_eigs = sp.simplify(sum(val * mult for val, mult in eigs_B.items()))
prod_eigs = sp.simplify(sp.prod([val**mult for val, mult in eigs_B.items()]))
T_sym = sp.expand(prod_eigs + sum_eigs)
target_sym = 2*m**3 + 6*m**2 + 4*m + 3

assert sp.simplify(T_sym - target_sym) == 0, f"Symbolic mismatch: {T_sym}"
assert sp.simplify(B.trace() - sum_eigs) == 0
assert sp.simplify(B.det() - prod_eigs) == 0

for m_val in range(2, 10):
    B_num = np.array([
        [m_val + 1, 1, 0],
        [2, m_val + 2, 0],
        [0, 0, 2*m_val]
    ], dtype=float)
    eig_num = np.linalg.eigvals(B_num)
    t_num = float(np.prod(eig_num) + np.sum(eig_num))
    expected = float(2*m_val**3 + 6*m_val**2 + 4*m_val + 3)
    assert np.isclose(t_num, expected, rtol=1e-9), f"Numeric mismatch at m={m_val}: {t_num} != {expected}"

print(f"VERIFIED_OK: ALG-EIG-02 | eigs={list(eigs_B.keys())} | T(m)={T_sym} | T(3)={T_sym.subs(m, 3)}")
""",
        },
        # =====================================================================
        # ALG-EIG-03: Essay — Đa thức đặc trưng, Vector riêng & Chéo hóa 3x3
        # =====================================================================
        {
            "code": "ALG-EIG-03",
            "agent_id": 17,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Đa thức đặc trưng, Trị riêng & Vector riêng phụ thuộc tham số",
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
                    "description": "Tham số nguyên m >= 2 đảm bảo 3 trị riêng phân biệt",
                }
            },
            "title": "Phân tích toàn diện Đa thức đặc trưng, Trị riêng, Cơ sở không gian riêng và Chéo hóa ma trận bậc 3 theo tham số m",
            "stem_symbolic": (
                r"Cho ma trận thực đối xứng khối cấp $3$ phụ thuộc tham số nguyên $m \ge 2$: "
                r"$$C(m) = \begin{pmatrix} m+2 & -1 & 0 \\ -1 & m+2 & 0 \\ 0 & 0 & 3m+1 \end{pmatrix}.$$ "
                r"a) Lập đa thức đặc trưng $P(\lambda; m) = \det(C(m) - \lambda I_3)$ và tìm tất cả các trị riêng $\lambda_1 < \lambda_2 < \lambda_3$ của $C(m)$ theo $m$. "
                r"b) Tìm các cơ sở trực giao của các không gian con riêng $E(\lambda_i)$ và viết ma trận làm chéo hóa $C(m)$. "
                r"c) Tính vết bình phương $\operatorname{Tr}(C(m)^2) = \lambda_1^2 + \lambda_2^2 + \lambda_3^2$ theo $m$."
            ),
            "stem_template": (
                r"Cho ma trận thực đối xứng khối cấp $3$ với tham số $m = {m}$: "
                r"$$C({m}) = \begin{pmatrix} {m}+2 & -1 & 0 \\ -1 & {m}+2 & 0 \\ 0 & 0 & 3\cdot {m}+1 \end{pmatrix}.$$ "
                r"a) Lập đa thức đặc trưng $P(\lambda; {m}) = \det(C({m}) - \lambda I_3)$ và tìm ba trị riêng $\lambda_1 < \lambda_2 < \lambda_3$. "
                r"b) Tìm cơ sở các không gian con riêng $E(\lambda_i)$ và chỉ ra ma trận khả nghịch $P$ sao cho $P^{-1} C({m}) P$ là ma trận đường chéo. "
                r"c) Tính tổng bình phương các trị riêng $\operatorname{Tr}(C({m})^2) = \lambda_1^2 + \lambda_2^2 + \lambda_3^2$."
            ),
            "options_symbolic": {
                "A": r"$\operatorname{Tr}(C(m)^2) = 11m^2 + 12m + 11$ với $\lambda \in \{m+1, m+3, 3m+1\}$",
                "B": r"$\operatorname{Tr}(C(m)^2) = 11m^2 + 14m + 9$ với $\lambda \in \{m+1, m+2, 3m+1\}$",
                "C": r"$\operatorname{Tr}(C(m)^2) = 11m^2 + 14m + 11$ với $\lambda \in \{m+1, m+3, 3m+1\}$",
                "D": r"$\operatorname{Tr}(C(m)^2) = 9m^2 + 14m + 11$ với $\lambda \in \{m-1, m+3, 3m+1\}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "11*m**2 + 12*m + 11",
                    "B": "11*m**2 + 14*m + 9",
                    "C": "11*m**2 + 14*m + 11",
                    "D": "9*m**2 + 14*m + 11",
                },
                "target_expr": "11*m**2 + 14*m + 11",
            },
            "correct_option": "C",
            "solution_symbolic": (
                r"**a) Đa thức đặc trưng và các trị riêng của $C(m)$:** "
                r"Khai triển định thức theo dòng 3 (hoặc cột 3): "
                r"$$P(\lambda; m) = \det(C(m) - \lambda I_3) = (3m + 1 - \lambda)\left[(m + 2 - \lambda)^2 - (-1)^2\right] "
                r"= (3m + 1 - \lambda)(\lambda - (m+1))(\lambda - (m+3)).$$ "
                r"Vì $m \ge 2 \implies 3m + 1 - (m+3) = 2m - 2 \ge 2 > 0$, nên $C(m)$ luôn có 3 trị riêng thực phân biệt: "
                r"$$\lambda_1 = m + 1 < \lambda_2 = m + 3 < \lambda_3 = 3m + 1.$$ "
                "\n\n"
                r"**b) Không gian con riêng và chéo hóa ma trận:** "
                r"- Với $\lambda_1 = m+1$: $(C(m) - \lambda_1 I_3)x = 0 \iff x_1 - x_2 = 0,\; x_3 = 0 \implies v_1 = (1, 1, 0)^T$. "
                r"- Với $\lambda_2 = m+3$: $(C(m) - \lambda_2 I_3)x = 0 \iff -x_1 - x_2 = 0,\; x_3 = 0 \implies v_2 = (1, -1, 0)^T$. "
                r"- Với $\lambda_3 = 3m+1$: $(C(m) - \lambda_3 I_3)x = 0 \iff x_1 = x_2 = 0 \implies v_3 = (0, 0, 1)^T$. "
                r"Ba vector riêng $v_1, v_2, v_3$ đôi một trực giao. Đặt $P = \begin{pmatrix} 1 & 1 & 0 \\ 1 & -1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$, "
                r"ta có $P^{-1} C(m) P = \operatorname{diag}(m+1, m+3, 3m+1)$. "
                "\n\n"
                r"**c) Tính bất biến phổ $\operatorname{Tr}(C(m)^2)$:** "
                r"$$\operatorname{Tr}(C(m)^2) = \lambda_1^2 + \lambda_2^2 + \lambda_3^2 = (m+1)^2 + (m+3)^2 + (3m+1)^2 "
                r"= (m^2 + 2m + 1) + (m^2 + 6m + 9) + (9m^2 + 6m + 1) = 11m^2 + 14m + 11.$$ "
                r"Khi $m = 3$, ta có $\lambda_1 = 4, \lambda_2 = 6, \lambda_3 = 10$ và $\operatorname{Tr}(C(3)^2) = 16 + 36 + 100 = 152$."
            ),
            "rubric_points": [
                {"step": "Lập đúng đa thức đặc trưng P(lambda; m) và tìm đúng 3 trị riêng m+1, m+3, 3m+1", "points": 0.4},
                {"step": "Tìm đúng 3 vector riêng cơ sở v1=(1,1,0)^T, v2=(1,-1,0)^T, v3=(0,0,1)^T và ma trận chéo hóa P", "points": 0.35},
                {"step": "Tính đúng Tr(C(m)^2) = 11m^2 + 14m + 11 và đối chiếu với vết của C(m)^2", "points": 0.25},
            ],
            "lean4_code": """-- Core Lean 4 verification for ALG-EIG-03 (No Mathlib, No sorry)
def eigC1 (m : Nat) : Nat := m + 1
def eigC2 (m : Nat) : Nat := m + 3
def eigC3 (m : Nat) : Nat := 3 * m + 1

def sumSqEigC (m : Nat) : Nat :=
  eigC1 m * eigC1 m + eigC2 m * eigC2 m + eigC3 m * eigC3 m

def formulaC (m : Nat) : Nat := 11 * m * m + 14 * m + 11

theorem alg_eig_03_m3 : sumSqEigC 3 = 152 := by rfl
theorem alg_eig_03_formula_m3 : sumSqEigC 3 = formulaC 3 := by decide
theorem alg_eig_03_strict_order_m3 : eigC1 3 < eigC2 3 ∧ eigC2 3 < eigC3 3 := by decide

theorem alg_eig_03_grid_check :
    (List.range 8 |>.map (fun i => i + 2) |>.all (fun m =>
      sumSqEigC m == formulaC m &&
      eigC1 m < eigC2 m &&
      eigC2 m < eigC3 m)) = true := by decide

#eval (eigC1 3, eigC2 3, eigC3 3, sumSqEigC 3, formulaC 3)
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
C = sp.Matrix([
    [m + 2, -1, 0],
    [-1, m + 2, 0],
    [0, 0, 3*m + 1]
])
eigs_C = C.eigenvals()
sum_sq_C = sp.expand(sum(val**2 * mult for val, mult in eigs_C.items()))
trace_C2 = sp.expand((C * C).trace())
target_C = 11*m**2 + 14*m + 11

assert sp.simplify(sum_sq_C - target_C) == 0, f"Symbolic mismatch: {sum_sq_C}"
assert sp.simplify(trace_C2 - target_C) == 0, f"Trace C^2 mismatch: {trace_C2}"

P = sp.Matrix([
    [1, 1, 0],
    [1, -1, 0],
    [0, 0, 1]
])
D = sp.simplify(P.inv() * C * P)
assert D == sp.diag(m + 1, m + 3, 3*m + 1), f"Diagonalization mismatch: {D}"

for m_val in range(2, 10):
    C_num = np.array([
        [m_val + 2, -1, 0],
        [-1, m_val + 2, 0],
        [0, 0, 3*m_val + 1]
    ], dtype=float)
    eig_num = np.linalg.eigvals(C_num)
    val_num = float(np.sum(eig_num**2))
    expected = float(11*m_val**2 + 14*m_val + 11)
    assert np.isclose(val_num, expected, rtol=1e-9), f"Numeric mismatch at m={m_val}: {val_num} != {expected}"

print(f"VERIFIED_OK: ALG-EIG-03 | eigs={list(eigs_C.keys())} | Tr(C^2)={sum_sq_C} | Tr(C(3)^2)={sum_sq_C.subs(m, 3)}")
""",
        },
    ]
