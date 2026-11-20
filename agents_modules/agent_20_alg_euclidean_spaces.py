# -*- coding: utf-8 -*-
"""
Agent-20: Đại số — Không gian Euclid, Trực giao hóa Gram-Schmidt & Hình chiếu trực giao
Sinh và kiểm chứng câu hỏi có tham số m (Symbolic, Lean 4 Core, SymPy/NumPy Verification).
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 20,
    "agent_code": "AGENT-20",
    "agent_name": "Agent-20 (Đại số: Không gian Euclid, Gram-Schmidt & Hình chiếu)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Tích vô hướng có tham số, Trực giao hóa Gram-Schmidt, Khoảng cách & Hình chiếu trực giao",
}


def get_questions() -> list[dict]:
    return [
        {
            "code": "ALG-EUC-01",
            "agent_id": 20,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian Euclid, Trực giao hóa Gram-Schmidt & Hình chiếu trực giao",
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
            "title": "Tích vô hướng phi chính tắc có tham số trên R^3 và bình phương chuẩn vectơ",
            "stem_symbolic": (
                r"Trong không gian thực $\mathbb{R}^3$, với tham số nguyên dương $m \ge 2$, xét ánh xạ song tuyến tính "
                r"$\langle u, v \rangle_m = x_1 y_1 + 2 x_2 y_2 + (m^2 + 1) x_3 y_3 + x_1 y_2 + x_2 y_1$ "
                r"với $u = (x_1, x_2, x_3)$ và $v = (y_1, y_2, y_3)$. "
                r"Biết rằng $\langle \cdot, \cdot \rangle_m$ xác định một tích vô hướng trên $\mathbb{R}^3$. "
                r"Hãy tính bình phương độ dài $\|w\|_m^2 = \langle w, w \rangle_m$ của vectơ $w = (1, 1, 1)$ theo $m$."
            ),
            "stem_template": (
                r"Trong không gian thực $\mathbb{R}^3$, với $m = {m}$, xét tích vô hướng xác định bởi "
                r"$\langle u, v \rangle_{{{m}}} = x_1 y_1 + 2 x_2 y_2 + ({m}^2 + 1) x_3 y_3 + x_1 y_2 + x_2 y_1$ "
                r"với $u = (x_1, x_2, x_3)$ và $v = (y_1, y_2, y_3)$. "
                r"Hãy tính bình phương độ dài $\|w\|_{{{m}}}^2 = \langle w, w \rangle_{{{m}}}$ của vectơ $w = (1, 1, 1)$."
            ),
            "options_symbolic": {
                "A": r"$m^2 + 6$",
                "B": r"$m^2 + 4$",
                "C": r"$m^2 + 5$",
                "D": r"$2m^2 + 6$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2 + 6",
                    "B": "m**2 + 4",
                    "C": "m**2 + 5",
                    "D": "2*m**2 + 6",
                },
                "target_expr": "m**2 + 6",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Bước 1: Kiểm chứng điều kiện xác định dương của tích vô hướng.**" "\n"
                r"Với mọi $u = (x_1, x_2, x_3) \in \mathbb{R}^3$, ta có:" "\n"
                r"$$\langle u, u \rangle_m = x_1^2 + 2x_1 x_2 + 2x_2^2 + (m^2 + 1)x_3^2 = (x_1 + x_2)^2 + x_2^2 + (m^2 + 1)x_3^2 \ge 0.$$" "\n"
                r"Vì $m^2 + 1 > 0$, đẳng thức $\langle u, u \rangle_m = 0$ xảy ra khi và chỉ khi $x_1 = x_2 = x_3 = 0$. Do đó $\langle \cdot, \cdot \rangle_m$ là tích vô hướng trên $\mathbb{R}^3$." "\n\n"
                r"**Bước 2: Tính bình phương chuẩn $\|w\|_m^2$ với $w = (1, 1, 1)$.**" "\n"
                r"Thay $x_1 = x_2 = x_3 = 1$ và $y_1 = y_2 = y_3 = 1$ vào công thức tích vô hướng:" "\n"
                r"$$\|w\|_m^2 = \langle w, w \rangle_m = 1\cdot 1 + 2\cdot 1\cdot 1 + (m^2 + 1)\cdot 1\cdot 1 + 1\cdot 1 + 1\cdot 1 = m^2 + 6.$$" "\n"
                r"Vậy đáp án đúng là **A** ($m^2 + 6$)."
            ),
            "rubric_points": [
                {"step": "Biểu diễn dạng toàn phương tương ứng theo tổng các bình phương để xác nhận tính xác định dương", "points": 0.5},
                {"step": "Thay tọa độ w = (1, 1, 1) vào biểu thức tích vô hướng và rút gọn ra m^2 + 6", "points": 0.5},
            ],
            "lean4_code": """-- Lean 4 Core verification for ALG-EUC-01 (No Mathlib, No sorry)
