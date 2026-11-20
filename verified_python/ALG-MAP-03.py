import sympy as sp

m, lam = sp.symbols('m lam', integer=True)
A = sp.Matrix([
    [1, 2, -1, m],
    [2, 5, 0, 2*m + 1],
    [m + 2, 2*m + 5, -m, m**2 + 2*m + 1]
])
rref_A, pivots = A.rref()
assert pivots == (0, 1)
assert sp.simplify(rref_A[0, 3] - (m - 2)) == 0
u1 = sp.Matrix([5, -2, 1, 0])
u2 = sp.Matrix([2 - m, -1, 0, 1])
assert sp.simplify(A * u1) == sp.zeros(3, 1)
assert sp.simplify(A * u2) == sp.zeros(3, 1)

for m_val in range(2, 10):
    A_num = A.subs(m, m_val)
    rk = A_num.rank()
    nullity = len(A_num.nullspace())
    assert rk == 2 and nullity == 2 and rk + nullity == 4
    Aug = A_num.row_join(sp.Matrix([1, 2, m_val + 2]))
    assert Aug.rank() == rk

print(f'VERIFIED_OK: ALG-MAP-03 rank=2, nullity=2, lambda(m)=m+2, m=3 -> lambda={3+2}')
