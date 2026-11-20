import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
lam = sp.Symbol('lam')

A = sp.Matrix([[2*m, m], [m, 2*m]])
charpoly = sp.factor(A.charpoly(lam).as_expr())
eigs = A.eigenvals()
sum_sq_sym = sp.simplify(sum(val**2 * mult for val, mult in eigs.items()))
viete_sym = sp.simplify(A.trace()**2 - 2*A.det())

assert sp.simplify(sum_sq_sym - 10*m**2) == 0, f"Symbolic mismatch: {sum_sq_sym}"
assert sp.simplify(viete_sym - 10*m**2) == 0, f"Viete mismatch: {viete_sym}"

for m_val in range(2, 10):
    A_num = np.array([[2*m_val, m_val], [m_val, 2*m_val]], dtype=float)
    eig_num = np.linalg.eigvals(A_num)
    val_num = float(np.sum(eig_num**2))
    expected = float(10 * m_val**2)
    assert np.isclose(val_num, expected, rtol=1e-9), f"Numeric mismatch at m={m_val}: {val_num} != {expected}"

print(f"VERIFIED_OK: ALG-EIG-01 | charpoly={charpoly} | S(m)={sum_sq_sym} | S(3)={sum_sq_sym.subs(m, 3)}")
