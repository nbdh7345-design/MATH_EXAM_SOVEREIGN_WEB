import sympy as sp

m, k = sp.symbols('m k', integer=True)
A = sp.Matrix([
    [1, 1, m],
    [2, 3, 3*m + 1],
    [1, m, k]
])
det_A = sp.simplify(A.det())
k_sol = sp.solve(sp.Eq(det_A, 0), k)[0]
assert sp.simplify(k_sol - (m**2 + m - 1)) == 0, f'Unexpected k_sol: {k_sol}'

for m_val in range(2, 10):
    k_val = int(k_sol.subs(m, m_val))
    A_num = A.subs({m: m_val, k: k_val})
    rk = A_num.rank()
    nullity = len(A_num.nullspace())
    assert rk == 2 and nullity == 1 and rk + nullity == 3

print(f'VERIFIED_OK: ALG-MAP-01 k(m) = {k_sol}, m=3 -> k={k_sol.subs(m, 3)}')
