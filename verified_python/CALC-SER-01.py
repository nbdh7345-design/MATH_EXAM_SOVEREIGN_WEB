import sympy as sp
import numpy as np

n = sp.Symbol('n', integer=True, positive=True)
m_sym = sp.Symbol('m', integer=True, positive=True)

for m_val in range(2, 10):
    term = m_val / (n * (n + 1)) + (m_val - 1) / (m_val ** n)
    exact_sum = sp.summation(term, (n, 1, sp.oo))
    expected = m_val + 1
    assert sp.simplify(exact_sum - expected) == 0, f'Mismatch at m={m_val}: {exact_sum} != {expected}'
    # Numerical partial sum verification via numpy
    k = np.arange(1, 5000, dtype=np.float64)
    partial_sum = np.sum(m_val / (k * (k + 1.0))) + np.sum((m_val - 1.0) / (float(m_val) ** np.arange(1, 50)))
    assert abs(partial_sum - expected) < 1e-2, f'Numerical error at m={m_val}: {partial_sum}'

print('VERIFIED_OK: CALC-SER-01 verified symbolically via sympy.summation and numerically across m in [2..9]')
