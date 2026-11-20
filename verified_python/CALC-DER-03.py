import sympy as sp
import numpy as np

x = sp.Symbol('x', real=True)
m = sp.Symbol('m', positive=True)
f_expr = x**4 - 2*(m**2)*(x**2) + m**4
df = sp.diff(f_expr, x)
d2f = sp.diff(f_expr, x, 2)
roots = sorted(sp.solve(df, x), key=str)
assert sp.simplify(d2f.subs(x, 0) - (-4*m**2)) == 0
assert sp.simplify(d2f.subs(x, m) - (8*m**2)) == 0
T_sym = sp.simplify(f_expr.subs(x, 0) + (m**2) * ((-m)**2 + m**2))
assert sp.simplify(T_sym - 3*m**4) == 0, f'Mismatch: {T_sym}'

# Kiểm chứng đạo hàm cấp 2 bằng sai phân hữu hạn trên lưới m in [2..9]
h = 1e-4
for m_val in range(2, 10):
    fn = lambda t: (t**4) - 2*(m_val**2)*(t**2) + (m_val**4)
    d2_at_0 = (fn(h) - 2*fn(0.0) + fn(-h)) / (h**2)
    d2_at_m = (fn(m_val + h) - 2*fn(m_val) + fn(m_val - h)) / (h**2)
    assert abs(d2_at_0 - (-4 * m_val**2)) < 1e-3
    assert abs(d2_at_m - (8 * m_val**2)) < 1e-2
    T_num = fn(0.0) + (m_val**2) * ((-m_val)**2 + (m_val**2))
    assert abs(T_num - 3*(m_val**4)) < 1e-8

print('VERIFIED_OK: CALC-DER-03 quartic extrema & finite-difference grid [2..9] passed (3*m**4)')
