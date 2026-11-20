import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
G = sp.Matrix([
    [1, 1, 0],
    [1, 2, 0],
    [0, 0, m**2 + 1]
])
w = sp.Matrix([1, 1, 1])
norm_sq = sp.simplify((w.T * G * w)[0])
assert sp.simplify(norm_sq - (m**2 + 6)) == 0, f"Mismatch symbolic: {norm_sq}"

for m_val in range(2, 10):
    G_num = np.array([[1.0, 1.0, 0.0], [1.0, 2.0, 0.0], [0.0, 0.0, float(m_val**2 + 1)]])
    eigvals = np.linalg.eigvalsh(G_num)
    assert np.all(eigvals > 0), "Gram matrix must be positive definite"
    w_num = np.array([1.0, 1.0, 1.0])
    val_num = float(w_num @ G_num @ w_num)
    assert abs(val_num - (m_val**2 + 6)) < 1e-9

print(f"VERIFIED_OK: ALG-EUC-01 norm_sq={norm_sq}")
