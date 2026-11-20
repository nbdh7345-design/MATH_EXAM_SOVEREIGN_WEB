"""
Agent-06: Giải tích - Vi phân & Cực trị hàm nhiều biến
Sinh & kiểm chứng câu hỏi Đạo hàm riêng, Ma trận Hessian, Cực trị tự do hàm 2-3 biến phụ thuộc tham số.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 6,
    "agent_code": "AGENT-06",
    "agent_name": "Agent-06 (Giải tích: Vi phân & Cực trị hàm nhiều biến)",
    "domain": "Giải tích",
    "role_desc": "Sinh & kiểm chứng câu hỏi Đạo hàm riêng, Ma trận Hessian, Cực trị tự do hàm 2-3 biến phụ thuộc tham số",
}


def get_questions() -> list[dict]:
    return [
        {
            "code": "CALC-MUL-01",
            "agent_id": 6,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Đạo hàm riêng, Ma trận Hessian & Cực trị hàm nhiều biến",
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
            "title": "Cực trị tự do hàm hai biến và định thức Hessian tại điểm cực tiểu",
            "stem_symbolic": (
                r"Cho hàm số hai biến thực $f(x, y) = x^3 + y^3 - 3mxy + m^3$ với tham số nguyên $m \in [2, 9]$. "
                r"Gọi $M(x_0, y_0)$ là điểm cực tiểu địa phương của hàm số $f(x, y)$ và "
                r"$\Delta(x_0, y_0) = f''_{xx}(x_0, y_0)f''_{yy}(x_0, y_0) - \left[f''_{xy}(x_0, y_0)\right]^2$ "
                r"là định thức của ma trận Hessian tại $M$. Giá trị của biểu thức $P(m) = \Delta(x_0, y_0) + f(x_0, y_0)$ bằng:"
            ),
            "stem_template": (
                r"Cho hàm số hai biến thực $f(x, y) = x^3 + y^3 - 3\cdot {m}xy + {m}^3$ (với $m = {m}$). "
                r"Gọi $M(x_0, y_0)$ là điểm cực tiểu địa phương của hàm số $f(x, y)$ và "
                r"$\Delta(x_0, y_0) = f''_{{xx}}(x_0, y_0)f''_{{yy}}(x_0, y_0) - \left[f''_{{xy}}(x_0, y_0)\right]^2$ "
                r"là định thức của ma trận Hessian tại $M$. Giá trị của biểu thức $P({m}) = \Delta(x_0, y_0) + f(x_0, y_0)$ bằng:"
            ),
            "options_symbolic": {
                "A": r"$27m^2$",
                "B": r"$36m^2 + m^3$",
                "C": r"$9m^2 + m^3$",
                "D": r"$54m^2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "27*m**2",
                    "B": "36*m**2 + m**3",
                    "C": "9*m**2 + m**3",
                    "D": "54*m**2",
                },
                "target_expr": "27*m**2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Bước 1: Tìm các điểm dừng của hàm số.**" "\n"
                r"Ta tính các đạo hàm riêng cấp một:" "\n"
                r"$$\begin{cases} f'_x(x, y) = 3x^2 - 3my = 0 \\ f'_y(x, y) = 3y^2 - 3mx = 0 \end{cases} "
                r"\iff \begin{cases} y = \frac{x^2}{m} \\ x^4 - m^3 x = 0 \end{cases}$$" "\n"
                r"Do $m \in [2, 9]$, hệ phương trình có hai nghiệm thực (điểm dừng) là $O(0, 0)$ và $M(m, m)$." "\n\n"
                r"**Bước 2: Lập ma trận Hessian và phân loại điểm dừng.**" "\n"
                r"Các đạo hàm riêng cấp hai là: $A = f''_{xx} = 6x$, $B = f''_{xy} = -3m$, $C = f''_{yy} = 6y$." "\n"
                r"Định thức Hessian: $\Delta(x, y) = AC - B^2 = 36xy - 9m^2$." "\n"
                r"- Tại $O(0, 0)$: $\Delta(0, 0) = -9m^2 < 0$, nên $O(0, 0)$ là điểm yên ngựa (không phải cực trị)." "\n"
                r"- Tại $M(m, m)$: $\Delta(m, m) = 36m^2 - 9m^2 = 27m^2 > 0$ và $A = 6m > 0$ (vì $m \ge 2 > 0$). "
                r"Do đó $M(m, m)$ là điểm cực tiểu địa phương duy nhất của hàm số." "\n\n"
                r"**Bước 3: Tính giá trị biểu thức $P(m)$.**" "\n"
                r"Tại $M(m, m)$, giá trị cực tiểu là $f(m, m) = m^3 + m^3 - 3m(m)(m) + m^3 = 0$." "\n"
                r"Suy ra $P(m) = \Delta(m, m) + f(m, m) = 27m^2 + 0 = 27m^2$. Chọn đáp án **A**."
            ),
            "rubric_points": 1.0,
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MUL-01 (No Mathlib, No sorry)\n"
                "def f_val (m x y : Int) : Int :=\n"
                "  x^3 + y^3 - 3 * m * x * y + m^3\n\n"
                "def grad_x (m x y : Int) : Int :=\n"
                "  3 * x^2 - 3 * m * y\n\n"
                "def grad_y (m x y : Int) : Int :=\n"
                "  3 * y^2 - 3 * m * x\n\n"
                "def hessian_det (m x y : Int) : Int :=\n"
                "  (6 * x) * (6 * y) - (-3 * m)^2\n\n"
                "def target_P (m : Int) : Int :=\n"
                "  hessian_det m m m + f_val m m m\n\n"
                "theorem calc_mul_01_stationary_m3 : grad_x 3 3 3 = 0 ∧ grad_y 3 3 3 = 0 := by\n"
                "  decide\n\n"
                "theorem calc_mul_01_grid_check :\n"
                "    (List.range 8).all (fun k =>\n"
                "      let m : Int := Int.ofNat (k + 2)\n"
                "      grad_x m m m == 0 && grad_y m m m == 0 &&\n"
                "      hessian_det m m m > 0 && target_P m == 27 * m^2) = true := by\n"
                "  decide\n\n"
                "#eval (List.range 8).map (fun k => let m := Int.ofNat (k + 2); (m, target_P m))\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "x, y, m = sp.symbols('x y m', real=True)\n"
                "f = x**3 + y**3 - 3*m*x*y + m**3\n"
                "gx = sp.diff(f, x)\n"
                "gy = sp.diff(f, y)\n"
                "H = sp.hessian(f, (x, y))\n"
                "det_H = sp.simplify(H.det())\n\n"
                "for m_val in range(2, 10):\n"
                "    assert gx.subs({x: m_val, y: m_val, m: m_val}) == 0\n"
                "    assert gy.subs({x: m_val, y: m_val, m: m_val}) == 0\n"
                "    det_at_min = int(det_H.subs({x: m_val, y: m_val, m: m_val}))\n"
                "    f_xx_val = int(H[0, 0].subs({x: m_val, y: m_val, m: m_val}))\n"
                "    f_min_val = int(f.subs({x: m_val, y: m_val, m: m_val}))\n"
                "    assert det_at_min > 0 and f_xx_val > 0\n"
                "    assert det_at_min + f_min_val == 27 * (m_val ** 2)\n\n"
                "print('VERIFIED_OK: CALC-MUL-01 symbolic Hessian and grid m in [2..9] passed.')"
            ),
        },
        {
            "code": "CALC-MUL-02",
            "agent_id": 6,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Đạo hàm riêng, Ma trận Hessian & Cực trị hàm nhiều biến",
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
                    "label": "Tham số nguyên dương m",
                }
            },
            "title": "Đạo hàm riêng cấp một và cấp hai của hàm ba biến thuần nhất (Hệ thức Euler)",
            "stem_symbolic": (
                r"Cho hàm số ba biến $u(x, y, z) = m x^2 y + y^2 z + m z^2 x$ với tham số nguyên $m \in [2, 9]$. "
                r"Xét biểu thức vi phân kết hợp đạo hàm riêng cấp một và vết của ma trận Hessian: "
                r"$$S(x, y, z) = \left(x u'_x + y u'_y + z u'_z\right) + \frac{1}{2}\operatorname{Tr}\left(H_u(x, y, z)\right)$$"
                r"với $\operatorname{Tr}\left(H_u\right) = u''_{xx} + u''_{yy} + u''_{zz}$. Giá trị của $S(1, 1, 1)$ theo tham số $m$ bằng:"
            ),
            "stem_template": (
                r"Cho hàm số ba biến $u(x, y, z) = {m} x^2 y + y^2 z + {m} z^2 x$ (với $m = {m}$). "
                r"Xét biểu thức vi phân kết hợp đạo hàm riêng cấp một và vết của ma trận Hessian: "
                r"$$S(x, y, z) = \left(x u'_x + y u'_y + z u'_z\right) + \frac{{1}}{{2}}\operatorname{{Tr}}\left(H_u(x, y, z)\right)$$"
                r"với $\operatorname{{Tr}}\left(H_u\right) = u''_{{xx}} + u''_{{yy}} + u''_{{zz}}$. Giá trị của $S(1, 1, 1)$ bằng:"
            ),
            "options_symbolic": {
                "A": r"$8m + 4$",
                "B": r"$6m + 3$",
                "C": r"$10m + 5$",
                "D": r"$8m + 2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "8*m + 4",
                    "B": "6*m + 3",
                    "C": "10*m + 5",
                    "D": "8*m + 2",
                },
                "target_expr": "8*m + 4",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Bước 1: Tính tổ hợp đạo hàm riêng cấp một bằng định lý Euler (hoặc tính trực tiếp).**" "\n"
                r"Ta có các đạo hàm riêng cấp một:" "\n"
                r"$$u'_x = 2mxy + mz^2, \quad u'_y = mx^2 + 2yz, \quad u'_z = y^2 + 2mzx$$" "\n"
                r"Vì $u(x, y, z)$ là hàm thuần nhất bậc $k = 3$, theo định lý Euler ta có:" "\n"
                r"$$x u'_x + y u'_y + z u'_z = 3u(x, y, z)$$" "\n"
                r"Tại điểm $P(1, 1, 1)$: $u(1, 1, 1) = m + 1 + m = 2m + 1$, suy ra $\left(x u'_x + y u'_y + z u'_z\right)\big|_{(1,1,1)} = 3(2m + 1) = 6m + 3$." "\n\n"
                r"**Bước 2: Tính vết ma trận Hessian $\operatorname{Tr}(H_u(1, 1, 1))$.**" "\n"
                r"Các đạo hàm riêng cấp hai trên đường chéo chính của ma trận Hessian $H_u$ là:" "\n"
                r"$$u''_{xx} = 2my, \quad u''_{yy} = 2z, \quad u''_{zz} = 2mx$$" "\n"
                r"Tại điểm $P(1, 1, 1)$, ta có:" "\n"
                r"$$\operatorname{Tr}(H_u(1, 1, 1)) = 2m(1) + 2(1) + 2m(1) = 4m + 2 \implies \frac{1}{2}\operatorname{Tr}(H_u(1, 1, 1)) = 2m + 1$$" "\n\n"
                r"**Bước 3: Tổng hợp giá trị $S(1, 1, 1)$.**" "\n"
                r"$$S(1, 1, 1) = (6m + 3) + (2m + 1) = 8m + 4$$" "\n"
                r"Chọn đáp án **A**."
            ),
            "rubric_points": 1.0,
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MUL-02 (No Mathlib, No sorry)\n"
                "def u_val (m x y z : Int) : Int :=\n"
                "  m * x^2 * y + y^2 * z + m * z^2 * x\n\n"
                "def ux (m x y z : Int) : Int := 2 * m * x * y + m * z^2\n"
                "def uy (m x y z : Int) : Int := m * x^2 + 2 * y * z\n"
                "def uz (m x y z : Int) : Int := y^2 + 2 * m * z * x\n\n"
                "def uxx (m _ y _ : Int) : Int := 2 * m * y\n"
                "def uyy (_ _ _ z : Int) : Int := 2 * z\n"
                "def uzz (m x _ _ : Int) : Int := 2 * m * x\n\n"
                "def S_at_111 (m : Int) : Int :=\n"
                "  let euler_part := 1 * ux m 1 1 1 + 1 * uy m 1 1 1 + 1 * uz m 1 1 1\n"
                "  let half_trace := (uxx m 1 1 1 + uyy m 1 1 1 + uzz m 1 1 1) / 2\n"
                "  euler_part + half_trace\n\n"
                "theorem calc_mul_02_euler_identity :\n"
                "    (List.range 10).all (fun k => let m := Int.ofNat (k + 1); ux m 1 1 1 + uy m 1 1 1 + uz m 1 1 1 == 3 * u_val m 1 1 1) = true := by\n"
                "  decide\n\n"
                "theorem calc_mul_02_grid_check :\n"
                "    (List.range 8).all (fun k =>\n"
                "      let m : Int := Int.ofNat (k + 2)\n"
                "      S_at_111 m == 8 * m + 4) = true := by\n"
                "  decide\n\n"
                "#eval (List.range 8).map (fun k => let m := Int.ofNat (k + 2); (m, S_at_111 m))\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "x, y, z, m = sp.symbols('x y z m', real=True)\n"
                "u = m * x**2 * y + y**2 * z + m * z**2 * x\n"
                "H = sp.hessian(u, (x, y, z))\n"
                "euler_expr = x * sp.diff(u, x) + y * sp.diff(u, y) + z * sp.diff(u, z)\n"
                "assert sp.simplify(euler_expr - 3 * u) == 0\n"
                "S_expr = sp.simplify(euler_expr + sp.Rational(1, 2) * H.trace())\n"
                "S_111 = sp.simplify(S_expr.subs({x: 1, y: 1, z: 1}))\n"
                "assert sp.simplify(S_111 - (8 * m + 4)) == 0\n\n"
                "for m_val in range(2, 10):\n"
                "    val = int(S_111.subs(m, m_val))\n"
                "    assert val == 8 * m_val + 4\n\n"
                "print('VERIFIED_OK: CALC-MUL-02 Euler partial derivatives & Hessian trace passed.')"
            ),
        },
        {
            "code": "CALC-MUL-03",
            "agent_id": 6,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Giải tích",
            "topic": "Đạo hàm riêng, Ma trận Hessian & Cực trị hàm nhiều biến",
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
            "title": "Cực trị toàn cục hàm ba biến và kiểm định xác định dương Sylvester của ma trận Hessian",
            "stem_symbolic": (
                r"Cho hàm số ba biến thực $f(x, y, z) = x^2 + 2y^2 + 2z^2 + 2xy + 2xz + 2yz - 2mx - 6my + 7m^2$ "
                r"với tham số nguyên $m \in [2, 9]$." "\n"
                r"1) Giải hệ phương trình $\nabla f(x, y, z) = \mathbf{0}$ để tìm tọa độ điểm dừng duy nhất $P_0(x_0, y_0, z_0)$ theo $m$." "\n"
                r"2) Lập ma trận Hessian $H_f(x, y, z)$ và tính các định thức con chính dẫn đầu $D_1, D_2, D_3$ theo tiêu chuẩn Sylvester để chứng minh $f$ đạt cực tiểu toàn cục chặt tại $P_0$." "\n"
                r"3) Tính giá trị cực tiểu $f_{\min}(m) = f(x_0, y_0, z_0)$ và tổng $Q(m) = f_{\min}(m) + D_1 + D_2 + D_3$."
            ),
            "stem_template": (
                r"Cho hàm số ba biến thực $f(x, y, z) = x^2 + 2y^2 + 2z^2 + 2xy + 2xz + 2yz - 2\cdot {m}x - 6\cdot {m}y + 7\cdot {m}^2$ "
                r"(với tham số $m = {m}$)." "\n"
                r"1) Giải hệ phương trình $\nabla f(x, y, z) = \mathbf{{0}}$ để tìm tọa độ điểm dừng duy nhất $P_0(x_0, y_0, z_0)$." "\n"
                r"2) Lập ma trận Hessian $H_f(x, y, z)$ và tính các định thức con chính dẫn đầu $D_1, D_2, D_3$ theo tiêu chuẩn Sylvester để chứng minh $f$ đạt cực tiểu toàn cục chặt tại $P_0$." "\n"
                r"3) Tính giá trị cực tiểu $f_{{\min}}({m}) = f(x_0, y_0, z_0)$ và tổng $Q({m}) = f_{{\min}}({m}) + D_1 + D_2 + D_3$."
            ),
            "options_symbolic": {
                "A": r"$Q(m) = m^2 + 14$ với $P_0(0, 2m, -m)$ và $f_{\min}(m) = m^2$",
                "B": r"$Q(m) = 2m^2 + 14$ với $P_0(m, 2m, -m)$ và $f_{\min}(m) = 2m^2$",
                "C": r"$Q(m) = m^2 + 8$ với $P_0(0, m, -m)$ và $f_{\min}(m) = m^2$",
                "D": r"$Q(m) = 7m^2 + 14$ với $P_0(0, 0, 0)$ và $f_{\min}(m) = 7m^2$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2 + 14",
                    "B": "2*m**2 + 14",
                    "C": "m**2 + 8",
                    "D": "7*m**2 + 14",
                },
                "target_expr": "m**2 + 14",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**Phần 1: Tìm điểm dừng duy nhất $P_0(x_0, y_0, z_0)$.**" "\n"
                r"Tính các đạo hàm riêng cấp một của $f(x, y, z)$:" "\n"
                r"$$\begin{cases} "
                r"f'_x = 2x + 2y + 2z - 2m = 0 \\ "
                r"f'_y = 2x + 4y + 2z - 6m = 0 \\ "
                r"f'_z = 2x + 2y + 4z = 0 "
                r"\end{cases} \iff \begin{cases} "
                r"x + y + z = m \quad (1) \\ "
                r"x + 2y + z = 3m \quad (2) \\ "
                r"x + y + 2z = 0 \quad (3) "
                r"\end{cases}$$" "\n"
                r"Lấy $(2) - (1)$ ta được $y = 2m$. Lấy $(3) - (1)$ ta được $z = -m$. "
                r"Thay vào $(1)$ suy ra $x = m - 2m - (-m) = 0$. "
                r"Vậy hàm số có điểm dừng duy nhất là $P_0(0, 2m, -m)$." "\n\n"
                r"**Phần 2: Lập ma trận Hessian và kiểm định Sylvester.**" "\n"
                r"Ma trận Hessian cấp $3 \times 3$ của hàm số (hằng số tại mọi $(x, y, z) \in \mathbb{R}^3$) là:" "\n"
                r"$$H_f(x, y, z) = \begin{pmatrix} 2 & 2 & 2 \\ 2 & 4 & 2 \\ 2 & 2 & 4 \end{pmatrix}$$" "\n"
                r"Các định thức con chính dẫn đầu theo tiêu chuẩn Sylvester:" "\n"
                r"- $D_1 = 2 > 0$" "\n"
                r"- $D_2 = \det \begin{pmatrix} 2 & 2 \\ 2 & 4 \end{pmatrix} = 8 - 4 = 4 > 0$" "\n"
                r"- $D_3 = \det H_f = 2(16 - 4) - 2(8 - 4) + 2(4 - 8) = 24 - 8 - 8 = 8 > 0$" "\n"
                r"Vì $D_1 > 0, D_2 > 0, D_3 > 0$, ma trận $H_f$ xác định dương trên toàn không gian $\mathbb{R}^3$. "
                r"Do đó $f(x, y, z)$ là hàm lồi chặt và đạt cực tiểu toàn cục duy nhất tại $P_0(0, 2m, -m)$." "\n\n"
                r"**Phần 3: Tính giá trị cực tiểu $f_{\min}(m)$ và biểu thức $Q(m)$.**" "\n"
                r"Ta có thể phân tích dạng bình phương toàn phần:" "\n"
                r"$$f(x, y, z) = (x + y + z - m)^2 + (y - 2m)^2 + (z + m)^2 + m^2 \ge m^2, \quad \forall (x, y, z) \in \mathbb{R}^3$$" "\n"
                r"Đẳng thức xảy ra khi và chỉ khi $(x, y, z) = (0, 2m, -m)$, nên $f_{\min}(m) = m^2$." "\n"
                r"Tổng cần tìm là: $Q(m) = f_{\min}(m) + D_1 + D_2 + D_3 = m^2 + (2 + 4 + 8) = m^2 + 14$."
            ),
            "rubric_points": 2.0,
            "lean4_code": (
                "-- Lean 4 Core verification for CALC-MUL-03 (No Mathlib, No sorry)\n"
                "def f3_val (m x y z : Int) : Int :=\n"
                "  x^2 + 2*y^2 + 2*z^2 + 2*x*y + 2*x*z + 2*y*z - 2*m*x - 6*m*y + 7*m^2\n\n"
                "def f3_sos (m x y z : Int) : Int :=\n"
                "  (x + y + z - m)^2 + (y - 2*m)^2 + (z + m)^2 + m^2\n\n"
                "def D1 : Int := 2\n"
                "def D2 : Int := 2 * 4 - 2 * 2\n"
                "def D3 : Int := 2 * (4 * 4 - 2 * 2) - 2 * (2 * 4 - 2 * 2) + 2 * (2 * 2 - 4 * 2)\n\n"
                "theorem sylvester_positive_definite : D1 = 2 ∧ D2 = 4 ∧ D3 = 8 ∧ D1 > 0 ∧ D2 > 0 ∧ D3 > 0 := by\n"
                "  decide\n\n"
                "theorem calc_mul_03_grid_check :\n"
                "    (List.range 8).all (fun k =>\n"
                "      let m : Int := Int.ofNat (k + 2)\n"
                "      let x0 : Int := 0\n"
                "      let y0 : Int := 2 * m\n"
                "      let z0 : Int := -m\n"
                "      f3_val m x0 y0 z0 == m^2 &&\n"
                "      f3_sos m x0 y0 z0 == m^2 &&\n"
                "      (f3_val m x0 y0 z0 + D1 + D2 + D3) == m^2 + 14) = true := by\n"
                "  decide\n\n"
                "#eval (List.range 8).map (fun k => let m := Int.ofNat (k + 2); (m, f3_val m 0 (2*m) (-m) + D1 + D2 + D3))\n"
            ),
            "python_code": (
                "import sympy as sp\n\n"
                "x, y, z, m = sp.symbols('x y z m', real=True)\n"
                "f = x**2 + 2*y**2 + 2*z**2 + 2*x*y + 2*x*z + 2*y*z - 2*m*x - 6*m*y + 7*m**2\n"
                "sos = (x + y + z - m)**2 + (y - 2*m)**2 + (z + m)**2 + m**2\n"
                "assert sp.expand(f - sos) == 0\n\n"
                "grad = [sp.diff(f, v) for v in (x, y, z)]\n"
                "sol = sp.solve(grad, (x, y, z))\n"
                "assert sol[x] == 0 and sol[y] == 2*m and sol[z] == -m\n\n"
                "H = sp.hessian(f, (x, y, z))\n"
                "D1 = int(H[:1, :1].det())\n"
                "D2 = int(H[:2, :2].det())\n"
                "D3 = int(H.det())\n"
                "assert (D1, D2, D3) == (2, 4, 8)\n\n"
                "for m_val in range(2, 10):\n"
                "    f_min = int(f.subs({x: 0, y: 2*m_val, z: -m_val, m: m_val}))\n"
                "    assert f_min == m_val**2\n"
                "    assert f_min + D1 + D2 + D3 == m_val**2 + 14\n\n"
                "print('VERIFIED_OK: CALC-MUL-03 3D Sylvester Hessian & global minimum passed.')"
            ),
        },
    ]
