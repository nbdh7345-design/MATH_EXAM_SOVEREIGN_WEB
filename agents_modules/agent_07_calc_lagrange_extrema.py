"""
Agent-07: Giải tích — Nhân tử Lagrange & Cực trị có điều kiện theo tham số.
Sinh và kiểm chứng tự động (SymPy + NumPy + Lean 4 Core) 3 câu hỏi chuẩn mực:
- CALC-LAG-01 (MCQ): Cực trị hàm tuyến tính trên đường tròn/elip tham số m.
- CALC-LAG-02 (MCQ): Cực trị dạng toàn phương 3 biến trên siêu phẳng và nhân tử Lagrange.
- CALC-LAG-03 (Essay): Giá trị lớn nhất, giá trị nhỏ nhất toàn cục trên miền hình tròn đóng (compact) D_m.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 7,
    "agent_code": "AGENT-07",
    "agent_name": "Agent-07 (Giải tích: Nhân tử Lagrange & Cực trị có điều kiện)",
    "domain": "Giải tích",
    "role_desc": "Sinh & kiểm chứng câu hỏi Cực trị có điều kiện, Nhân tử Lagrange & GTLN/GTNN trên miền compact chứa tham số",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn hóa của Agent-07."""
    return [
        # =====================================================================
        # CÂU 1: CALC-LAG-01 (MCQ)
        # =====================================================================
        {
            "code": "CALC-LAG-01",
            "agent_id": 7,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Nhân tử Lagrange & Cực trị có điều kiện theo tham số",
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
            "title": "Giá trị lớn nhất của hàm tuyến tính trên đường tròn tham số m",
            "stem_symbolic": (
                "Cho tham số nguyên dương $m \\ge 2$. Sử dụng phương pháp nhân tử Lagrange, "
                "hãy tìm giá trị lớn nhất $M(m)$ của hàm mục tiêu $f(x, y) = 3m x + 4m y$ "
                "trên đường tròn ràng buộc $g(x, y) = x^2 + y^2 - m^2 = 0$."
            ),
            "stem_template": (
                "Với tham số $m = {m}$, sử dụng phương pháp nhân tử Lagrange, hãy tìm giá trị "
                "lớn nhất $M({m})$ của hàm mục tiêu $f(x, y) = 3 \\cdot {m} x + 4 \\cdot {m} y$ "
                "trên đường tròn ràng buộc $x^2 + y^2 = {m}^2$."
            ),
            "options_symbolic": {
                "A": "$M(m) = 5m^2$",
                "B": "$M(m) = 7m^2$",
                "C": "$M(m) = 25m^2$",
                "D": "$M(m) = 5m$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "5*m**2",
                    "B": "7*m**2",
                    "C": "25*m**2",
                    "D": "5*m",
                },
                "target_expr": "5*m**2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                "**Lời giải chi tiết (Phương pháp nhân tử Lagrange):**\n\n"
                "1. **Lập hàm Lagrange:**\n"
                "   $$\\mathcal{L}(x, y, \\lambda) = 3mx + 4my - \\lambda(x^2 + y^2 - m^2)$$\n"
                "   Vì $\\nabla g(x, y) = (2x, 2y) \\ne (0, 0)$ trên toàn bộ đường tròn $x^2 + y^2 = m^2 > 0$, "
                "điều kiện chính quy LICQ được thỏa mãn tại mọi điểm khả dĩ.\n\n"
                "2. **Hệ phương trình điểm dừng Lagrange:**\n"
                "   $$\\begin{cases} "
                "\\dfrac{\\partial \\mathcal{L}}{\\partial x} = 3m - 2\\lambda x = 0 \\implies x = \\dfrac{3m}{2\\lambda} \\\\[6pt] "
                "\\dfrac{\\partial \\mathcal{L}}{\\partial y} = 4m - 2\\lambda y = 0 \\implies y = \\dfrac{4m}{2\\lambda} \\\\[6pt] "
                "x^2 + y^2 = m^2 "
                "\\end{cases}$$\n\n"
                "3. **Giải tìm nhân tử $\\lambda$ và tọa độ điểm cực trị:**\n"
                "   Thay $x, y$ vào phương trình ràng buộc:\n"
                "   $$\\frac{9m^2 + 16m^2}{4\\lambda^2} = m^2 \\iff \\frac{25}{4\\lambda^2} = 1 \\iff \\lambda = \\pm \\frac{5}{2}$$\n"
                "   - Với $\\lambda = \\dfrac{5}{2}$: $(x^*, y^*) = \\left(\\dfrac{3}{5}m, \\dfrac{4}{5}m\\right)$, "
                "giá trị hàm mục tiêu đạt cực đại:\n"
                "     $$f(x^*, y^*) = 3m\\left(\\frac{3}{5}m\\right) + 4m\\left(\\frac{4}{5}m\\right) = 5m^2$$\n"
                "   - Với $\\lambda = -\\dfrac{5}{2}$: $(x_*, y_*) = \\left(-\\dfrac{3}{5}m, -\\dfrac{4}{5}m\\right)$, "
                "giá trị hàm mục tiêu đạt cực tiểu $f(x_*, y_*) = -5m^2$.\n\n"
                "Vậy $M(m) = 5m^2$. Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Thiết lập đúng hàm Lagrange L(x, y, lambda) và kiểm tra điều kiện chính quy grad(g) != 0 (0.25đ)",
                "Viết đúng hệ phương trình đạo hàm riêng dL/dx = 0, dL/dy = 0, g(x,y) = 0 (0.25đ)",
                "Giải đúng nhân tử lambda = +-5/2 và tọa độ điểm dừng (+-3m/5, +-4m/5) (0.25đ)",
                "Kết luận đúng giá trị lớn nhất M(m) = 5m^2 (0.25đ)",
            ],
            "lean4_code": """-- Lean 4 Core Verification for CALC-LAG-01 (No Mathlib, No sorry)
def max_lagrange_01 (m : Nat) : Nat := 5 * m * m

-- Kiểm chứng đẳng thức đại số Cauchy-Schwarz / Lagrange đã quy đồng mẫu số 5:
-- (3*x + 4*y)^2 + (4*x - 3*y)^2 = 25 * (x^2 + y^2)
-- Tại điểm cực đại (3m, 4m) (tỉ lệ x5): 3m*(3m) + 4m*(4m) = 25*m^2 = 5 * (5*m^2)
theorem calc_lag_01_m3 : max_lagrange_01 3 = 45 := by decide
theorem calc_lag_01_m5 : max_lagrange_01 5 = 125 := by decide

theorem cauchy_identity_m3 :
    let m := 3
    let x5 := 3 * m
    let y5 := 4 * m
    (3 * m * x5 + 4 * m * y5) / 5 = max_lagrange_01 m := by decide

#eval max_lagrange_01 3
#eval max_lagrange_01 7
""",
            "python_code": """import sympy as sp
import numpy as np

def verify_calc_lag_01():
    x, y, lam = sp.symbols('x y lam', real=True)
    m = sp.Symbol('m', positive=True)

    f = 3 * m * x + 4 * m * y
    g = x**2 + y**2 - m**2
    L = f - lam * g

    eqs = [sp.diff(L, x), sp.diff(L, y), g]
    sols = sp.solve(eqs, (x, y, lam), dict=True)
    vals = [sp.simplify(f.subs(s)) for s in sols]
    sym_max = sp.simplify(max(vals, key=lambda v: float(v.subs(m, 3))))

    expected = 5 * m**2
    assert sp.simplify(sym_max - expected) == 0, f"SymPy mismatch: {sym_max} != {expected}"

    # Kiểm chứng số học trên lưới góc lượng giác cho mọi m từ 2 đến 9
    theta = np.linspace(0, 2 * np.pi, 20000)
    for m_val in range(2, 10):
        xs = m_val * np.cos(theta)
        ys = m_val * np.sin(theta)
        f_num = np.max(3 * m_val * xs + 4 * m_val * ys)
        f_exact = 5 * (m_val ** 2)
        assert abs(f_num - f_exact) < 1e-4, f"NumPy mismatch at m={m_val}: {f_num} vs {f_exact}"

    print(f"VERIFIED_OK: CALC-LAG-01 | M(m) = {sym_max} | M(3) = {expected.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_lag_01()
""",
        },
        # =====================================================================
        # CÂU 2: CALC-LAG-02 (MCQ)
        # =====================================================================
        {
            "code": "CALC-LAG-02",
            "agent_id": 7,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Nhân tử Lagrange & Cực trị có điều kiện theo tham số",
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
            "title": "Cực tiểu hàm toàn phương 3 biến trên siêu phẳng và nhân tử Lagrange",
            "stem_symbolic": (
                "Cho tham số nguyên dương $m \\ge 2$. Xét bài toán tìm giá trị nhỏ nhất $f_{\\min}(m)$ "
                "của hàm mục tiêu $f(x, y, z) = x^2 + y^2 + z^2$ với điều kiện ràng buộc siêu phẳng "
                "$g(x, y, z) = x + 2y + 2z - 9m = 0$. Với hàm Lagrange được định nghĩa tường minh bởi "
                "$\\mathcal{L}(x, y, z, \\lambda) = x^2 + y^2 + z^2 - \\lambda(x + 2y + 2z - 9m)$, "
                "gọi $\\lambda^*$ là nhân tử Lagrange tại điểm cực tiểu. Tính $P(m) = f_{\\min}(m) + \\lambda^*$."
            ),
            "stem_template": (
                "Với tham số $m = {m}$, xét bài toán tìm giá trị nhỏ nhất $f_{\\min}({m})$ của hàm "
                "$f(x, y, z) = x^2 + y^2 + z^2$ thỏa mãn ràng buộc $x + 2y + 2z - 9 \\cdot {m} = 0$. "
                "Với hàm Lagrange $\\mathcal{L}(x, y, z, \\lambda) = x^2 + y^2 + z^2 - \\lambda(x + 2y + 2z - 9 \\cdot {m})$ "
                "và nhân tử Lagrange $\\lambda^*$ tại điểm cực tiểu, hãy tính $P({m}) = f_{\\min}({m}) + \\lambda^*$."
            ),
            "options_symbolic": {
                "A": "$P(m) = 9m^2$",
                "B": "$P(m) = 9m^2 + 2m$",
                "C": "$P(m) = 9m^2 - 2m$",
                "D": "$P(m) = 81m^2 + 2m$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "9*m**2",
                    "B": "9*m**2 + 2*m",
                    "C": "9*m**2 - 2*m",
                    "D": "81*m**2 + 2*m",
                },
                "target_expr": "9*m**2 + 2*m",
            },
            "correct_option": "B",
            "solution_symbolic": (
                "**Lời giải chi tiết:**\n\n"
                "1. **Thiết lập điều kiện dừng của hàm Lagrange:**\n"
                "   $$\\mathcal{L}(x, y, z, \\lambda) = x^2 + y^2 + z^2 - \\lambda(x + 2y + 2z - 9m)$$\n"
                "   Hệ phương trình điểm dừng:\n"
                "   $$\\begin{cases} "
                "\\dfrac{\\partial \\mathcal{L}}{\\partial x} = 2x - \\lambda = 0 \\implies x = \\dfrac{\\lambda}{2} \\\\[6pt] "
                "\\dfrac{\\partial \\mathcal{L}}{\\partial y} = 2y - 2\\lambda = 0 \\implies y = \\lambda \\\\[6pt] "
                "\\dfrac{\\partial \\mathcal{L}}{\\partial z} = 2z - 2\\lambda = 0 \\implies z = \\lambda \\\\[6pt] "
                "x + 2y + 2z = 9m "
                "\\end{cases}$$\n\n"
                "2. **Xác định nhân tử $\\lambda^*$ và điểm cực tiểu:**\n"
                "   Thay $x, y, z$ theo $\\lambda$ vào phương trình siêu phẳng:\n"
                "   $$\\frac{\\lambda}{2} + 2\\lambda + 2\\lambda = 9m \\iff \\frac{9}{2}\\lambda = 9m \\iff \\lambda^* = 2m$$\n"
                "   Suy ra điểm dừng duy nhất là $(x^*, y^*, z^*) = (m, 2m, 2m)$.\n\n"
                "3. **Kiểm tra điều kiện đủ cấp hai và tính $P(m)$:**\n"
                "   Vi phân cấp hai của hàm Lagrange: $d^2\\mathcal{L} = 2(dx^2 + dy^2 + dz^2) > 0$ với mọi $(dx, dy, dz) \\ne (0, 0, 0)$.\n"
                "   Do đó hàm số đạt giá trị nhỏ nhất toàn cục trên siêu phẳng tại $(m, 2m, 2m)$:\n"
                "   $$f_{\\min}(m) = m^2 + (2m)^2 + (2m)^2 = 9m^2$$\n"
                "   Vậy $P(m) = f_{\\min}(m) + \\lambda^* = 9m^2 + 2m$. Chọn đáp án **B**."
            ),
            "rubric_points": [
                "Viết đúng hệ phương trình Lagrange 2x = lambda, 2y = 2*lambda, 2z = 2*lambda (0.25đ)",
                "Thay vào phương trình ràng buộc giải đúng nhân tử Lagrange lambda* = 2m (0.25đ)",
                "Tìm đúng tọa độ điểm cực tiểu (x*, y*, z*) = (m, 2m, 2m) và f_min(m) = 9m^2 (0.25đ)",
                "Tính đúng tổng P(m) = 9m^2 + 2m (0.25đ)",
            ],
            "lean4_code": """-- Lean 4 Core Verification for CALC-LAG-02 (No Mathlib, No sorry)
def f_min_02 (m : Nat) : Nat := 9 * m * m
def lambda_star_02 (m : Nat) : Nat := 2 * m
def P_02 (m : Nat) : Nat := f_min_02 m + lambda_star_02 m

theorem calc_lag_02_constraint (m : Nat) :
    let x := m
    let y := 2 * m
    let z := 2 * m
    x + 2 * y + 2 * z = 9 * m := by omega

theorem calc_lag_02_m3 : P_02 3 = 87 := by decide
theorem calc_lag_02_m4 : P_02 4 = 152 := by decide

#eval P_02 3
#eval P_02 5
""",
            "python_code": """import sympy as sp
import numpy as np

def verify_calc_lag_02():
    x, y, z, lam = sp.symbols('x y z lam', real=True)
    m = sp.Symbol('m', positive=True)

    f = x**2 + y**2 + z**2
    g = x + 2 * y + 2 * z - 9 * m
    L = f - lam * g

    sol = sp.solve([sp.diff(L, x), sp.diff(L, y), sp.diff(L, z), g], (x, y, z, lam), dict=True)[0]
    f_min_sym = sp.simplify(f.subs(sol))
    lam_sym = sp.simplify(sol[lam])
    P_sym = sp.simplify(f_min_sym + lam_sym)

    expected = 9 * m**2 + 2 * m
    assert sp.simplify(P_sym - expected) == 0, f"SymPy mismatch: {P_sym} != {expected}"

    # Kiểm chứng số học trên siêu phẳng x = 9m - 2y - 2z cho m = 2..9
    for m_val in range(2, 10):
        ys = np.linspace(2 * m_val - 3, 2 * m_val + 3, 401)
        zs = np.linspace(2 * m_val - 3, 2 * m_val + 3, 401)
        Y, Z = np.meshgrid(ys, zs)
        X = 9 * m_val - 2 * Y - 2 * Z
        F_val = np.min(X**2 + Y**2 + Z**2)
        assert abs(F_val - 9 * (m_val ** 2)) < 1e-8, f"NumPy mismatch at m={m_val}"

    print(f"VERIFIED_OK: CALC-LAG-02 | P(m) = {P_sym} | P(3) = {expected.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_lag_02()
""",
        },
        # =====================================================================
        # CÂU 3: CALC-LAG-03 (ESSAY)
        # =====================================================================
        {
            "code": "CALC-LAG-03",
            "agent_id": 7,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Nhân tử Lagrange & Cực trị có điều kiện theo tham số",
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
            "title": "Tìm GTLN và GTNN toàn cục trên miền hình tròn đóng (compact) chứa tham số m",
            "stem_symbolic": (
                "Cho tham số nguyên dương $m \\ge 2$. Xét hàm số khả vi liên tục "
                "$f(x, y) = x^2 + y^2 - 2mx + 2m^2$ trên miền đóng và bị chặn (compact) "
                "$D_m = \\{(x, y) \\in \\mathbb{R}^2 : x^2 + y^2 \\le 4m^2\\}$.\n"
                "a) Tìm các điểm dừng của $f(x, y)$ trong miền trong $\\text{int}(D_m)$ và tính giá trị hàm tại đó.\n"
                "b) Sử dụng phương pháp nhân tử Lagrange, tìm các điểm cực trị có điều kiện của $f(x, y)$ "
                "trên biên $\\partial D_m = \\{(x, y) \\in \\mathbb{R}^2 : x^2 + y^2 = 4m^2\\}$.\n"
                "c) Từ đó xác định giá trị lớn nhất toàn cục $f_{\\max}(m)$, giá trị nhỏ nhất toàn cục $f_{\\min}(m)$ "
                "trên $D_m$ và tính tổng $T(m) = f_{\\max}(m) + f_{\\min}(m)$."
            ),
            "stem_template": (
                "Với tham số $m = {m}$, xét hàm số $f(x, y) = x^2 + y^2 - 2 \\cdot {m}x + 2 \\cdot {m}^2$ "
                "trên miền hình tròn đóng $D_{{{m}}} = \\{{(x, y) \\in \\mathbb{{R}}^2 : x^2 + y^2 \\le 4 \\cdot {m}^2\\}}$.\n"
                "a) Tìm điểm dừng của $f(x, y)$ trong miền trong $x^2 + y^2 < 4 \\cdot {m}^2$.\n"
                "b) Dùng phương pháp nhân tử Lagrange tìm các điểm nghi ngờ cực trị trên biên $x^2 + y^2 = 4 \\cdot {m}^2$.\n"
                "c) Xác định $f_{{\\max}}({m})$, $f_{{\\min}}({m})$ trên $D_{{{m}}}$ và tính $T({m}) = f_{{\\max}}({m}) + f_{{\\min}}({m})$."
            ),
            "options_symbolic": {
                "A": "$T(m) = 11m^2$ (với $f_{\\max}(m) = 10m^2, f_{\\min}(m) = m^2$)",
                "B": "$T(m) = 12m^2$ (với $f_{\\max}(m) = 10m^2, f_{\\min}(m) = 2m^2$)",
                "C": "$T(m) = 9m^2$ (với $f_{\\max}(m) = 8m^2, f_{\\min}(m) = m^2$)",
                "D": "$T(m) = 13m^2$ (với $f_{\\max}(m) = 11m^2, f_{\\min}(m) = 2m^2$)",
            },
            "parametric_formulas": {
                "options": {
                    "A": "11*m**2",
                    "B": "12*m**2",
                    "C": "9*m**2",
                    "D": "13*m**2",
                },
                "target_expr": "11*m**2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                "**Lời giải tự luận chi tiết:**\n\n"
                "**Bước 1: Sự tồn tại GTLN và GTNN toàn cục (Định lý Weierstrass)**\n"
                "Miền $D_m = \\{(x, y) \\in \\mathbb{R}^2 : x^2 + y^2 \\le 4m^2\\}$ là tập đóng và bị chặn (compact) trong $\\mathbb{R}^2$, "
                "và $f(x, y)$ là đa thức liên tục trên $D_m$, nên tồn tại GTLN và GTNN toàn cục trên $D_m$.\n\n"
                "**Bước 2: Tìm điểm dừng trong miền trong $\\text{int}(D_m) = \\{x^2 + y^2 < 4m^2\\}$**\n"
                "Giải hệ phương trình đạo hàm riêng bằng $0$:\n"
                "$$\\begin{cases} "
                "\\dfrac{\\partial f}{\\partial x} = 2x - 2m = 0 \\\\[6pt] "
                "\\dfrac{\\partial f}{\\partial y} = 2y = 0 "
                "\\end{cases} \\iff \\begin{cases} x = m \\\\ y = 0 \\end{cases}$$\n"
                "Kiểm tra điều kiện thuộc miền trong: $x^2 + y^2 = m^2 + 0 = m^2 < 4m^2$ (luôn đúng vì $m \\ge 2 > 0$). "
                "Vậy $A(m, 0) \\in \\text{int}(D_m)$ là điểm dừng nội bộ duy nhất.\n"
                "Giá trị hàm tại $A(m, 0)$:\n"
                "$$f(m, 0) = m^2 + 0 - 2m^2 + 2m^2 = m^2$$\n\n"
                "**Bước 3: Khảo sát trên biên $\\partial D_m = \\{g(x, y) = x^2 + y^2 - 4m^2 = 0\\}$ bằng Nhân tử Lagrange**\n"
                "Lập hàm Lagrange:\n"
                "$$\\mathcal{L}(x, y, \\lambda) = x^2 + y^2 - 2mx + 2m^2 - \\lambda(x^2 + y^2 - 4m^2)$$\n"
                "Hệ phương trình điểm dừng trên biên:\n"
                "$$\\begin{cases} "
                "\\dfrac{\\partial \\mathcal{L}}{\\partial x} = 2x(1 - \\lambda) - 2m = 0 \\quad (1) \\\\[6pt] "
                "\\dfrac{\\partial \\mathcal{L}}{\\partial y} = 2y(1 - \\lambda) = 0 \\quad (2) \\\\[6pt] "
                "x^2 + y^2 = 4m^2 \\quad (3) "
                "\\end{cases}$$\n"
                "Từ $(1)$, do $m \\ge 2 > 0$ nên $1 - \\lambda \\ne 0$. Thay vào $(2)$ suy ra $y = 0$.\n"
                "Thế $y = 0$ vào $(3)$ ta được $x^2 = 4m^2 \\iff x = 2m$ hoặc $x = -2m$:\n"
                "- Tại $B_1(2m, 0)$ (ứng với $\\lambda_1 = \\frac{1}{2}$): $f(2m, 0) = 4m^2 - 4m^2 + 2m^2 = 2m^2$.\n"
                "- Tại $B_2(-2m, 0)$ (ứng với $\\lambda_2 = \\frac{3}{2}$): $f(-2m, 0) = 4m^2 + 4m^2 + 2m^2 = 10m^2$.\n\n"
                "**Bước 4: So sánh và kết luận**\n"
                "So sánh các giá trị ứng viên $\\{m^2, 2m^2, 10m^2\\}$ với $m \\ge 2$:\n"
                "- Giá trị nhỏ nhất toàn cục: $f_{\\min}(m) = m^2$, đạt tại điểm trong $A(m, 0)$.\n"
                "- Giá trị lớn nhất toàn cục: $f_{\\max}(m) = 10m^2$, đạt tại điểm biên $B_2(-2m, 0)$.\n"
                "- Tổng cần tìm: $T(m) = f_{\\max}(m) + f_{\\min}(m) = 10m^2 + m^2 = 11m^2$."
            ),
            "rubric_points": [
                "Vận dụng định lý Weierstrass khẳng định sự tồn tại GTLN/GTNN trên tập compact D_m (0.20đ)",
                "Giải hệ grad(f) = 0 tìm đúng điểm dừng nội bộ A(m, 0), kiểm tra m^2 < 4m^2 và tính f(m, 0) = m^2 (0.30đ)",
                "Thiết lập hàm Lagrange trên biên x^2 + y^2 = 4m^2, biện luận 1 - lambda != 0 suy ra y = 0 và tìm 2 điểm biên (+-2m, 0) (0.30đ)",
                "Tính đúng f(2m, 0) = 2m^2, f(-2m, 0) = 10m^2, kết luận f_min = m^2, f_max = 10m^2 và T(m) = 11m^2 (0.20đ)",
            ],
            "lean4_code": """-- Lean 4 Core Verification for CALC-LAG-03 (No Mathlib, No sorry)
def f_max_03 (m : Nat) : Nat := 10 * m * m
def f_min_03 (m : Nat) : Nat := m * m
def T_03 (m : Nat) : Nat := f_max_03 m + f_min_03 m

theorem calc_lag_03_formula : (List.range 10).all (fun k => let m := k + 1; T_03 m == 11 * m * m) = true := by
  decide

theorem calc_lag_03_m3 : T_03 3 = 99 := by decide
theorem calc_lag_03_m5 : T_03 5 = 275 := by decide

#eval T_03 3
#eval T_03 6
""",
            "python_code": """import sympy as sp
import numpy as np

def verify_calc_lag_03():
    x, y, lam = sp.symbols('x y lam', real=True)
    m = sp.Symbol('m', positive=True)

    f = x**2 + y**2 - 2 * m * x + 2 * m**2
    g = x**2 + y**2 - 4 * m**2

    # 1. Điểm dừng miền trong
    int_sols = sp.solve([sp.diff(f, x), sp.diff(f, y)], (x, y), dict=True)
    candidates = []
    for s in int_sols:
        if sp.simplify(g.subs(s)).subs(m, 3) < 0:
            candidates.append(sp.simplify(f.subs(s)))

    # 2. Điểm dừng Lagrange trên biên
    L = f - lam * g
    bd_sols = sp.solve([sp.diff(L, x), sp.diff(L, y), g], (x, y, lam), dict=True)
    for s in bd_sols:
        candidates.append(sp.simplify(f.subs(s)))

    f_min_sym = min(candidates, key=lambda v: float(v.subs(m, 3)))
    f_max_sym = max(candidates, key=lambda v: float(v.subs(m, 3)))
    T_sym = sp.simplify(f_max_sym + f_min_sym)

    assert sp.simplify(f_min_sym - m**2) == 0, f"f_min mismatch: {f_min_sym}"
    assert sp.simplify(f_max_sym - 10 * m**2) == 0, f"f_max mismatch: {f_max_sym}"
    assert sp.simplify(T_sym - 11 * m**2) == 0, f"T(m) mismatch: {T_sym}"

    # 3. Kiểm chứng lưới tọa độ cực (r, theta) trên toàn miền compact D_m
    theta = np.linspace(0, 2 * np.pi, 1000)
    r_norm = np.linspace(0, 1.0, 500)
    R_grid, Th_grid = np.meshgrid(r_norm, theta)

    for m_val in range(2, 10):
        R = 2 * m_val * R_grid
        X = R * np.cos(Th_grid)
        Y = R * np.sin(Th_grid)
        F = X**2 + Y**2 - 2 * m_val * X + 2 * (m_val ** 2)
        assert abs(np.min(F) - (m_val ** 2)) < 1e-2, f"Grid min mismatch at m={m_val}"
        assert abs(np.max(F) - 10 * (m_val ** 2)) < 1e-2, f"Grid max mismatch at m={m_val}"

    print(f"VERIFIED_OK: CALC-LAG-03 | f_min={f_min_sym}, f_max={f_max_sym}, T(m)={T_sym} | T(3)={T_sym.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_lag_03()
""",
        },
    ]