def inner_m (m : Int) (x1 x2 x3 y1 y2 y3 : Int) : Int :=
  x1 * y1 + 2 * x2 * y2 + (m * m + 1) * x3 * y3 + x1 * y2 + x2 * y1

def norm_sq_w (m : Int) : Int :=
  inner_m m 1 1 1 1 1 1

theorem alg_euc_01_m3 : norm_sq_w 3 = 3 * 3 + 6 := by decide
theorem alg_euc_01_m5 : norm_sq_w 5 = 5 * 5 + 6 := by decide
theorem alg_euc_01_pos_def_decomp :
    (List.range 10).all (fun k => let m := Int.ofNat (k + 2); inner_m m 1 2 3 1 2 3 == (1 + 2) * (1 + 2) + 2 * 2 + (m * m + 1) * 3 * 3) = true := by
  decide

#eval norm_sq_w 3
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
G = sp.Matrix([
    [1, 1, 0],
    [1, 2, 0],
    [0, 0, m**2 + 1]
])
w = sp.Matrix([1, 1, 1])
norm_sq = sp.simplify((w.T * G * w)[0])
assert sp.simplify(norm_sq - (m**2 + 6)) == 0, f"Mismatch symbolic: {norm_sq}"

for m_val in range(2, 10):
    G_num = np.array([[1.0, 1.0, 0.0], [1.0, 2.0, 0.0], [0.0, 0.0, float(m_val**2 + 1)]])
    eigvals = np.linalg.eigvalsh(G_num)
    assert np.all(eigvals > 0), "Gram matrix must be positive definite"
    w_num = np.array([1.0, 1.0, 1.0])
    val_num = float(w_num @ G_num @ w_num)
    assert abs(val_num - (m_val**2 + 6)) < 1e-9

print(f"VERIFIED_OK: ALG-EUC-01 norm_sq={norm_sq}")
""",
        },
        {
            "code": "ALG-EUC-02",
            "agent_id": 20,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian Euclid, Trực giao hóa Gram-Schmidt & Hình chiếu trực giao",
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
                    "label": "Tham số nguyên dương m",
                }
            },
            "title": "Trực giao hóa Gram-Schmidt hệ vectơ phụ thuộc tham số trong R^3",
            "stem_symbolic": (
                r"Trong không gian Euclid $\mathbb{R}^3$ với tích vô hướng chính tắc, cho hệ hai vectơ độc lập tuyến tính "
                r"$u_1 = (1, 1, 0)$ và $u_2 = (2m, 0, m)$ với $m \ge 2$ là tham số nguyên dương. "
                r"Thực hiện quá trình trực giao hóa Gram-Schmidt cho hệ $\{u_1, u_2\}$ với $e_1 = u_1$ và "
                r"$e_2 = u_2 - \dfrac{\langle u_2, e_1 \rangle}{\|e_1\|^2} e_1$. "
                r"Hãy tính bình phương độ dài $\|e_2\|^2$ theo tham số $m$."
            ),
            "stem_template": (
                r"Trong không gian Euclid $\mathbb{R}^3$ với tích vô hướng chính tắc, cho hệ hai vectơ độc lập tuyến tính "
                r"$u_1 = (1, 1, 0)$ và $u_2 = (2\cdot {m}, 0, {m})$ (với $m = {m}$). "
                r"Thực hiện quá trình trực giao hóa Gram-Schmidt với $e_1 = u_1$ và "
                r"$e_2 = u_2 - \dfrac{\langle u_2, e_1 \rangle}{\|e_1\|^2} e_1$. "
                r"Hãy tính bình phương độ dài $\|e_2\|^2$."
            ),
            "options_symbolic": {
                "A": r"$2m^2$",
                "B": r"$3m^2$",
                "C": r"$4m^2$",
                "D": r"$5m^2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m**2",
                    "B": "3*m**2",
                    "C": "4*m**2",
                    "D": "5*m**2",
                },
                "target_expr": "3*m**2",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Bước 1: Xác định $e_1$ và hệ số chiếu Gram-Schmidt.**" "\n"
                r"Đặt $e_1 = u_1 = (1, 1, 0)$, suy ra $\|e_1\|^2 = 1^2 + 1^2 + 0^2 = 2$." "\n"
                r"Tích vô hướng chính tắc giữa $u_2 = (2m, 0, m)$ và $e_1 = (1, 1, 0)$ là:" "\n"
                r"$$\langle u_2, e_1 \rangle = 2m \cdot 1 + 0 \cdot 1 + m \cdot 0 = 2m.$$" "\n"
                r"Hệ số chiếu là $\alpha = \dfrac{\langle u_2, e_1 \rangle}{\|e_1\|^2} = \dfrac{2m}{2} = m$." "\n\n"
                r"**Bước 2: Tìm vectơ trực giao $e_2$ và tính $\|e_2\|^2$.**" "\n"
                r"$$e_2 = u_2 - m e_1 = (2m, 0, m) - (m, m, 0) = (m, -m, m).$$" "\n"
                r"Kiểm tra tính trực giao: $\langle e_2, e_1 \rangle = m \cdot 1 + (-m) \cdot 1 + m \cdot 0 = 0$." "\n"
                r"Bình phương độ dài của $e_2$ là:" "\n"
                r"$$\|e_2\|^2 = m^2 + (-m)^2 + m^2 = 3m^2.$$" "\n"
                r"Vậy đáp án đúng là **B** ($3m^2$)."
            ),
            "rubric_points": [
                {"step": "Tính đúng ||e_1||^2 = 2 và tích vô hướng <u_2, e_1> = 2m", "points": 0.5},
                {"step": "Xác định e_2 = (m, -m, m) và tính ||e_2||^2 = 3m^2", "points": 0.5},
            ],
            "lean4_code": """-- Lean 4 Core verification for ALG-EUC-02 (No Mathlib, No sorry)
