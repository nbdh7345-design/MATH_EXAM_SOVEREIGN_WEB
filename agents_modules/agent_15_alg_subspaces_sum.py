"""
Agent-15: Đại số — Không gian vector con, Giao & Tổng Grassmann
Sinh & kiểm chứng câu hỏi Không gian vector con, Bao tuyến tính span,
Công thức chiều Grassmann dim(U+W) có tham số m.
"""

from __future__ import annotations

AGENT_META = {
    "agent_id": 15,
    "agent_code": "AGENT-15",
    "agent_name": "Agent-15 (Đại số: Không gian con, Giao & Tổng Grassmann)",
    "domain": "Đại số",
    "role_desc": "Sinh & kiểm chứng câu hỏi Không gian vector con, Bao tuyến tính span, Công thức chiều Grassmann dim(U+W) có tham số",
}


def get_questions() -> list[dict]:
    """Trả về danh sách 3 câu hỏi chuẩn Sovereign (2 MCQ, 1 Essay) có tham số m."""
    return [
        {
            "code": "ALG-SUB-01",
            "agent_id": 15,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian vector con, Giao & Tổng trực tiếp Grassmann",
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
                    "description": "Tham số nguyên dương m trong tọa độ cơ sở và siêu phẳng",
                }
            },
            "title": "Công thức chiều Grassmann cho giao và tổng hai không gian vector con",
            "stem_symbolic": (
                r"Trong không gian vector $\mathbb{R}^4$, xét không gian con "
                r"$U = \operatorname{span}\{u_1, u_2, u_3\}$ với "
                r"$u_1 = (1, 0, m, 1)$, $u_2 = (0, 1, 1, m)$, $u_3 = (1, 1, m+1, m+1)$ "
                r"(với $m \ge 2$ là tham số nguyên) và siêu phẳng "
                r"$W = \{(x_1, x_2, x_3, x_4) \in \mathbb{R}^4 \mid m x_1 + x_2 - x_3 = 0\}$. "
                r"Đặt $T(m) = m \cdot \dim(U + W) + \dim(U \cap W)$. Khẳng định nào sau đây đúng?"
            ),
            "stem_template": (
                r"Trong không gian vector $\mathbb{R}^4$, xét không gian con "
                r"$U = \operatorname{span}\{u_1, u_2, u_3\}$ với "
                r"$u_1 = (1, 0, {m}, 1)$, $u_2 = (0, 1, 1, {m})$, $u_3 = (1, 1, {m}+1, {m}+1)$ "
                r"và siêu phẳng "
                r"$W = \{(x_1, x_2, x_3, x_4) \in \mathbb{R}^4 \mid {m} x_1 + x_2 - x_3 = 0\}$. "
                r"Giá trị của biểu thức $T({m}) = {m} \cdot \dim(U + W) + \dim(U \cap W)$ bằng:"
            ),
            "options_symbolic": {
                "A": r"$3m + 2$",
                "B": r"$4m + 1$",
                "C": r"$3m + 1$",
                "D": r"$2m + 3$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "3*m + 2",
                    "B": "4*m + 1",
                    "C": "3*m + 1",
                    "D": "2*m + 3",
                },
                "target_expr": "3*m + 2",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"Ta nhận thấy $u_3 = u_1 + u_2$, trong khi hai vector $u_1 = (1, 0, m, 1)$ và "
                r"$u_2 = (0, 1, 1, m)$ độc lập tuyến tính với mọi $m$, nên $\dim(U) = 2$. "
                r"Không gian $W$ được xác định bởi một phương trình tuyến tính thuần nhất không suy biến "
                r"$m x_1 + x_2 - x_3 = 0$ trong $\mathbb{R}^4$, suy ra $\dim(W) = 4 - 1 = 3$ "
                r"(số ẩn tự do bằng $\dim(\operatorname{nullspace}(A_W)) = 3$). "
                r"Thay tọa độ $u_1, u_2$ vào phương trình của $W$: "
                r"$m(1) + 0 - m = 0$ và $m(0) + 1 - 1 = 0$, nên $u_1, u_2 \in W \implies U \subset W$. "
                r"Do đó $U \cap W = U \implies \dim(U \cap W) = 2$. "
                r"Áp dụng công thức chiều Grassmann: "
                r"$\dim(U + W) = \dim(U) + \dim(W) - \dim(U \cap W) = 2 + 3 - 2 = 3$. "
                r"Vậy $T(m) = m \cdot \dim(U + W) + \dim(U \cap W) = 3m + 2$."
            ),
            "rubric_points": [
                "Xác định hạng của họ vector sinh U bằng biến đổi sơ cấp RREF: dim(U) = 2 (0.25đ)",
                "Sử dụng định lý hạng - số khuyết (nullspace) suy ra dim(W) = 4 - 1 = 3 (0.25đ)",
                "Kiểm tra điều kiện thuộc W của cơ sở U suy ra dim(U ∩ W) = 2 (0.25đ)",
                "Áp dụng công thức Grassmann dim(U+W) = dim(U)+dim(W)-dim(U∩W) = 3 và tính T(m) = 3m + 2 (0.25đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-SUB-01: Grassmann dimension formula\n"
                "def dimU : Nat := 2\n"
                "def dimW : Nat := 3\n"
                "def dimInter : Nat := 2\n"
                "def dimSum : Nat := dimU + dimW - dimInter\n\n"
                "def targetExpr (m : Nat) : Nat := m * dimSum + dimInter\n\n"
                "theorem grassmann_identity : dimU + dimW = dimSum + dimInter := by decide\n\n"
                "theorem alg_sub_01_formula (m : Nat) : targetExpr m = 3 * m + 2 := by\n"
                "  unfold targetExpr dimSum dimU dimW dimInter\n"
                "  omega\n\n"
                "theorem alg_sub_01_m3 : targetExpr 3 = 11 := by rfl\n\n"
                "#eval targetExpr 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "def verify_alg_sub_01():\n"
                "    for m_val in range(2, 10):\n"
                "        u1 = [1, 0, m_val, 1]\n"
                "        u2 = [0, 1, 1, m_val]\n"
                "        u3 = [1, 1, m_val + 1, m_val + 1]\n"
                "        M_U = sp.Matrix([u1, u2, u3])\n"
                "        rref_U, pivots_U = M_U.rref()\n"
                "        dim_U = len(pivots_U)\n"
                "        assert dim_U == 2\n\n"
                "        A_W = sp.Matrix([[m_val, 1, -1, 0]])\n"
                "        null_W = A_W.nullspace()\n"
                "        dim_W = len(null_W)\n"
                "        assert dim_W == 3\n\n"
                "        basis_W = [list(v) for v in null_W]\n"
                "        M_sum = sp.Matrix([u1, u2] + basis_W)\n"
                "        _, pivots_sum = M_sum.rref()\n"
                "        dim_sum = len(pivots_sum)\n"
                "        dim_inter = dim_U + dim_W - dim_sum\n\n"
                "        np_rank_sum = np.linalg.matrix_rank(np.array([u1, u2] + basis_W, dtype=float))\n"
                "        assert dim_sum == int(np_rank_sum) == 3\n"
                "        assert dim_inter == 2\n"
                "        val = m_val * dim_sum + dim_inter\n"
                "        assert val == 3 * m_val + 2\n"
                "    print('VERIFIED_OK: ALG-SUB-01 Grassmann dimensions verified across m=2..9')\n\n"
                "if __name__ == '__main__':\n"
                "    verify_alg_sub_01()\n"
            ),
        },
        {
            "code": "ALG-SUB-02",
            "agent_id": 15,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian vector con, Giao & Tổng trực tiếp Grassmann",
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
                    "description": "Tham số nguyên dương m trong bao tuyến tính span",
                }
            },
            "title": "Điều kiện vector thuộc bao tuyến tính span và bảo toàn chiều không gian con",
            "stem_symbolic": (
                r"Trong không gian vector $\mathbb{R}^4$, cho không gian con "
                r"$U = \operatorname{span}\{v_1, v_2, v_3\}$ với "
                r"$v_1 = (1, 2, m, 1)$, $v_2 = (2, 5, 2m+1, 3)$, $v_3 = (3, 7, 3m+1, 4)$ "
                r"(với $m \ge 2$ là tham số nguyên). Xét vector $w = (1, 3, m+1, k - m^2)$. "
                r"Tìm giá trị của $k$ theo $m$ để $w \in U$ (tức là $\dim(\operatorname{span}\{v_1, v_2, v_3, w\}) = \dim(U)$)."
            ),
            "stem_template": (
                r"Trong không gian vector $\mathbb{R}^4$, cho không gian con "
                r"$U = \operatorname{span}\{v_1, v_2, v_3\}$ với "
                r"$v_1 = (1, 2, {m}, 1)$, $v_2 = (2, 5, 2\cdot{m}+1, 3)$, $v_3 = (3, 7, 3\cdot{m}+1, 4)$. "
                r"Xét vector $w = (1, 3, {m}+1, k - {m}^2)$. "
                r"Giá trị của $k$ để $w \in U$ bằng:"
            ),
            "options_symbolic": {
                "A": r"$m^2 + 1$",
                "B": r"$m^2 + 2$",
                "C": r"$m^2 - 2$",
                "D": r"$2m^2 + 1$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2 + 1",
                    "B": "m**2 + 2",
                    "C": "m**2 - 2",
                    "D": "2*m**2 + 1",
                },
                "target_expr": "m**2 + 2",
            },
            "correct_option": "B",
            "solution_symbolic": (
                r"Ta có $v_3 = v_1 + v_2$ và $\{v_1, v_2\}$ độc lập tuyến tính nên $U = \operatorname{span}\{v_1, v_2\}$ "
                r"có $\dim(U) = 2$. "
                r"Để $w \in U$, phải tồn tại các số thực $\alpha, \beta$ sao cho $w = \alpha v_1 + \beta v_2$. "
                r"Xét 2 tọa độ đầu: $\alpha + 2\beta = 1$ và $2\alpha + 5\beta = 3 \implies \alpha = -1, \beta = 1$. "
                r"Kiểm tra tọa độ thứ 3: $-m + (2m + 1) = m + 1$ (luôn thỏa mãn với mọi $m$). "
                r"Xét tọa độ thứ 4: $k - m^2 = \alpha(1) + \beta(3) = -1 + 3 = 2 \iff k = m^2 + 2$."
            ),
            "rubric_points": [
                "Rút gọn hệ sinh của U về cơ sở {v1, v2} bằng phép khử Gauss RREF (0.25đ)",
                "Thiết lập hệ phương trình tổ hợp tuyến tính w = alpha*v1 + beta*v2 (0.25đ)",
                "Giải hệ tìm duy nhất bộ hệ số alpha = -1, beta = 1 (0.25đ)",
                "Đồng nhất tọa độ thứ tư k - m^2 = 2 suy ra k = m^2 + 2 (0.25đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-SUB-02: Linear span membership\n"
                "def v1 (m : Int) : Int × Int × Int × Int := (1, 2, m, 1)\n"
                "def v2 (m : Int) : Int × Int × Int × Int := (2, 5, 2 * m + 1, 3)\n"
                "def kTarget (m : Int) : Int := m * m + 2\n\n"
                "theorem span_fourth_coord (m : Int) : kTarget m - m * m = -1 * 1 + 1 * 3 := by\n"
                "  unfold kTarget\n"
                "  omega\n\n"
                "theorem alg_sub_02_m3 : kTarget 3 = 11 := by rfl\n\n"
                "#eval kTarget 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "def verify_alg_sub_02():\n"
                "    m, k = sp.symbols('m k')\n"
                "    for m_val in range(2, 10):\n"
                "        v1 = [1, 2, m_val, 1]\n"
                "        v2 = [2, 5, 2 * m_val + 1, 3]\n"
                "        v3 = [3, 7, 3 * m_val + 1, 4]\n"
                "        k_good = m_val**2 + 2\n"
                "        w_good = [1, 3, m_val + 1, k_good - m_val**2]\n"
                "        M_good = sp.Matrix([v1, v2, v3, w_good])\n"
                "        _, pivots_good = M_good.rref()\n"
                "        assert len(pivots_good) == 2\n\n"
                "        # Nullspace of transpose confirms linear dependence\n"
                "        ns = M_good.T.nullspace()\n"
                "        assert len(ns) == 2\n\n"
                "        # Distractor check\n"
                "        w_bad = [1, 3, m_val + 1, (m_val**2 + 1) - m_val**2]\n"
                "        np_rank_bad = np.linalg.matrix_rank(np.array([v1, v2, v3, w_bad], dtype=float))\n"
                "        assert int(np_rank_bad) == 3\n"
                "    print('VERIFIED_OK: ALG-SUB-02 span condition verified across m=2..9')\n\n"
                "if __name__ == '__main__':\n"
                "    verify_alg_sub_02()\n"
            ),
        },
        {
            "code": "ALG-SUB-03",
            "agent_id": 15,
            "agent_name": AGENT_META["agent_name"],
            "subject": "Đại số",
            "topic": "Không gian vector con, Giao & Tổng trực tiếp Grassmann",
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
                    "description": "Tham số nguyên dương m trong hệ cơ sở và phương trình không gian con",
                }
            },
            "title": "Xác định cơ sở của giao U ∩ W, tổng U + W và phần bù tổng trực tiếp trong R^4",
            "stem_symbolic": (
                r"Trong không gian vector $\mathbb{R}^4$, cho hai không gian vector con phụ thuộc tham số nguyên $m \ge 2$:"
                "\n"
                r"$$U = \operatorname{span}\{u_1 = (1, 0, m, 0), \, u_2 = (0, 1, 0, m)\}$$"
                "\n"
                r"$$W = \{(x_1, x_2, x_3, x_4) \in \mathbb{R}^4 \mid m x_1 - x_3 + x_4 = 0, \, x_4 = 0\}$$"
                "\n"
                r"a) Tìm số chiều và một cơ sở chuẩn tắc (có tọa độ đầu bằng 1) $b_{\cap}$ của không gian giao $U \cap W$.\n"
                r"b) Tính $\dim(U + W)$ theo công thức Grassmann và tìm một không gian con $Z \subset \mathbb{R}^4$ sao cho $(U + W) \oplus Z = \mathbb{R}^4$.\n"
                r"c) Tính chỉ số bất biến $I(m) = \|b_{\cap}\|_2^2 + \dim(U + W)$ theo $m$."
            ),
            "stem_template": (
                r"Trong không gian vector $\mathbb{R}^4$, cho hai không gian vector con (với $m = {m}$):"
                "\n"
                r"$$U = \operatorname{span}\{{u_1 = (1, 0, {m}, 0), \, u_2 = (0, 1, 0, {m})\}}$$"
                "\n"
                r"$$W = \{{(x_1, x_2, x_3, x_4) \in \mathbb{R}^4 \mid {m} x_1 - x_3 + x_4 = 0, \, x_4 = 0\}}$$"
                "\n"
                r"a) Tìm số chiều và vector cơ sở $b_{\cap}$ (có tọa độ thứ nhất bằng 1) của $U \cap W$.\n"
                r"b) Tính $\dim(U + W)$ theo công thức Grassmann và chỉ ra một không gian con $Z$ sao cho $(U + W) \oplus Z = \mathbb{R}^4$.\n"
                r"c) Tính giá trị chỉ số $I({m}) = \|b_{\cap}\|_2^2 + \dim(U + W)$."
            ),
            "options_symbolic": {
                "A": r"$m^2 + 4$",
                "B": r"$m^2 + 3$",
                "C": r"$2m^2 + 3$",
                "D": r"$m^2 + 5$",
            },
            "parametric_formulas": {
                "options": {
                    "A": "m**2 + 4",
                    "B": "m**2 + 3",
                    "C": "2*m**2 + 3",
                    "D": "m**2 + 5",
                },
                "target_expr": "m**2 + 4",
            },
            "correct_option": "A",
            "solution_symbolic": (
                r"**a) Cơ sở và số chiều của $U \cap W$:**"
                "\n"
                r"Mọi vector $u \in U$ có dạng $u = a u_1 + b u_2 = (a, b, m a, m b)$ với $a, b \in \mathbb{R}$. "
                r"Thay vào hệ phương trình xác định $W$: "
                r"$\begin{cases} m a - m a + m b = 0 \\ m b = 0 \end{cases} \iff b = 0$ (do $m \ge 2 \ne 0$). "
                r"Suy ra $u = a(1, 0, m, 0)$. Vậy $\dim(U \cap W) = 1$ và vector cơ sở chuẩn hóa là $b_{\cap} = (1, 0, m, 0)$."
                "\n\n"
                r"**b) Công thức chiều Grassmann và tổng trực tiếp:**"
                "\n"
                r"Hệ phương trình của $W$ tương đương $x_3 = m x_1, x_4 = 0$, nên $\dim(W) = 4 - 2 = 2$ với cơ sở "
                r"$w_1 = (1, 0, m, 0), w_2 = (0, 1, 0, 0)$. Vì $\dim(U) = 2$, theo định lý Grassmann: "
                r"$$\dim(U + W) = \dim(U) + \dim(W) - \dim(U \cap W) = 2 + 2 - 1 = 3.$$"
                r"Một cơ sở của $U + W$ là $\{u_1 = (1,0,m,0), u_2 = (0,1,0,m), w_2 = (0,1,0,0)\}$. "
                r"Chọn $Z = \operatorname{span}\{e_3 = (0,0,1,0)\}$, ta có $\det[u_1, u_2, w_2, e_3] = -m \ne 0$, "
                r"nên $(U + W) \oplus Z = \mathbb{R}^4$."
                "\n\n"
                r"**c) Tính chỉ số $I(m)$:**"
                "\n"
                r"Ta có $\|b_{\cap}\|_2^2 = 1^2 + 0^2 + m^2 + 0^2 = m^2 + 1$. "
                r"Do đó $I(m) = (m^2 + 1) + 3 = m^2 + 4$."
            ),
            "rubric_points": [
                "Biểu diễn tổng quát u in U và giải hệ điều kiện u in W tìm được dim(U ∩ W) = 1, b_cap = (1, 0, m, 0) (0.35đ)",
                "Tìm cơ sở không gian nghiệm W (nullspace) suy ra dim(W) = 2 và áp dụng công thức Grassmann dim(U+W) = 3 (0.35đ)",
                "Xác định đúng không gian bù trực tiếp Z = span{(0,0,1,0)} và tính đúng I(m) = m^2 + 4 (0.30đ)",
            ],
            "lean4_code": (
                "-- Lean 4 Core verification for ALG-SUB-03: Direct sum & Grassmann essay\n"
                "def normSqBcap (m : Nat) : Nat := 1 + 0 + m * m + 0\n"
                "def dimU_03 : Nat := 2\n"
                "def dimW_03 : Nat := 2\n"
                "def dimInter_03 : Nat := 1\n"
                "def dimSum_03 : Nat := dimU_03 + dimW_03 - dimInter_03\n\n"
                "def indexI (m : Nat) : Nat := normSqBcap m + dimSum_03\n\n"
                "theorem direct_sum_complement : dimSum_03 + 1 = 4 := by decide\n\n"
                "theorem alg_sub_03_formula (m : Nat) : indexI m = m * m + 4 := by\n"
                "  unfold indexI normSqBcap dimSum_03 dimU_03 dimW_03 dimInter_03\n"
                "  omega\n\n"
                "theorem alg_sub_03_m3 : indexI 3 = 13 := by rfl\n\n"
                "#eval indexI 3\n"
            ),
            "python_code": (
                "import sympy as sp\n"
                "import numpy as np\n\n"
                "def verify_alg_sub_03():\n"
                "    for m_val in range(2, 10):\n"
                "        u1 = [1, 0, m_val, 0]\n"
                "        u2 = [0, 1, 0, m_val]\n"
                "        A_W = sp.Matrix([[m_val, 0, -1, 1], [0, 0, 0, 1]])\n"
                "        null_W = A_W.nullspace()\n"
                "        assert len(null_W) == 2\n\n"
                "        basis_W = [list(v) for v in null_W]\n"
                "        M_sum = sp.Matrix([u1, u2] + basis_W)\n"
                "        _, pivots_sum = M_sum.rref()\n"
                "        dim_sum = len(pivots_sum)\n"
                "        dim_inter = 2 + len(null_W) - dim_sum\n"
                "        assert dim_sum == 3 and dim_inter == 1\n\n"
                "        # Direct sum complement check with e3 = [0, 0, 1, 0]\n"
                "        e3 = [0, 0, 1, 0]\n"
                "        M_full = np.array([u1, u2, basis_W[0], e3], dtype=float)\n"
                "        assert np.linalg.matrix_rank(M_full) == 4\n\n"
                "        b_cap = np.array(u1, dtype=int)\n"
                "        index_I = int(np.dot(b_cap, b_cap)) + dim_sum\n"
                "        assert index_I == m_val**2 + 4\n"
                "    print('VERIFIED_OK: ALG-SUB-03 Grassmann & direct sum verified across m=2..9')\n\n"
                "if __name__ == '__main__':\n"
                "    verify_alg_sub_03()\n"
            ),
        },
    ]
