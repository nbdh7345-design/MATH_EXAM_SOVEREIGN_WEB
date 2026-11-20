import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
lam = sp.Symbol('lam')

B = sp.Matrix([
    [m + 1, 1, 0],
    [2, m + 2, 0],
    [0, 0, 2*m]
])
eigs_B = B.eigenvals()
sum_eigs = sp.simplify(sum(val * mult for val, mult in eigs_B.items()))
prod_eigs = sp.simplify(sp.prod([val**mult for val, mult in eigs_B.items()]))
T_sym = sp.expand(prod_eigs + sum_eigs)
target_sym = 2*m**3 + 6*m**2 + 4*m + 3

assert sp.simplify(T_sym - target_sym) == 0, f"Symbolic mismatch: {T_sym}"
assert sp.simplify(B.trace() - sum_eigs) == 0
assert sp.simplify(B.det() - prod_eigs) == 0

for m_val in range(2, 10):
    B_num = np.array([
        [m_val + 1, 1, 0],
        [2, m_val + 2, 0],
        [0, 0, 2*m_val]
    ], dtype=float)
    eig_num = np.linalg.eigvals(B_num)
    t_num = float(np.prod(eig_num) + np.sum(eig_num))
    expected = float(2*m_val**3 + 6*m_val**2 + 4*m_val + 3)
    assert np.isclose(t_num, expected, rtol=1e-9), f"Numeric mismatch at m={m_val}: {t_num} != {expected}"

print(f"VERIFIED_OK: ALG-EIG-02 | eigs={list(eigs_B.keys())} | T(m)={T_sym} | T(3)={T_sym.subs(m, 3)}")
