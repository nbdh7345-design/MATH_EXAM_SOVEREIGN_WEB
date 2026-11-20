# -*- coding: utf-8 -*-
"""
Agent-09: Giải tích Vector, Định lý Green, Stokes, Gauss - Ostrogradsky
Sinh & kiểm chứng câu hỏi Tích phân đường, Tích phân mặt, Trường thế,
Định lý Green - Stokes - Ostrogradsky chứa tham số m.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 9,
    "agent_code": "AGENT-09",
    "agent_name": "Agent-09 (Giải tích: Giải tích Vector, Green, Stokes, Gauss)",
    "domain": "Giải tích",
    "role_desc": "Sinh & kiểm chứng câu hỏi Tích phân đường, Tích phân mặt, Trường thế, Định lý Green - Stokes - Ostrogradsky chứa tham số",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa của Agent-09 (2 MCQ, 1 Essay)."""
    return [
        # =====================================================================
        # CÂU 1: CALC-VEC-01 (MCQ) - ĐỊNH LÝ GREEN & TÍCH PHÂN ĐƯỜNG LOẠI 2
        # =====================================================================
        {
            "code": "CALC-VEC-01",
            "agent_id": 9,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Tích phân đường, Tích phân mặt & Định lý Green - Stokes - Gauss",
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
            "title": "Tích phân đường loại 2 và Định lý Green trên miền hình chữ nhật",
            "stem_symbolic": (
                r"Trong mặt phẳng $Oxy$, cho miền hình chữ nhật $D = [0, 2] \times [0, 3]$ "
                r"với biên $C = \partial D^+$ định hướng dương (ngược chiều kim đồng hồ). "
                r"Với tham số nguyên dương $m$, tính tích phân đường loại 2: "
                r"$$I(m) = \oint_{C} \left(x^2 y - m y\right) dx + \left(m x + \frac{1}{3}x^3\right) dy$$"
            ),
            "stem_template": (
                r"Trong mặt phẳng $Oxy$, cho miền hình chữ nhật $D = [0, 2] \times [0, 3]$ "
                r"với biên $C = \partial D^+$ định hướng dương (ngược chiều kim đồng hồ). "
                r"Khi $m = {m}$, tính tích phân đường loại 2: "
                r"$$I({m}) = \oint_{C} \left(x^2 y - {m} y\right) dx + \left({m} x + \frac{{1}}{{3}}x^3\right) dy$$"
            ),
            "options_symbolic": {
                "A": r"$12m$",
                "B": r"$6m$",
                "C": r"$12m + 16$",
                "D": r"$24m$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "12*m",
                    "B": "6*m",
                    "C": "12*m + 16",
                    "D": "24*m",
                },
                "target_expr": "12*m",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Bước 1: Xác định các thành phần của trường vector phẳng.**" "\n"
                r"Đặt $P(x, y) = x^2 y - m y$ và $Q(x, y) = m x + \frac{1}{3}x^3$. "
                r"Các hàm $P, Q$ cùng các đạo hàm riêng cấp một liên tục trên toàn mặt phẳng $\mathbb{R}^2$." "\n\n"
                r"**Bước 2: Áp dụng công thức Green cho miền đóng $D = [0, 2] \times [0, 3]$.**" "\n"
                r"Ta có các đạo hàm riêng:" "\n"
                r"$$\frac{\partial Q}{\partial x} = m + x^2, \quad \frac{\partial P}{\partial y} = x^2 - m$$" "\n"
                r"Suy ra độ xoáy phẳng (thành phần $z$ của $\text{curl}$):" "\n"
                r"$$\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = (m + x^2) - (x^2 - m) = 2m$$" "\n\n"
                r"**Bước 3: Tính tích phân kép trên hình chữ nhật $D$.**" "\n"
                r"Theo Định lý Green với biên $C = \partial D^+$ định hướng dương:" "\n"
                r"$$I(m) = \iint_{D} \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right) dx\,dy "
                r"= \int_{0}^{2} dx \int_{0}^{3} 2m\,dy = 2m \cdot (2 \times 3) = 12m$$" "\n"
                r"Vậy đáp án đúng là **A** ($12m$)."
            ),
            "rubric_points": 1.0,
            "lean4_code": """-- Lean 4 Core Verification for CALC-VEC-01 (Green's Theorem on D = [0,2]x[0,3])
def greenCurlDensity (m : Nat) : Nat := 2 * m
def rectArea : Nat := 2 * 3
def lineIntegralGreen (m : Nat) : Nat := greenCurlDensity m * rectArea

theorem calc_vec_01_formula (m : Nat) : lineIntegralGreen m = 12 * m := by
  unfold lineIntegralGreen greenCurlDensity rectArea
  omega

theorem calc_vec_01_m3 : lineIntegralGreen 3 = 36 := by
  decide

theorem calc_vec_01_grid :
    (List.range 8).all (fun k =>
      let m := k + 2
      lineIntegralGreen m == 12 * m) = true := by
  decide

#eval lineIntegralGreen 3
""",
            "python_code": """import sympy as sp

def verify_calc_vec_01():
    x, y, t, m = sp.symbols('x y t m', real=True)
    P = x**2 * y - m * y
    Q = m * x + sp.Rational(1, 3) * x**3

    # 1. Double integral via Green's Theorem on D = [0, 2] x [0, 3]
    curl_z = sp.diff(Q, x) - sp.diff(P, y)
    I_green = sp.integrate(sp.integrate(curl_z, (y, 0, 3)), (x, 0, 2))

    # 2. Direct line integral over 4 boundary segments of D = [0, 2] x [0, 3]
    # C1: (t, 0), t in [0, 2]
    I1 = sp.integrate(P.subs({x: t, y: 0}), (t, 0, 2))
    # C2: (2, t), t in [0, 3]
    I2 = sp.integrate(Q.subs({x: 2, y: t}), (t, 0, 3))
    # C3: (t, 3), t from 2 to 0
    I3 = sp.integrate(P.subs({x: t, y: 3}), (t, 2, 0))
    # C4: (0, t), t from 3 to 0
    I4 = sp.integrate(Q.subs({x: 0, y: t}), (t, 3, 0))
    I_line = sp.simplify(I1 + I2 + I3 + I4)

    assert sp.simplify(I_green - 12 * m) == 0, f"Mismatch Green: {I_green}"
    assert sp.simplify(I_line - I_green) == 0, f"Mismatch Line vs Green: {I_line} != {I_green}"

    for m_val in range(2, 10):
        val_green = int(I_green.subs(m, m_val))
        val_line = int(I_line.subs(m, m_val))
        assert val_green == 12 * m_val == val_line

    print(f"VERIFIED_OK: CALC-VEC-01 | I(m) = {I_green} | I(3) = {I_green.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_vec_01()
""",
        },
        # =====================================================================
        # CÂU 2: CALC-VEC-02 (MCQ) - TRƯỜNG THẾ & TÍCH PHÂN ĐỘC LẬP ĐƯỜNG ĐI
        # =====================================================================
        {
            "code": "CALC-VEC-02",
            "agent_id": 9,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Tích phân đường, Tích phân mặt & Định lý Green - Stokes - Gauss",
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
            "title": "Trường thế trong không gian R^3 và tích phân đường độc lập đường đi",
            "stem_symbolic": (
                r"Trong không gian $\mathbb{R}^3$, cho trường vector chứa tham số nguyên dương $m$: "
                r"$$\vec{F}(x, y, z) = \left(2m x y + z^2\right)\vec{i} + \left(m x^2 + 2 y z\right)\vec{j} + \left(y^2 + 2 x z + 3m z^2\right)\vec{k}$$"
                r"Tính công của trường lực $W(m) = \int_{\Gamma} \vec{F} \cdot d\vec{r}$ dọc theo đường cong trơn "
                r"$\Gamma$ bất kỳ đi từ điểm $A(0, 0, 0)$ đến điểm $B(1, 2, 1)$."
            ),
            "stem_template": (
                r"Trong không gian $\mathbb{R}^3$, cho trường vector với $m = {m}$: "
                r"$$\vec{{F}}(x, y, z) = \left(2\cdot {m} x y + z^2\right)\vec{{i}} + \left({m} x^2 + 2 y z\right)\vec{{j}} + \left(y^2 + 2 x z + 3\cdot {m} z^2\right)\vec{{k}}$$"
                r"Tính công của trường lực $W({m}) = \int_{{\Gamma}} \vec{{F}} \cdot d\vec{{r}}$ dọc theo đường cong trơn "
                r"$\Gamma$ bất kỳ đi từ điểm $A(0, 0, 0)$ đến điểm $B(1, 2, 1)$."
            ),
            "options_symbolic": {
                "A": r"$2m + 5$",
                "B": r"$3m + 5$",
                "C": r"$3m + 3$",
                "D": r"$4m + 5$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "2*m + 5",
                    "B": "3*m + 5",
                    "C": "3*m + 3",
                    "D": "4*m + 5",
                },
                "target_expr": "3*m + 5",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Bước 1: Kiểm tra điều kiện trường thế ($\text{curl}\,\vec{F} = \vec{0}$).**" "\n"
                r"Với $P = 2mxy + z^2$, $Q = mx^2 + 2yz$, $R = y^2 + 2xz + 3mz^2$, ta tính vector xoáy:" "\n"
                r"$$\nabla \times \vec{F} = \left(\frac{\partial R}{\partial y} - \frac{\partial Q}{\partial z},\, "
                r"\frac{\partial P}{\partial z} - \frac{\partial R}{\partial x},\, "
                r"\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right) "
                r"= (2y - 2y,\, 2z - 2z,\, 2mx - 2mx) = (0, 0, 0)$$" "\n"
                r"Vì miền $\mathbb{R}^3$ đơn liên nên $\vec{F}$ là trường thế." "\n\n"
                r"**Bước 2: Tìm hàm thế vị $U(x, y, z)$ sao cho $\nabla U = \vec{F}$.**" "\n"
                r"Tích phân theo từng biến với $U(0, 0, 0) = 0$:" "\n"
                r"$$U(x, y, z) = \int_{0}^{x} (2m t y + z^2)\,dt + \int_{0}^{y} 2 t z\,dt + \int_{0}^{z} 3m t^2\,dt "
                r"= m x^2 y + x z^2 + y^2 z + m z^3$$" "\n\n"
                r"**Bước 3: Tính tích phân đường từ $A(0,0,0)$ đến $B(1,2,1)$.**" "\n"
                r"$$W(m) = U(1, 2, 1) - U(0, 0, 0) = m(1)^2(2) + (1)(1)^2 + (2)^2(1) + m(1)^3 = 3m + 5$$" "\n"
                r"Vậy đáp án đúng là **B** ($3m + 5$)."
            ),
            "rubric_points": 1.0,
            "lean4_code": """-- Lean 4 Core Verification for CALC-VEC-02 (Conservative Field Potential in R^3)
def potentialU (m x y z : Nat) : Nat :=
  m * x * x * y + x * z * z + y * y * z + m * z * z * z

def workAB (m : Nat) : Nat :=
  potentialU m 1 2 1 - potentialU m 0 0 0

theorem calc_vec_02_formula (m : Nat) : workAB m = 3 * m + 5 := by
  simp [workAB, potentialU]
  omega

theorem calc_vec_02_m3 : workAB 3 = 14 := by
  decide

theorem calc_vec_02_grid :
    (List.range 8).all (fun k =>
      let m := k + 2
      workAB m == 3 * m + 5) = true := by
  decide

#eval workAB 3
""",
            "python_code": """import sympy as sp

def verify_calc_vec_02():
    x, y, z, t, m = sp.symbols('x y z t m', real=True)
    P = 2 * m * x * y + z**2
    Q = m * x**2 + 2 * y * z
    R = y**2 + 2 * x * z + 3 * m * z**2

    # 1. Verify curl(F) == (0, 0, 0)
    curl_x = sp.simplify(sp.diff(R, y) - sp.diff(Q, z))
    curl_y = sp.simplify(sp.diff(P, z) - sp.diff(R, x))
    curl_z = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))
    assert (curl_x, curl_y, curl_z) == (0, 0, 0), "Curl is not zero!"

    # 2. Verify scalar potential U
    U = m * x**2 * y + x * z**2 + y**2 * z + m * z**3
    assert sp.simplify(sp.diff(U, x) - P) == 0
    assert sp.simplify(sp.diff(U, y) - Q) == 0
    assert sp.simplify(sp.diff(U, z) - R) == 0

    W_pot = sp.simplify(U.subs({x: 1, y: 2, z: 1}) - U.subs({x: 0, y: 0, z: 0}))

    # 3. Verify path independence along two distinct paths from A(0,0,0) to B(1,2,1)
    # Path 1: straight line r1(t) = (t, 2t, t), t in [0, 1]
    integrand_1 = P.subs({x: t, y: 2*t, z: t}) * 1 + Q.subs({x: t, y: 2*t, z: t}) * 2 + R.subs({x: t, y: 2*t, z: t}) * 1
    W_path1 = sp.integrate(integrand_1, (t, 0, 1))

    # Path 2: parabolic curve r2(t) = (t, 2*t**2, t**3), t in [0, 1]
    integrand_2 = (
        P.subs({x: t, y: 2*t**2, z: t**3}) * 1
        + Q.subs({x: t, y: 2*t**2, z: t**3}) * (4*t)
        + R.subs({x: t, y: 2*t**2, z: t**3}) * (3*t**2)
    )
    W_path2 = sp.integrate(integrand_2, (t, 0, 1))

    assert sp.simplify(W_pot - (3 * m + 5)) == 0
    assert sp.simplify(W_path1 - W_pot) == 0
    assert sp.simplify(W_path2 - W_pot) == 0

    for m_val in range(2, 10):
        assert int(W_pot.subs(m, m_val)) == 3 * m_val + 5

    print(f"VERIFIED_OK: CALC-VEC-02 | W(m) = {W_pot} | W(3) = {W_pot.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_vec_02()
""",
        },
        # =====================================================================
        # CÂU 3: CALC-VEC-03 (ESSAY) - ĐỊNH LÝ STOKES & GAUSS - OSTROGRADSKY
        # =====================================================================
        {
            "code": "CALC-VEC-03",
            "agent_id": 9,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Tích phân đường, Tích phân mặt & Định lý Green - Stokes - Gauss",
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
            "title": "Tự luận: Thông lượng Gauss - Ostrogradsky và Lưu số Stokes chứa tham số m",
            "stem_symbolic": (
                r"Trong không gian $\mathbb{R}^3$, xét khối hộp chữ nhật $\Omega = [0, 2] \times [0, 1] \times [0, 1]$ "
                r"với mặt biên kín $S = \partial \Omega^+$ định hướng pháp tuyến ngoài và tham số nguyên dương $m$." "\n"
                r"a) Cho trường vector $\vec{F}(x, y, z) = (m x + y^2)\vec{i} + (2m y + z^2)\vec{j} + (3m z + x^2)\vec{k}$. "
                r"Hãy tính độ phân kỳ $\text{div}\,\vec{F}$ và áp dụng Định lý Gauss - Ostrogradsky để tính thông lượng "
                r"$\Phi(m) = \oiint_{S} \vec{F} \cdot d\vec{S}$." "\n"
                r"b) Gọi $\Gamma$ là đường biên của mặt nắp trên $S_{\text{top}} = [0, 2] \times [0, 1] \times \{1\}$ "
                r"định hướng ngược chiều kim đồng hồ khi nhìn từ chiều dương trục $Oz$. "
                r"Cho trường vector $\vec{G}(x, y, z) = (-m y + z)\vec{i} + (2m x + z^2)\vec{j} + (x + y)\vec{k}$. "
                r"Dùng Định lý Stokes tính lưu số $C(m) = \oint_{\Gamma} \vec{G} \cdot d\vec{r}$ và tính tổng $T(m) = \Phi(m) + C(m)$."
            ),
            "stem_template": (
                r"Trong không gian $\mathbb{R}^3$, xét khối hộp chữ nhật $\Omega = [0, 2] \times [0, 1] \times [0, 1]$ "
                r"với mặt biên kín $S = \partial \Omega^+$ định hướng pháp tuyến ngoài và $m = {m}$." "\n"
                r"a) Cho trường vector $\vec{{F}}(x, y, z) = ({m} x + y^2)\vec{{i}} + (2\cdot {m} y + z^2)\vec{{j}} + (3\cdot {m} z + x^2)\vec{{k}}$. "
                r"Hãy tính độ phân kỳ $\text{{div}}\,\vec{{F}}$ và áp dụng Định lý Gauss - Ostrogradsky để tính thông lượng "
                r"$\Phi({m}) = \oiint_{{S}} \vec{{F}} \cdot d\vec{{S}}$." "\n"
                r"b) Gọi $\Gamma$ là đường biên của mặt nắp trên $S_{{\text{{top}}}} = [0, 2] \times [0, 1] \times \{{1\}}$ "
                r"định hướng ngược chiều kim đồng hồ khi nhìn từ chiều dương trục $Oz$. "
                r"Cho trường vector $\vec{{G}}(x, y, z) = (-{m} y + z)\vec{{i}} + (2\cdot {m} x + z^2)\vec{{j}} + (x + y)\vec{{k}}$. "
                r"Dùng Định lý Stokes tính lưu số $C({m}) = \oint_{{\Gamma}} \vec{{G}} \cdot d\vec{{r}}$ và tính tổng $T({m}) = \Phi({m}) + C({m})$."
            ),
            "options_symbolic": {
                "A": r"$T(m) = 18m \quad (\Phi(m) = 12m,\; C(m) = 6m)$",
                "B": r"$T(m) = 15m \quad (\Phi(m) = 12m,\; C(m) = 3m)$",
                "C": r"$T(m) = 12m \quad (\Phi(m) = 6m,\; C(m) = 6m)$",
                "D": r"$T(m) = 24m \quad (\Phi(m) = 18m,\; C(m) = 6m)$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "18*m",
                    "B": "15*m",
                    "C": "12*m",
                    "D": "24*m",
                },
                "target_expr": "18*m",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"### Lời giải chi tiết & Thang điểm chấm (Rubric 2.0 điểm)" "\n\n"
                r"**Phần a) Tính thông lượng $\Phi(m)$ bằng Định lý Gauss - Ostrogradsky (1.0 điểm):**" "\n"
                r"1. Tính độ phân kỳ (Divergence) của trường $\vec{F}$:" "\n"
                r"$$\text{div}\,\vec{F} = \frac{\partial}{\partial x}(mx + y^2) + \frac{\partial}{\partial y}(2my + z^2) + \frac{\partial}{\partial z}(3mz + x^2) = m + 2m + 3m = 6m$$" "\n"
                r"2. Áp dụng Định lý Gauss - Ostrogradsky trên khối hộp $\Omega = [0, 2] \times [0, 1] \times [0, 1]$ có thể tích $V(\Omega) = 2 \times 1 \times 1 = 2$:" "\n"
                r"$$\Phi(m) = \oiint_{S} \vec{F} \cdot d\vec{S} = \iiint_{\Omega} \text{div}\,\vec{F}\,dx\,dy\,dz = 6m \cdot V(\Omega) = 12m$$" "\n\n"
                r"**Phần b) Tính lưu số $C(m)$ bằng Định lý Stokes và tổng $T(m)$ (1.0 điểm):**" "\n"
                r"1. Mặt nắp trên $S_{\text{top}} = [0, 2] \times [0, 1] \times \{1\}$ có vector pháp tuyến đơn vị hướng lên $\vec{n} = (0, 0, 1)$ phù hợp quy tắc bàn tay phải với hướng của $\Gamma$." "\n"
                r"2. Tính thành phần thứ ba của vector xoáy $\text{curl}\,\vec{G} = \nabla \times \vec{G}$:" "\n"
                r"$$(\nabla \times \vec{G})_z = \frac{\partial}{\partial x}(2mx + z^2) - \frac{\partial}{\partial y}(-my + z) = 2m - (-m) = 3m$$" "\n"
                r"3. Theo Định lý Stokes trên mặt $S_{\text{top}}$ có diện tích $\text{Area}(S_{\text{top}}) = 2 \times 1 = 2$:" "\n"
                r"$$C(m) = \oint_{\Gamma} \vec{G} \cdot d\vec{r} = \iint_{S_{\text{top}}} (\nabla \times \vec{G}) \cdot \vec{n}\,dS = \int_{0}^{2} dx \int_{0}^{1} 3m\,dy = 6m$$" "\n"
                r"4. Tổng bất biến cần tìm:" "\n"
                r"$$T(m) = \Phi(m) + C(m) = 12m + 6m = 18m$$"
            ),
            "rubric_points": 2.0,
            "lean4_code": """-- Lean 4 Core Verification for CALC-VEC-03 (Gauss Flux + Stokes Circulation)
def divF (m : Nat) : Nat := m + 2 * m + 3 * m
def boxVolume : Nat := 2 * 1 * 1
def gaussFlux (m : Nat) : Nat := divF m * boxVolume

def curlGz (m : Nat) : Nat := 2 * m + m
def topFaceArea : Nat := 2 * 1
def stokesCirculation (m : Nat) : Nat := curlGz m * topFaceArea

def totalInvariant (m : Nat) : Nat := gaussFlux m + stokesCirculation m

theorem calc_vec_03_flux (m : Nat) : gaussFlux m = 12 * m := by
  simp [gaussFlux, divF, boxVolume]
  omega

theorem calc_vec_03_circ (m : Nat) : stokesCirculation m = 6 * m := by
  simp [stokesCirculation, curlGz, topFaceArea]
  omega

theorem calc_vec_03_total (m : Nat) : totalInvariant m = 18 * m := by
  simp [totalInvariant, gaussFlux, stokesCirculation, divF, curlGz, boxVolume, topFaceArea]
  omega

theorem calc_vec_03_m3 : totalInvariant 3 = 54 := by
  decide

#eval (gaussFlux 3, stokesCirculation 3, totalInvariant 3)
""",
            "python_code": """import sympy as sp

def verify_calc_vec_03():
    x, y, z, t, m = sp.symbols('x y z t m', real=True)

    # Part (a): Gauss - Ostrogradsky Flux vs 6 Surface Integrals
    F1 = m * x + y**2
    F2 = 2 * m * y + z**2
    F3 = 3 * m * z + x**2
    div_F = sp.diff(F1, x) + sp.diff(F2, y) + sp.diff(F3, z)
    flux_gauss = sp.integrate(sp.integrate(sp.integrate(div_F, (z, 0, 1)), (y, 0, 1)), (x, 0, 2))

    # Direct surface flux across 6 faces of [0, 2] x [0, 1] x [0, 1]
    flux_x2 = sp.integrate(sp.integrate(F1.subs(x, 2), (z, 0, 1)), (y, 0, 1))
    flux_x0 = sp.integrate(sp.integrate(-F1.subs(x, 0), (z, 0, 1)), (y, 0, 1))
    flux_y1 = sp.integrate(sp.integrate(F2.subs(y, 1), (z, 0, 1)), (x, 0, 2))
    flux_y0 = sp.integrate(sp.integrate(-F2.subs(y, 0), (z, 0, 1)), (x, 0, 2))
    flux_z1 = sp.integrate(sp.integrate(F3.subs(z, 1), (y, 0, 1)), (x, 0, 2))
    flux_z0 = sp.integrate(sp.integrate(-F3.subs(z, 0), (y, 0, 1)), (x, 0, 2))
    flux_faces = sp.simplify(flux_x2 + flux_x0 + flux_y1 + flux_y0 + flux_z1 + flux_z0)

    assert sp.simplify(flux_gauss - 12 * m) == 0
    assert sp.simplify(flux_faces - flux_gauss) == 0

    # Part (b): Stokes Circulation vs 4 Boundary Line Integrals on z = 1
    G1 = -m * y + z
    G2 = 2 * m * x + z**2
    G3 = x + y
    curl_G_z = sp.diff(G2, x) - sp.diff(G1, y)
    circ_stokes = sp.integrate(sp.integrate(curl_G_z.subs(z, 1), (y, 0, 1)), (x, 0, 2))

    # Direct line integral around [0, 2] x [0, 1] at z = 1
    c1 = sp.integrate(G1.subs({x: t, y: 0, z: 1}), (t, 0, 2))
    c2 = sp.integrate(G2.subs({x: 2, y: t, z: 1}), (t, 0, 1))
    c3 = sp.integrate(G1.subs({x: t, y: 1, z: 1}), (t, 2, 0))
    c4 = sp.integrate(G2.subs({x: 0, y: t, z: 1}), (t, 1, 0))
    circ_line = sp.simplify(c1 + c2 + c3 + c4)

    assert sp.simplify(circ_stokes - 6 * m) == 0
    assert sp.simplify(circ_line - circ_stokes) == 0

    total_T = sp.simplify(flux_gauss + circ_stokes)
    assert sp.simplify(total_T - 18 * m) == 0

    for m_val in range(2, 10):
        assert int(total_T.subs(m, m_val)) == 18 * m_val

    print(f"VERIFIED_OK: CALC-VEC-03 | Phi(m)={flux_gauss}, C(m)={circ_stokes}, T(m)={total_T} | T(3)={total_T.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_vec_03()
""",
        },
    ]