def dot3 (x1 x2 x3 y1 y2 y3 : Int) : Int :=
  x1 * y1 + x2 * y2 + x3 * y3

def e2_vec (m : Int) : Int × Int × Int :=
  (2 * m - m * 1, 0 - m * 1, m - m * 0)

def e2_norm_sq (m : Int) : Int :=
  let (a, b, c) := e2_vec m
  dot3 a b c a b c

theorem alg_euc_02_orthogonal :
    (List.range 10).all (fun k => let m := Int.ofNat (k + 2); let (a, b, c) := e2_vec m; dot3 a b c 1 1 0 == 0) = true := by
  decide

theorem alg_euc_02_m3 : e2_norm_sq 3 = 3 * 3 * 3 := by decide
theorem alg_euc_02_m7 : e2_norm_sq 7 = 3 * 7 * 7 := by decide

#eval e2_norm_sq 3
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
u1 = sp.Matrix([1, 1, 0])
u2 = sp.Matrix([2*m, 0, m])

e1 = u1
e2 = u2 - (u2.dot(e1) / e1.dot(e1)) * e1
assert sp.simplify(e2.dot(e1)) == 0, "e1 and e2 must be orthogonal"
norm_e2_sq = sp.simplify(e2.dot(e2))
assert sp.simplify(norm_e2_sq - 3*m**2) == 0, f"Mismatch: {norm_e2_sq}"

for m_val in range(2, 10):
    u1_n = np.array([1.0, 1.0, 0.0])
    u2_n = np.array([2.0 * m_val, 0.0, 1.0 * m_val])
    e1_n = u1_n
    e2_n = u2_n - (np.dot(u2_n, e1_n) / np.dot(e1_n, e1_n)) * e1_n
    assert abs(np.dot(e1_n, e2_n)) < 1e-9
    assert abs(np.dot(e2_n, e2_n) - 3.0 * (m_val ** 2)) < 1e-9

