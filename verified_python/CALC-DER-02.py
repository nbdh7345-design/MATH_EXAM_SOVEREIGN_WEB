import sympy as sp
import numpy as np

x = sp.Symbol('x', real=True)
m = sp.Symbol('m', positive=True)
f_expr = x**3 - 3*m*x**2 + 4*m**3
df = sp.diff(f_expr, x)
d2f = sp.diff(f_expr, x, 2)
crit_pts = sp.solve(df, x)
y_max = f_expr.subs(x, 0)
y_min = sp.simplify(f_expr.subs(x, 2*m))
delta_sym = sp.simplify(y_max - y_min)
assert sp.simplify(delta_sym - 4*m**3) == 0, f'Expected 4*m**3, got {delta_sym}'

# Kiểm chứng số học và sai phân đạo hàm trên lưới tham số m in [2..9]
h = 1e-6
for m_val in range(2, 10):
    fn = lambda t: t**3 - 3*m_val*(t**2) + 4*(m_val**3)
    df_0 = (fn(h) - fn(-h)) / (2*h)
    df_2m = (fn(2*m_val + h) - fn(2*m_val - h)) / (2*h)
    assert abs(df_0) < 1e-7 and abs(df_2m) < 1e-6
    gap = fn(0.0) - fn(2.0 * m_val)
    assert abs(gap - 4*(m_val**3)) < 1e-8

print('VERIFIED_OK: CALC-DER-02 symbolic extrema & numerical grid [2..9] passed (4*m**3)')
