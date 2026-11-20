# -*- coding: utf-8 -*-
"""
Agent-11: Đại số — Ma trận, Định thức cấp n & Khả nghịch
Sinh và kiểm chứng câu hỏi Định thức ma trận chứa tham số, Ma trận phụ hợp, Ma trận nghịch đảo A^{-1}(m).
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 11,
    "agent_code": "AGENT-11",
    "agent_name": "Agent-11 (Đại số: Ma trận, Định thức cấp n & Khả nghịch)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Định thức ma trận chứa tham số, Ma trận phụ hợp, Ma trận nghịch đảo A^{-1}(m)",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa của Agent-11 (2 MCQ, 1 Essay)."""
    return [
        # =====================================================================
        # 1. ALG-DET-01 (MCQ): Định thức ma trận đối xứng tuần hoàn cấp 3 chứa m
        # =====================================================================
        {
            "code": "ALG-DET-01",
            "agent_id": 11,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Ma trận, Định thức & Ma trận nghịch đảo chứa tham số",
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
                    "label": "Tham số đường chéo m",
                }
            },
            "title": "Định thức ma trận đối xứng cấp 3 chứa tham số m trên đường chéo chính",
            "stem_symbolic": (
                r"Cho ma trận vuông cấp 3 phụ thuộc tham số thực $m$: "
                r"$$A(m) = \begin{pmatrix} m & 1 & 1 \\ 1 & m & 1 \\ 1 & 1 & m \end{pmatrix}$$ "
                r"Biểu thức thu gọn của định thức $\det(A(m))$ là:"
            ),
            "stem_template": (
                r"Cho ma trận vuông cấp 3 với giá trị tham số $m = {m}$: "
                r"$$A({m}) = \begin{pmatrix} {m} & 1 & 1 \\ 1 & {m} & 1 \\ 1 & 1 & {m} \end{pmatrix}$$ "
                r"Biểu thức định thức $\det(A(m))$ tổng quát và giá trị tại $m = {m}$ tương ứng với phương án nào sau đây?"
            ),
            "options_symbolic": {
                "A": r"$\det(A(m)) = (m - 1)^2(m + 2) = m^3 - 3m + 2$",
                "B": r"$\det(A(m)) = (m - 1)(m + 2)^2 = m^3 + 3m^2 - 4$",
                "C": r"$\det(A(m)) = (m + 1)^2(m - 2) = m^3 - 3m - 2$",
                "D": r"$\det(A(m)) = m^3 - 3m^2 + 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "(m - 1)**2 * (m + 2)",
                    "B": "(m - 1) * (m + 2)**2",
                    "C": "(m + 1)**2 * (m - 2)",
                    "D": "m**3 - 3*m**2 + 2",
                },
                "target_expr": "(m - 1)**2 * (m + 2)",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Thực hiện phép biến đổi sơ cấp cột $C_1 \leftarrow C_1 + C_2 + C_3$, ta đưa nhân tử chung $(m + 2)$ ra ngoài:" "\n"
                r"$$\det(A(m)) = \det\begin{pmatrix} m+2 & 1 & 1 \\ m+2 & m & 1 \\ m+2 & 1 & m \end{pmatrix} "
                r"= (m + 2) \det\begin{pmatrix} 1 & 1 & 1 \\ 1 & m & 1 \\ 1 & 1 & m \end{pmatrix}$$" "\n"
                r"Tiếp tục thực hiện $R_2 \leftarrow R_2 - R_1$ và $R_3 \leftarrow R_3 - R_1$ để đưa về ma trận tam giác trên:" "\n"
                r"$$\det(A(m)) = (m + 2) \det\begin{pmatrix} 1 & 1 & 1 \\ 0 & m - 1 & 0 \\ 0 & 0 & m - 1 \end{pmatrix} "
                r"= (m - 1)^2(m + 2) = m^3 - 3m + 2.$$" "\n"
                r"Đặc biệt, với $m = 3$, ta có $\det(A(3)) = (3 - 1)^2(3 + 2) = 20$. Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Cộng cột 2 và cột 3 vào cột 1 để đặt nhân tử chung (m + 2): 0.5 điểm",
                "Khử hàng 2 và hàng 3 theo hàng 1 đưa về định thức tam giác trên: 0.25 điểm",
                "Kết luận đúng det(A(m)) = (m - 1)^2 (m + 2) = m^3 - 3m + 2: 0.25 điểm",
            ],
            "lean4_code": """-- Lean 4 Core verification for ALG-DET-01 (No Mathlib, No sorry)
def detA1 (m : Int) : Int :=
  m * (m * m - 1 * 1) - 1 * (1 * m - 1 * 1) + 1 * (1 * 1 - m * 1)

def closedForm1 (m : Int) : Int :=
  (m - 1) * (m - 1) * (m + 2)

theorem detA1_eq_closed_m3 : detA1 3 = closedForm1 3 := by rfl

theorem detA1_grid_verified :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      detA1 m == closedForm1 m) = true := by decide

theorem detA1_positive_m3 : detA1 3 = 20 := by decide

#eval (List.range 8).map (fun k =>
  let m : Int := Int.ofNat (k + 2)
  (m, detA1 m, closedForm1 m))
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
A_sym = sp.Matrix([
    [m, 1, 1],
    [1, m, 1],
    [1, 1, m],
])
det_sym = sp.factor(A_sym.det())
expected_sym = (m - 1)**2 * (m + 2)
assert sp.simplify(det_sym - expected_sym) == 0, f"Symbolic mismatch: {det_sym}"

for m_val in range(2, 10):
    A_np = np.array([
        [m_val, 1.0, 1.0],
        [1.0, m_val, 1.0],
        [1.0, 1.0, m_val],
    ], dtype=float)
    det_num = round(float(np.linalg.det(A_np)))
    det_exact = (m_val - 1)**2 * (m_val + 2)
    assert det_num == det_exact, f"Numeric mismatch at m={m_val}: {det_num} != {det_exact}"

print(f"VERIFIED_OK: ALG-DET-01 det(A(m)) = {det_sym}, grid m in [2..9] passed, det(A(3)) = {(3-1)**2*(3+2)}")
""",
        },
        # =====================================================================
        # 2. ALG-DET-02 (MCQ): Định thức & Vết ma trận phụ hợp adj(A(m))
        # =====================================================================
        {
            "code": "ALG-DET-02",
            "agent_id": 11,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Ma trận, Định thức & Ma trận nghịch đảo chứa tham số",
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
            "title": "Tổng định thức và vết của ma trận phụ hợp đối với ma trận tam đường chéo chứa tham số m",
            "stem_symbolic": (
                r"Cho ma trận tam đường chéo cấp 3 chứa tham số nguyên $m \ge 2$: "
                r"$$A(m) = \begin{pmatrix} m & 1 & 0 \\ 1 & m & 1 \\ 0 & 1 & m \end{pmatrix}$$ "
                r"Gọi $\mathrm{adj}(A(m))$ là ma trận phụ hợp của $A(m)$ và $\mathrm{Tr}(\mathrm{adj}(A(m)))$ là vết (tổng các phần tử trên đường chéo chính) của $\mathrm{adj}(A(m))$. "
                r"Biểu thức $S(m) = \det(A(m)) + \mathrm{Tr}(\mathrm{adj}(A(m)))$ bằng:"
            ),
            "stem_template": (
                r"Cho ma trận tam đường chéo cấp 3 với tham số $m = {m}$: "
                r"$$A({m}) = \begin{pmatrix} {m} & 1 & 0 \\ 1 & {m} & 1 \\ 0 & 1 & {m} \end{pmatrix}$$ "
                r"Gọi $\mathrm{adj}(A(m))$ là ma trận phụ hợp của $A(m)$. "
                r"Biểu thức $S(m) = \det(A(m)) + \mathrm{Tr}(\mathrm{adj}(A(m)))$ và giá trị tại $m = {m}$ là:"
            ),
            "options_symbolic": {
                "A": r"$S(m) = m^3 + 3m^2 - 2m - 2$",
                "B": r"$S(m) = m^3 + 3m^2 - m - 1$",
                "C": r"$S(m) = m^3 + 2m^2 - 2m$",
                "D": r"$S(m) = m^3 - 3m^2 + 2m - 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**3 + 3*m**2 - 2*m - 2",
                    "B": "m**3 + 3*m**2 - m - 1",
                    "C": "m**3 + 2*m**2 - 2*m",
                    "D": "m**3 - 3*m**2 + 2*m - 2",
                },
                "target_expr": "m**3 + 3*m**2 - 2*m - 2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"1. **Tính định thức $\det(A(m))$:** Khai triển theo hàng 1:" "\n"
                r"$$\det(A(m)) = m(m^2 - 1) - 1(m - 0) = m^3 - 2m.$$" "\n"
                r"2. **Tính vết của ma trận phụ hợp $\mathrm{Tr}(\mathrm{adj}(A(m)))$:** "
                r"Các phần tử trên đường chéo chính của $\mathrm{adj}(A(m))$ chính là các phần bù đại số $C_{11}, C_{22}, C_{33}$:" "\n"
                r"$$C_{11} = \det\begin{pmatrix} m & 1 \\ 1 & m \end{pmatrix} = m^2 - 1, \quad "
                r"C_{22} = \det\begin{pmatrix} m & 0 \\ 0 & m \end{pmatrix} = m^2, \quad "
                r"C_{33} = \det\begin{pmatrix} m & 1 \\ 1 & m \end{pmatrix} = m^2 - 1.$$" "\n"
                r"Do đó $\mathrm{Tr}(\mathrm{adj}(A(m))) = C_{11} + C_{22} + C_{33} = 3m^2 - 2$." "\n\n"
                r"3. **Tổng $S(m)$:** "
                r"$$S(m) = \det(A(m)) + \mathrm{Tr}(\mathrm{adj}(A(m))) = m^3 + 3m^2 - 2m - 2.$$" "\n"
                r"Tại $m = 3$, ta có $S(3) = 27 + 27 - 6 - 2 = 46$. Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Tính đúng định thức det(A(m)) = m^3 - 2m: 0.4 điểm",
                "Xác định đúng 3 phần bù đại số chéo C_11 = m^2 - 1, C_22 = m^2, C_33 = m^2 - 1: 0.4 điểm",
                "Cộng đúng S(m) = m^3 + 3m^2 - 2m - 2: 0.2 điểm",
            ],
            "lean4_code": """-- Lean 4 Core verification for ALG-DET-02 (No Mathlib, No sorry)
def detA2 (m : Int) : Int :=
  m * (m * m - 1 * 1) - 1 * (1 * m - 1 * 0) + 0 * (1 * 1 - m * 0)

def traceAdjA2 (m : Int) : Int :=
  let c11 := m * m - 1
  let c22 := m * m
  let c33 := m * m - 1
  c11 + c22 + c33

def totalS2 (m : Int) : Int :=
  m * m * m + 3 * m * m - 2 * m - 2

theorem alg_det_02_m3 : detA2 3 + traceAdjA2 3 = 46 := by decide

theorem alg_det_02_grid_verified :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      (detA2 m + traceAdjA2 m) == totalS2 m) = true := by decide

#eval (List.range 8).map (fun k =>
  let m : Int := Int.ofNat (k + 2)
  (m, detA2 m, traceAdjA2 m, totalS2 m))
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
A_sym = sp.Matrix([
    [m, 1, 0],
    [1, m, 1],
    [0, 1, m],
])
det_sym = sp.expand(A_sym.det())
adj_sym = A_sym.adjugate()
trace_adj_sym = sp.expand(adj_sym.trace())
S_sym = sp.expand(det_sym + trace_adj_sym)
expected_S = m**3 + 3*m**2 - 2*m - 2
assert sp.simplify(S_sym - expected_S) == 0, f"Symbolic mismatch: {S_sym}"

for m_val in range(2, 10):
    A_np = np.array([
        [m_val, 1.0, 0.0],
        [1.0, m_val, 1.0],
        [0.0, 1.0, m_val],
    ], dtype=float)
    det_val = float(np.linalg.det(A_np))
    inv_np = np.linalg.inv(A_np)
    adj_np = det_val * inv_np
    s_num = round(det_val + float(np.trace(adj_np)))
    s_exact = m_val**3 + 3 * m_val**2 - 2 * m_val - 2
    assert s_num == s_exact, f"Numeric mismatch at m={m_val}: {s_num} != {s_exact}"

print(f"VERIFIED_OK: ALG-DET-02 S(m) = {S_sym}, grid m in [2..9] passed, S(3) = {int(expected_S.subs(m, 3))}")
""",
        },
        # =====================================================================
        # 3. ALG-DET-03 (Essay): Khả nghịch, Ma trận phụ hợp & Nghịch đảo A^{-1}(m)
        # =====================================================================
        {
            "code": "ALG-DET-03",
            "agent_id": 11,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Ma trận, Định thức & Ma trận nghịch đảo chứa tham số",
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
            "title": "Biện luận khả nghịch, tìm ma trận phụ hợp và ma trận nghịch đảo A^{-1}(m)",
            "stem_symbolic": (
                r"Cho ma trận vuông cấp 3 phụ thuộc tham số thực $m$: "
                r"$$A(m) = \begin{pmatrix} 1 & 1 & 1 \\ 1 & m & 1 \\ 1 & 1 & m^2 \end{pmatrix}$$ "
                r"a) Tính định thức $\det(A(m))$ dưới dạng phân tích nhân tử và tìm điều kiện của tham số $m$ để $A(m)$ khả nghịch." "\n"
                r"b) Khi $A(m)$ khả nghịch, tìm tường minh ma trận phụ hợp $\mathrm{adj}(A(m))$ và ma trận nghịch đảo $A^{-1}(m)$ theo $m$." "\n"
                r"c) Chứng minh rằng tổng tất cả 9 phần tử của ma trận phụ hợp $\mathrm{adj}(A(m))$ luôn bằng $\det(A(m))$, "
                r"suy ra tổng tất cả các phần tử của $A^{-1}(m)$ là một hằng số không phụ thuộc vào $m$."
            ),
            "stem_template": (
                r"Cho ma trận vuông cấp 3 phụ thuộc tham số $m$ (xét trường hợp cụ thể tại $m = {m}$): "
                r"$$A(m) = \begin{pmatrix} 1 & 1 & 1 \\ 1 & m & 1 \\ 1 & 1 & m^2 \end{pmatrix}, \quad "
                r"A({m}) = \begin{pmatrix} 1 & 1 & 1 \\ 1 & {m} & 1 \\ 1 & 1 & {m}^2 \end{pmatrix}$$ "
                r"a) Tính $\det(A(m))$, biện luận điều kiện khả nghịch của $A(m)$ và tính $\det(A({m}))$." "\n"
                r"b) Tìm ma trận phụ hợp $\mathrm{adj}(A(m))$, ma trận nghịch đảo $A^{-1}(m)$ và áp dụng cho $m = {m}$." "\n"
                r"c) Tính tổng tất cả 9 phần tử của $\mathrm{adj}(A({m}))$ và tổng các phần tử của $A^{-1}({m})$."
            ),
            "options_symbolic": {
                "A": r"$\det(A(m)) = (m - 1)^2(m + 1)$",
                "B": r"$\det(A(m)) = (m - 1)(m + 1)^2$",
                "C": r"$\det(A(m)) = m(m - 1)(m + 1)$",
                "D": r"$\det(A(m)) = (m - 1)^3$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "(m - 1)**2 * (m + 1)",
                    "B": "(m - 1) * (m + 1)**2",
                    "C": "m * (m - 1) * (m + 1)",
                    "D": "(m - 1)**3",
                },
                "target_expr": "(m - 1)**2 * (m + 1)",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"**a) Tính $\det(A(m))$ và điều kiện khả nghịch:**" "\n"
                r"Thực hiện biến đổi sơ cấp hàng $R_2 \leftarrow R_2 - R_1$ và $R_3 \leftarrow R_3 - R_1$:" "\n"
                r"$$\det(A(m)) = \det\begin{pmatrix} 1 & 1 & 1 \\ 0 & m - 1 & 0 \\ 0 & 0 & m^2 - 1 \end{pmatrix} "
                r"= (m - 1)(m^2 - 1) = (m - 1)^2(m + 1) = m^3 - m^2 - m + 1.$$" "\n"
                r"Ma trận $A(m)$ khả nghịch khi và chỉ khi $\det(A(m)) \ne 0 \iff m \notin \{-1, 1\}$." "\n\n"
                r"**b) Tìm ma trận phụ hợp $\mathrm{adj}(A(m))$ và ma trận nghịch đảo $A^{-1}(m)$:**" "\n"
                r"Tính các phần bù đại số $C_{ij}$ của $A(m)$ (do $A(m)$ đối xứng nên $C_{ij} = C_{ji}$):" "\n"
                r"- $C_{11} = m^3 - 1$, $C_{12} = 1 - m^2$, $C_{13} = 1 - m$." "\n"
                r"- $C_{21} = 1 - m^2$, $C_{22} = m^2 - 1$, $C_{23} = 0$." "\n"
                r"- $C_{31} = 1 - m$, $C_{32} = 0$, $C_{33} = m - 1$." "\n"
                r"Do đó:" "\n"
                r"$$\mathrm{adj}(A(m)) = \begin{pmatrix} m^3 - 1 & 1 - m^2 & 1 - m \\ 1 - m^2 & m^2 - 1 & 0 \\ 1 - m & 0 & m - 1 \end{pmatrix}, "
                r"\quad A^{-1}(m) = \frac{1}{(m - 1)^2(m + 1)} \mathrm{adj}(A(m)) "
                r"= \begin{pmatrix} \frac{m^2+m+1}{m^2-1} & -\frac{1}{m-1} & -\frac{1}{m^2-1} \\ -\frac{1}{m-1} & \frac{1}{m-1} & 0 \\ -\frac{1}{m^2-1} & 0 & \frac{1}{m^2-1} \end{pmatrix}.$$" "\n\n"
                r"**c) Tổng các phần tử của $\mathrm{adj}(A(m))$ và $A^{-1}(m)$:**" "\n"
                r"Cộng tất cả 9 phần tử của $\mathrm{adj}(A(m))$:" "\n"
                r"$$\sum_{i,j=1}^{3} (\mathrm{adj}(A(m)))_{ij} = (m^3 - 1) + 2(1 - m^2) + (m^2 - 1) + 2(1 - m) + (m - 1) "
                r"= m^3 - m^2 - m + 1 = (m - 1)^2(m + 1) = \det(A(m)).$$" "\n"
                r"Suy ra với mọi $m \notin \{-1, 1\}$, tổng tất cả các phần tử của $A^{-1}(m)$ luôn bằng $\frac{\det(A(m))}{\det(A(m))} = 1$."
            ),
            "rubric_points": [
                "Phần a: Biến đổi hàng đưa về tam giác trên, tính đúng det(A(m)) = (m - 1)^2 (m + 1) và kết luận m != +-1: 1.0 điểm",
                "Phần b: Tính đúng ma trận phụ hợp adj(A(m)) và rút gọn A^{-1}(m): 1.25 điểm",
                "Phần c: Chứng minh tổng 9 phần tử của adj(A(m)) bằng det(A(m)) và tổng các phần tử của A^{-1}(m) bằng 1: 0.75 điểm",
            ],
            "lean4_code": """-- Lean 4 Core verification for ALG-DET-03 (No Mathlib, No sorry)
def detA3 (m : Int) : Int :=
  1 * (m * (m * m) - 1 * 1) - 1 * (1 * (m * m) - 1 * 1) + 1 * (1 * 1 - m * 1)

def sumAdjA3 (m : Int) : Int :=
  let c11 := m * m * m - 1
  let c12 := 1 - m * m
  let c13 := 1 - m
  let c21 := 1 - m * m
  let c22 := m * m - 1
  let c23 := 0
  let c31 := 1 - m
  let c32 := 0
  let c33 := m - 1
  c11 + c12 + c13 + c21 + c22 + c23 + c31 + c32 + c33

def factoredDet3 (m : Int) : Int :=
  (m - 1) * (m - 1) * (m + 1)

theorem alg_det_03_m3 : detA3 3 = 16 ∧ sumAdjA3 3 = 16 := by decide

theorem alg_det_03_grid_verified :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      (detA3 m == factoredDet3 m) && (sumAdjA3 m == detA3 m)) = true := by decide

#eval (List.range 8).map (fun k =>
  let m : Int := Int.ofNat (k + 2)
  (m, detA3 m, sumAdjA3 m, factoredDet3 m))
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
A_sym = sp.Matrix([
    [1, 1, 1],
    [1, m, 1],
    [1, 1, m**2],
])
det_sym = sp.factor(A_sym.det())
expected_det = (m - 1)**2 * (m + 1)
assert sp.simplify(det_sym - expected_det) == 0, f"Det mismatch: {det_sym}"

adj_sym = A_sym.adjugate()
assert sp.simplify(A_sym * adj_sym - A_sym.det() * sp.eye(3)) == sp.zeros(3, 3)
sum_adj_sym = sp.factor(sum(adj_sym))
assert sp.simplify(sum_adj_sym - expected_det) == 0, f"Adjugate sum mismatch: {sum_adj_sym}"

for m_val in range(2, 10):
    A_np = np.array([
        [1.0, 1.0, 1.0],
        [1.0, float(m_val), 1.0],
        [1.0, 1.0, float(m_val**2)],
    ], dtype=float)
    det_num = round(float(np.linalg.det(A_np)))
    det_exact = (m_val - 1)**2 * (m_val + 1)
    assert det_num == det_exact, f"Numeric det mismatch at m={m_val}: {det_num} != {det_exact}"
    inv_np = np.linalg.inv(A_np)
    assert abs(float(np.sum(inv_np)) - 1.0) < 1e-9, f"Inverse sum mismatch at m={m_val}"

print(f"VERIFIED_OK: ALG-DET-03 det(A(m)) = {det_sym}, sum(adj(A(m))) = {sum_adj_sym}, sum(A^-1(m)) = 1 for m in [2..9]")
""",
        },
    ]
