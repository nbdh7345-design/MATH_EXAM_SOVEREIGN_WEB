import sympy as sp
import numpy as np

x, m = sp.symbols('x m', real=True)
f_expr = (x**2) * sp.exp(m * x)
d4_symbolic = sp.simplify(sp.diff(f_expr, x, 4).subs(x, 0))
expected_symbolic = 12 * m**2
assert sp.simplify(d4_symbolic - expected_symbolic) == 0, f'Symbolic mismatch: {d4_symbolic}'

# Kiểm chứng sai phân hữu hạn bậc 4 trên lưới tham số m in [2..9]
h = 1e-3
for m_val in range(2, 10):
    fn = lambda t: (t**2) * np.exp(m_val * t)
    num_d4 = (fn(-2*h) - 4*fn(-h) + 6*fn(0.0) - 4*fn(h) + fn(2*h)) / (h**4)
    exact_val = float(12 * (m_val**2))
    assert abs(num_d4 - exact_val) / exact_val < 1e-4, f'Grid failure at m={m_val}: {num_d4} vs {exact_val}'

print('VERIFIED_OK: CALC-DER-01 symbolic diff & finite-difference grid [2..9] passed (12*m**2)')