print(f"VERIFIED_OK: ALG-EUC-02 norm_e2_sq={norm_e2_sq}")
""",
        },
        {
            "code": "ALG-EUC-03",
            "agent_id": 20,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian Euclid, Trực giao hóa Gram-Schmidt & Hình chiếu trực giao",
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
            "title": "Hình chiếu trực giao và bình phương khoảng cách từ vectơ đến không gian con trong R^4",
            "stem_symbolic": (
                r"Trong không gian Euclid $\mathbb{R}^4$ với tích vô hướng chính tắc, cho không gian con "
                r"$W = \text{span}\{u_1, u_2\}$ với $u_1 = (1, 1, 1, 1)$, $u_2 = (1, 3, -1, 1)$ "
                r"và vectơ $v = (3m, 4m, 0, m)$ phụ thuộc tham số nguyên dương $m \ge 2$." "\n"
                r"a) Thực hiện trực giao hóa Gram-Schmidt hệ $\{u_1, u_2\}$ để tìm một cơ sở trực giao $\{e_1, e_2\}$ của $W$." "\n"
                r"b) Tìm hình chiếu trực giao $p = \text{proj}_W(v)$ của $v$ lên $W$, thành phần trực giao $z = v - p \in W^\perp$, "
                r"và tính bình phương khoảng cách $d(v, W)^2 = \|v - \text{proj}_W(v)\|^2$ theo $m$."
            ),
            "stem_template": (
                r"Trong không gian Euclid $\mathbb{R}^4$ với tích vô hướng chính tắc, cho không gian con "
                r"$W = \text{span}\{u_1, u_2\}$ với $u_1 = (1, 1, 1, 1)$, $u_2 = (1, 3, -1, 1)$ "
                r"và vectơ $v = (3\cdot {m}, 4\cdot {m}, 0, {m})$ (với $m = {m}$)." "\n"
                r"a) Thực hiện trực giao hóa Gram-Schmidt hệ $\{u_1, u_2\}$ để tìm một cơ sở trực giao $\{e_1, e_2\}$ của $W$." "\n"
                r"b) Tìm hình chiếu trực giao $p = \text{proj}_W(v)$ của $v$ lên $W$, thành phần trực giao $z = v - p \in W^\perp$, "
                r"và tính bình phương khoảng cách $d(v, W)^2 = \|v - \text{proj}_W(v)\|^2$."
            ),
            "options_symbolic": {
                "A": r"$d(v, W)^2 = 2m^2$, với $\text{proj}_W(v) = (2m, 4m, 0, 2m)$",
                "B": r"$d(v, W)^2 = 4m^2$, với $\text{proj}_W(v) = (2m, 4m, 0, 2m)$",
                "C": r"$d(v, W)^2 = 24m^2$, với $\text{proj}_W(v) = (m, 0, 0, -m)$",
                "D": r"$d(v, W)^2 = 26m^2$, với $\text{proj}_W(v) = (3m, 4m, 0, m)$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m**2",
                    "B": "4*m**2",
                    "C": "24*m**2",
                    "D": "26*m**2",
                },
                "target_expr": "2*m**2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**a) Trực giao hóa Gram-Schmidt tìm cơ sở trực giao $\{e_1, e_2\}$ của $W$:**" "\n"
                r"- Chọn $e_1 = u_1 = (1, 1, 1, 1)$, ta có $\|e_1\|^2 = 1^2 + 1^2 + 1^2 + 1^2 = 4$." "\n"
                r"- Tính $\langle u_2, e_1 \rangle = 1\cdot 1 + 3\cdot 1 + (-1)\cdot 1 + 1\cdot 1 = 4$." "\n"
                r"- Suy ra:" "\n"
                r"$$e_2 = u_2 - \dfrac{\langle u_2, e_1 \rangle}{\|e_1\|^2} e_1 = (1, 3, -1, 1) - \dfrac{4}{4}(1, 1, 1, 1) = (0, 2, -2, 0).$$" "\n"
                r"- Ta có $\|e_2\|^2 = 0^2 + 2^2 + (-2)^2 + 0^2 = 8$ và $\langle e_1, e_2 \rangle = 0$." "\n\n"
                r"**b) Hình chiếu trực giao $\text{proj}_W(v)$ và bình phương khoảng cách $d(v, W)^2$:**" "\n"
                r"- Với $v = (3m, 4m, 0, m)$, tính các tích vô hướng:" "\n"
                r"$$\langle v, e_1 \rangle = 3m + 4m + 0 + m = 8m \implies \dfrac{\langle v, e_1 \rangle}{\|e_1\|^2} = \dfrac{8m}{4} = 2m,$$" "\n"
                r"$$\langle v, e_2 \rangle = 3m\cdot 0 + 4m\cdot 2 + 0\cdot(-2) + m\cdot 0 = 8m \implies \dfrac{\langle v, e_2 \rangle}{\|e_2\|^2} = \dfrac{8m}{8} = m.$$" "\n"
                r"- Hình chiếu trực giao của $v$ lên $W$ là:" "\n"
                r"$$p = \text{proj}_W(v) = 2m e_1 + m e_2 = (2m, 2m, 2m, 2m) + (0, 2m, -2m, 0) = (2m, 4m, 0, 2m).$$" "\n"
                r"- Thành phần trực giao với $W$ là:" "\n"
                r"$$z = v - p = (3m, 4m, 0, m) - (2m, 4m, 0, 2m) = (m, 0, 0, -m) \in W^\perp.$$" "\n"
                r"- Bình phương khoảng cách từ $v$ đến $W$ là:" "\n"
                r"$$d(v, W)^2 = \|z\|^2 = m^2 + 0^2 + 0^2 + (-m)^2 = 2m^2.$$" "\n"
                r"- Kiểm chứng định lý Pythagoras trong không gian Euclid: $\|p\|^2 + \|z\|^2 = 24m^2 + 2m^2 = 26m^2 = \|v\|^2$."
            ),
            "rubric_points": [
                {"step": "Trực giao hóa Gram-Schmidt tìm đúng e_1 = (1,1,1,1) và e_2 = (0,2,-2,0)", "points": 0.75},
                {"step": "Tính đúng các hệ số chiếu <v,e_1>/||e_1||^2 = 2m và <v,e_2>/||e_2||^2 = m", "points": 0.5},
                {"step": "Xác định hình chiếu p = (2m, 4m, 0, 2m) và vectơ độ lệch trực giao z = (m, 0, 0, -m)", "points": 0.5},
                {"step": "Kết luận bình phương khoảng cách d(v, W)^2 = 2m^2 và kiểm tra đẳng thức Pythagoras", "points": 0.25},
            ],
            "lean4_code": """-- Lean 4 Core verification for ALG-EUC-03 (No Mathlib, No sorry)
