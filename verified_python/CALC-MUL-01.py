import sympy as sp

x, y, m = sp.symbols('x y m', real=True)
f = x**3 + y**3 - 3*m*x*y + m**3
gx = sp.diff(f, x)
gy = sp.diff(f, y)
H = sp.hessian(f, (x, y))
det_H = sp.simplify(H.det())

for m_val in range(2, 10):
    assert gx.subs({x: m_val, y: m_val, m: m_val}) == 0
    assert gy.subs({x: m_val, y: m_val, m: m_val}) == 0
    det_at_min = int(det_H.subs({x: m_val, y: m_val, m: m_val}))
    f_xx_val = int(H[0, 0].subs({x: m_val, y: m_val, m: m_val}))
    f_min_val = int(f.subs({x: m_val, y: m_val, m: m_val}))
    assert det_at_min > 0 and f_xx_val > 0
    assert det_at_min + f_min_val == 27 * (m_val ** 2)

print('VERIFIED_OK: CALC-MUL-01 symbolic Hessian and grid m in [2..9] passed.')
