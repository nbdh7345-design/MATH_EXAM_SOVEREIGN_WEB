import sympy as sp

m = sp.Symbol('m', integer=True)
A = sp.Matrix([
    [1, 2, m],
    [2, 5, 3*m + 1],
    [3, 7, 4*m + 1]
])
ns = A.nullspace()
assert len(ns) == 1
u = sp.simplify(ns[0] / ns[0][2])
a_expr, b_expr = sp.simplify(u[0]), sp.simplify(u[1])
assert sp.simplify(a_expr - (m + 2)) == 0
assert sp.simplify(b_expr - (-(m + 1))) == 0
Q_expr = sp.simplify(2 * a_expr - b_expr)
assert sp.simplify(Q_expr - (3*m + 5)) == 0

for m_val in range(2, 10):
    A_num = A.subs(m, m_val)
    d_val = A_num.rank()
    ns_num = A_num.nullspace()[0]
    ns_norm = ns_num / ns_num[2]
    q_num = int(d_val * ns_norm[0] - ns_norm[1])
    assert d_val == 2 and q_num == 3 * m_val + 5

print(f'VERIFIED_OK: ALG-MAP-02 Q(m) = {Q_expr}, m=3 -> Q={Q_expr.subs(m, 3)}')