def dot4 (x1 x2 x3 x4 y1 y2 y3 y4 : Int) : Int :=
  x1 * y1 + x2 * y2 + x3 * y3 + x4 * y4

def dist_sq_W (m : Int) : Int :=
  let z1 := 3 * m - 2 * m
  let z2 := 4 * m - 4 * m
  let z3 := 0 - 0
  let z4 := m - 2 * m
  dot4 z1 z2 z3 z4 z1 z2 z3 z4

theorem alg_euc_03_z_orth_e1 (m : Int) :
    dot4 m 0 0 (-m) 1 1 1 1 = 0 := by
  unfold dot4; omega

theorem alg_euc_03_z_orth_e2 (m : Int) :
    dot4 m 0 0 (-m) 0 2 (-2) 0 = 0 := by
  unfold dot4; omega

theorem alg_euc_03_m3 : dist_sq_W 3 = 2 * 3 * 3 := by decide
theorem alg_euc_03_m6 : dist_sq_W 6 = 2 * 6 * 6 := by decide

#eval dist_sq_W 3
""",
            "python_code": """import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
u1 = sp.Matrix([1, 1, 1, 1])
u2 = sp.Matrix([1, 3, -1, 1])
v = sp.Matrix([3*m, 4*m, 0, m])

e1 = u1
e2 = u2 - (u2.dot(e1) / e1.dot(e1)) * e1
assert sp.simplify(e1.dot(e2)) == 0

p = (v.dot(e1) / e1.dot(e1)) * e1 + (v.dot(e2) / e2.dot(e2)) * e2
z = sp.simplify(v - p)
assert sp.simplify(z.dot(e1)) == 0 and sp.simplify(z.dot(e2)) == 0

dist_sq = sp.simplify(z.dot(z))
assert sp.simplify(dist_sq - 2*m**2) == 0, f"Mismatch dist_sq: {dist_sq}"
assert sp.simplify(p.dot(p) + z.dot(z) - v.dot(v)) == 0, "Pythagoras failed"

for m_val in range(2, 10):
    A = np.array([[1.0, 1.0, 1.0, 1.0], [1.0, 3.0, -1.0, 1.0]]).T
    v_n = np.array([3.0 * m_val, 4.0 * m_val, 0.0, 1.0 * m_val])
    p_n = A @ np.linalg.lstsq(A, v_n, rcond=None)[0]
    z_n = v_n - p_n
    assert abs(np.dot(z_n, z_n) - 2.0 * (m_val ** 2)) < 1e-9

print(f"VERIFIED_OK: ALG-EUC-03 dist_sq={dist_sq}")
""",
        },
    ]
