import sympy as sp
import numpy as np

n = sp.Symbol('n', integer=True, positive=True)

for m_val in range(2, 10):
    f_1 = sp.summation(n / (m_val ** n), (n, 1, sp.oo))
    expected_f1 = sp.Rational(m_val, (m_val - 1) ** 2)
    assert sp.simplify(f_1 - expected_f1) == 0, f'Symbolic sum failed at m={m_val}'
    T_val = sp.simplify(m_val * ((m_val - 1) ** 2) * f_1)
    assert T_val == m_val ** 2, f'T(m) mismatch at m={m_val}: {T_val}'
    # Numerical partial sum verification via numpy
    k = np.arange(1, 80, dtype=np.float64)
    partial_T = m_val * ((m_val - 1.0) ** 2) * np.sum(k / (float(m_val) ** k))
    assert abs(partial_T - (m_val ** 2)) < 1e-7, f'Numpy partial sum error at m={m_val}: {partial_T}'

print('VERIFIED_OK: CALC-SER-03 power series sum and T(m)=m^2 verified across m in [2..9]')
