import sympy as sp

x, y, z, m = sp.symbols('x y z m', real=True)
u = m * x**2 * y + y**2 * z + m * z**2 * x
H = sp.hessian(u, (x, y, z))
euler_expr = x * sp.diff(u, x) + y * sp.diff(u, y) + z * sp.diff(u, z)
assert sp.simplify(euler_expr - 3 * u) == 0
S_expr = sp.simplify(euler_expr + sp.Rational(1, 2) * H.trace())
S_111 = sp.simplify(S_expr.subs({x: 1, y: 1, z: 1}))
assert sp.simplify(S_111 - (8 * m + 4)) == 0

for m_val in range(2, 10):
    val = int(S_111.subs(m, m_val))
    assert val == 8 * m_val + 4

print('VERIFIED_OK: CALC-MUL-02 Euler partial derivatives & Hessian trace passed.')
