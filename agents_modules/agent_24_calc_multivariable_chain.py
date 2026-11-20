# -*- coding: utf-8 -*-
"""
Agent-24: Giải tích — Hàm nhiều biến nâng cao: đạo hàm hàm hợp, đạo hàm hàm ẩn,
giới hạn hàm hai biến, gradient & đạo hàm theo hướng có tham số.
Sinh và kiểm chứng tự động (SymPy + Lean 4 Core) cho ngân hàng đề thi.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 24,
    "agent_code": "AGENT-24",
    "agent_name": "Agent-24 (Giải tích: Hàm hợp, Hàm ẩn & Đạo hàm theo hướng)",
    "domain": "Giải tích",
    "role_desc": "Đạo hàm hàm hợp nhiều biến, Đạo hàm hàm ẩn, Giới hạn hàm hai biến & Đạo hàm theo hướng có tham số",
}

_PARAM_M = [
    {
        "name": "m",
        "symbol": "m",
        "default": 3,
        "min": 2,
        "max": 9,
        "step": 1,
        "label": "Tham số nguyên dương m",
    }
]


def get_questions() -> list[dict]:
    """Trả về 3 câu hỏi chuẩn hóa (2 MCQ, 1 Essay) có tham số m thuộc [2..9]."""
    return [
        # =====================================================================
        # CÂU 1: CALC-MV2-01 (MCQ - Vận dụng)
        # =====================================================================
        {
            "code": "CALC-MV2-01",
            "agent_id": 24,
            "agent_name": "Agent-24 (Giải tích: Hàm hợp, Hàm ẩn & Đạo hàm theo hướng)",
            "subject": "Giải tích",
            "topic": "Đạo hàm hàm hợp, hàm ẩn & đạo hàm theo hướng",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Đạo hàm riêng của hàm hợp hai biến theo quy tắc dây chuyền",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$ và hàm hợp $z = u^2 v$ với "
                r"$u = x + m y$, $v = m x - y$. Giá trị $\dfrac{\partial z}{\partial x}(1, 1)$ bằng"
            ),
            "stem_template": (
                r"Cho hàm hợp $z = u^2 v$ với $u = x + {m} y$, $v = {m} x - y$. "
                r"Tính $\dfrac{\partial z}{\partial x}(1, 1)$."
            ),
            "options_symbolic": {
                "A": r"$(m + 1)(m^2 + 3m - 2)$",
                "B": r"$(m + 1)(m^2 + m - 2)$",
                "C": r"$(m + 1)(m^2 + 3m)$",
                "D": r"$2(m + 1)(m - 1)$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "(m + 1)*(m**2 + 3*m - 2)",
                    "B": "(m + 1)*(m**2 + m - 2)",
                    "C": "(m + 1)*(m**2 + 3*m)",
                    "D": "2*(m + 1)*(m - 1)",
                },
                "target_expr": "(m + 1)*(m**2 + 3*m - 2)",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Theo quy tắc đạo hàm hàm hợp:" "\n"
                r"$$\frac{\partial z}{\partial x} = \frac{\partial z}{\partial u}\frac{\partial u}{\partial x} "
                r"+ \frac{\partial z}{\partial v}\frac{\partial v}{\partial x} = 2uv \cdot 1 + u^2 \cdot m.$$" "\n"
                r"Tại $(x, y) = (1, 1)$: $u = m + 1$, $v = m - 1$, nên" "\n"
                r"$$\frac{\partial z}{\partial x}(1, 1) = 2(m + 1)(m - 1) + m(m + 1)^2 = (m + 1)(m^2 + 3m - 2).$$" "\n"
                r"Chọn đáp án **A**."
            ),
            "rubric_points": [
                "Viết đúng công thức đạo hàm hàm hợp z_x = z_u u_x + z_v v_x (0.4 điểm)",
                "Tính đúng u = m + 1, v = m - 1 tại (1, 1) (0.2 điểm)",
                "Rút gọn và kết luận (m + 1)(m^2 + 3m - 2) (0.4 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MV2-01 (chain rule)\n"
                "-- z(x, 1) = (x + m)^2 (m x - 1) = m x^3 + (2m^2 - 1) x^2 + (m^3 - 2m) x - m^2\n"
                "-- => z_x(1, 1) = 3m + 2(2m^2 - 1) + (m^3 - 2m)\n"
                "def zAlongX (m x : Int) : Int := (x + m) ^ 2 * (m * x - 1)\n"
                "def zExpanded (m x : Int) : Int := m * x ^ 3 + (2 * m ^ 2 - 1) * x ^ 2 + (m ^ 3 - 2 * m) * x - m ^ 2\n"
                "def zxAt11 (m : Int) : Int := 3 * m + 2 * (2 * m ^ 2 - 1) + (m ^ 3 - 2 * m)\n"
                "def chainRule (m : Int) : Int := 2 * (m + 1) * (m - 1) * 1 + (m + 1) ^ 2 * m\n"
                "def options (m : Int) : List Int :=\n"
                "  [(m + 1) * (m ^ 2 + 3 * m - 2), (m + 1) * (m ^ 2 + m - 2), (m + 1) * (m ^ 2 + 3 * m), 2 * (m + 1) * (m - 1)]\n\n"
                "theorem calc_mv2_01_expand :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      (List.range 9).all (fun j => let x : Int := j - 4; zAlongX m x == zExpanded m x)) = true := by decide\n"
                "theorem calc_mv2_01_value :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      zxAt11 m == chainRule m && chainRule m == (m + 1) * (m ^ 2 + 3 * m - 2) && (options m).Nodup) = true := by\n"
                "  decide\n\n"
                "#eval chainRule 3\n"
            ),
            "python_code": '''import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', positive=True)
u = x + m * y
v = m * x - y
z = u**2 * v
zx = sp.diff(z, x).subs({x: 1, y: 1})
assert sp.expand(zx - (m + 1) * (m**2 + 3 * m - 2)) == 0, f'z_x mismatch: {sp.factor(zx)}'

U, V = sp.symbols('U V')
Z = U**2 * V
chain = (sp.diff(Z, U) * sp.diff(u, x) + sp.diff(Z, V) * sp.diff(v, x)).subs({U: u, V: v})
assert sp.expand(chain - sp.diff(z, x)) == 0

for mv in range(2, 10):
    opts = [(mv + 1) * (mv**2 + 3 * mv - 2), (mv + 1) * (mv**2 + mv - 2), (mv + 1) * (mv**2 + 3 * mv), 2 * (mv + 1) * (mv - 1)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
    h = 1e-6
    zf = lambda a, b: (a + mv * b)**2 * (mv * a - b)
    num = (zf(1 + h, 1) - zf(1 - h, 1)) / (2 * h)
    assert abs(num - opts[0]) < 1e-4 * opts[0]

print('VERIFIED_OK: CALC-MV2-01')
''',
        },
        # =====================================================================
        # CÂU 2: CALC-MV2-02 (MCQ - Vận dụng)
        # =====================================================================
        {
            "code": "CALC-MV2-02",
            "agent_id": 24,
            "agent_name": "Agent-24 (Giải tích: Hàm hợp, Hàm ẩn & Đạo hàm theo hướng)",
            "subject": "Giải tích",
            "topic": "Đạo hàm hàm hợp, hàm ẩn & đạo hàm theo hướng",
            "question_type": "mcq",
            "difficulty": "Vận dụng",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Đạo hàm của hàm ẩn xác định bởi phương trình chứa hàm mũ",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$. Hàm số $y = y(x)$ khả vi, xác định bởi phương trình "
                r"$$x e^{y} + y = m$$ và thỏa mãn $y(0) = m$. Giá trị $y'(0)$ bằng"
            ),
            "stem_template": (
                r"Hàm số $y = y(x)$ khả vi, xác định bởi phương trình $$x e^{y} + y = {m}$$ và thỏa mãn $y(0) = {m}$. "
                r"Tính $y'(0)$."
            ),
            "options_symbolic": {
                "A": r"$e^{m}$",
                "B": r"$-e^{m}$",
                "C": r"$-e^{-m}$",
                "D": r"$-m e^{m}$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "exp(m)",
                    "B": "-exp(m)",
                    "C": "-exp(-m)",
                    "D": "-m*exp(m)",
                },
                "target_expr": "-exp(m)",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"**Lời giải chi tiết:**" "\n\n"
                r"Đặt $F(x, y) = x e^{y} + y - m$. Ta có $F'_x = e^{y}$, $F'_y = x e^{y} + 1$. "
                r"Tại $(0, m)$: $F(0, m) = 0$ và $F'_y(0, m) = 1 \ne 0$, nên theo công thức đạo hàm hàm ẩn" "\n"
                r"$$y'(0) = -\frac{F'_x(0, m)}{F'_y(0, m)} = -\frac{e^{m}}{1} = -e^{m}.$$" "\n"
                r"Chọn đáp án **B**."
            ),
            "rubric_points": [
                "Đặt F(x, y) = x e^y + y - m và tính đúng F_x, F_y (0.4 điểm)",
                "Kiểm tra F(0, m) = 0 và F_y(0, m) = 1 khác 0 (0.2 điểm)",
                "Áp dụng y' = -F_x/F_y và kết luận y'(0) = -e^m (0.4 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MV2-02 (implicit differentiation)\n"
                "-- With E := e^y treated as a positive integer symbol: F_x = E, F_y = x * E + 1\n"
                "def Fval (m x y E : Int) : Int := x * E + y - m\n"
                "def Fy (x E : Int) : Int := x * E + 1\n\n"
                "theorem calc_mv2_02_point :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2;\n"
                "      (List.range 50).all (fun e => Fval m 0 m (e + 1) == 0)) = true := by decide\n"
                "theorem calc_mv2_02_nondegenerate :\n"
                "    (List.range 50).all (fun e => Fy 0 (e + 1) == 1) = true := by decide\n\n"
                "#eval Fy 0 20\n"
            ),
            "python_code": '''import math
import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', positive=True)
F = x * sp.exp(y) + y - m
assert sp.simplify(F.subs({x: 0, y: m})) == 0
yp = (-sp.diff(F, x) / sp.diff(F, y)).subs({x: 0, y: m})
assert sp.simplify(yp + sp.exp(m)) == 0, f'y prime mismatch: {yp}'
assert sp.simplify(sp.idiff(F, y, x).subs({x: 0, y: m}) + sp.exp(m)) == 0

def solve_y(xv, mv):
    yv = float(mv)
    for _ in range(100):
        g = xv * math.exp(yv) + yv - mv
        dg = xv * math.exp(yv) + 1
        yv -= g / dg
    return yv

for mv in range(2, 10):
    h = 1e-7
    num = (solve_y(h, mv) - solve_y(-h, mv)) / (2 * h)
    assert abs(num + math.exp(mv)) < 1e-3 * math.exp(mv), f'Numeric check failed at m={mv}'
    opts = [math.exp(mv), -math.exp(mv), -math.exp(-mv), -mv * math.exp(mv)]
    assert len(set(opts)) == 4

print('VERIFIED_OK: CALC-MV2-02')
''',
        },
        # =====================================================================
        # CÂU 3: CALC-MV2-03 (ESSAY - Vận dụng cao)
        # =====================================================================
        {
            "code": "CALC-MV2-03",
            "agent_id": 24,
            "agent_name": "Agent-24 (Giải tích: Hàm hợp, Hàm ẩn & Đạo hàm theo hướng)",
            "subject": "Giải tích",
            "topic": "Đạo hàm hàm hợp, hàm ẩn & đạo hàm theo hướng",
            "question_type": "essay",
            "difficulty": "Vận dụng cao",
            "has_parameters": True,
            "parameters_schema": _PARAM_M,
            "title": "Giới hạn hàm hai biến không tồn tại và đạo hàm theo hướng của hàm có tham số",
            "stem_symbolic": (
                r"Cho tham số nguyên dương $m \in [2, 9]$." "\n"
                r"a) Chứng minh rằng giới hạn $\displaystyle\lim_{(x, y) \to (0, 0)} \frac{m x y}{x^2 + y^2}$ không tồn tại." "\n"
                r"b) Cho $f(x, y) = x^2 y + m y^3$. Tính $\nabla f(1, 1)$." "\n"
                r"c) Tính đạo hàm theo hướng của $f$ tại $M(1, 1)$ theo hướng vector $\vec{\ell} = (3, 4)$."
            ),
            "stem_template": (
                r"a) Chứng minh rằng giới hạn $\displaystyle\lim_{(x, y) \to (0, 0)} \frac{{m} x y}{x^2 + y^2}$ không tồn tại." "\n"
                r"b) Cho $f(x, y) = x^2 y + {m} y^3$. Tính $\nabla f(1, 1)$." "\n"
                r"c) Tính đạo hàm theo hướng của $f$ tại $M(1, 1)$ theo hướng vector $\vec{\ell} = (3, 4)$."
            ),
            "options_symbolic": {},
            "parametric_formulas": {
                "options": {},
                "target_expr": "(12*m + 10)/5",
            },
            "correct_option": "ESSAY",
            "solution_symbolic": (
                r"**Lời giải chi tiết (Tự luận):**" "\n\n"
                r"**Ý a)** Cho $(x, y) \to (0, 0)$ dọc theo đường thẳng $y = kx$ ($x \ne 0$):" "\n"
                r"$$\frac{m x \cdot kx}{x^2 + k^2 x^2} = \frac{m k}{1 + k^2}.$$" "\n"
                r"Giá trị này phụ thuộc $k$: với $k = 0$ được $0$, với $k = 1$ được $\dfrac{m}{2} \ne 0$. "
                r"Hai đường khác nhau cho hai giới hạn khác nhau nên giới hạn không tồn tại." "\n\n"
                r"**Ý b)** $f'_x = 2xy$, $f'_y = x^2 + 3m y^2$, nên $\nabla f(1, 1) = (2,\ 1 + 3m)$." "\n\n"
                r"**Ý c)** Vector đơn vị cùng hướng $\vec{\ell}$ là $\vec{u} = \left(\dfrac{3}{5}, \dfrac{4}{5}\right)$. "
                r"Vì $f$ khả vi tại $M$:" "\n"
                r"$$\frac{\partial f}{\partial \vec{\ell}}(M) = \nabla f(M) \cdot \vec{u} = 2 \cdot \frac{3}{5} + (1 + 3m)\frac{4}{5} "
                r"= \frac{12m + 10}{5}.$$"
            ),
            "rubric_points": [
                "Chọn đường y = kx, tính giới hạn mk/(1 + k^2) và chỉ ra phụ thuộc k (0.3 điểm)",
                "Tính đúng các đạo hàm riêng và gradient (2, 1 + 3m) (0.3 điểm)",
                "Chuẩn hóa vector hướng thành (3/5, 4/5) (0.15 điểm)",
                "Tính đúng đạo hàm theo hướng (12m + 10)/5 (0.25 điểm)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MV2-03 (path-dependent limit & directional derivative)\n"
                "-- Along y = kx the expression equals m k / (1 + k^2): k = 0 gives 0, k = 1 gives m/2 (scaled by 2: m)\n"
                "def pathLimit2 (m k : Nat) : Nat := 2 * m * k / (1 + k ^ 2)\n"
                "def gradX : Int := 2\n"
                "def gradY (m : Int) : Int := 1 + 3 * m\n"
                "def dirDeriv5 (m : Int) : Int := 3 * gradX + 4 * gradY m\n\n"
                "theorem calc_mv2_03_paths :\n"
                "    (List.range 8).all (fun k => let m := k + 2; pathLimit2 m 0 != pathLimit2 m 1) = true := by decide\n"
                "theorem calc_mv2_03_direction :\n"
                "    (List.range 8).all (fun k => let m : Int := k + 2; dirDeriv5 m == 12 * m + 10) = true := by decide\n"
                "theorem calc_mv2_03_unit : 3 ^ 2 + 4 ^ 2 = 5 ^ 2 := by decide\n\n"
                "#eval dirDeriv5 3\n"
            ),
            "python_code": '''import sympy as sp

x, y, k = sp.symbols('x y k', real=True)
m = sp.symbols('m', positive=True)
g = m * x * y / (x**2 + y**2)
along = sp.simplify(g.subs(y, k * x))
assert sp.simplify(along - m * k / (1 + k**2)) == 0, f'Path value mismatch: {along}'
assert along.subs(k, 0) != along.subs(k, 1)

f = x**2 * y + m * y**3
grad = [sp.diff(f, x).subs({x: 1, y: 1}), sp.diff(f, y).subs({x: 1, y: 1})]
assert grad[0] == 2 and sp.simplify(grad[1] - (1 + 3 * m)) == 0
u = (sp.Rational(3, 5), sp.Rational(4, 5))
D = grad[0] * u[0] + grad[1] * u[1]
assert sp.simplify(D - (12 * m + 10) / 5) == 0

t = sp.symbols('t', real=True)
for mv in range(2, 10):
    ft = f.subs(m, mv).subs({x: 1 + t * u[0], y: 1 + t * u[1]})
    assert sp.simplify(sp.diff(ft, t).subs(t, 0) - sp.Rational(12 * mv + 10, 5)) == 0

print('VERIFIED_OK: CALC-MV2-03')
''',
        },
    ]
