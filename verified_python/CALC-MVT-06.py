import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
y = x / (x**2 + m**2)
crit = sp.solve(sp.diff(y, x), x)
assert set(crit) == {m, -m}, f'Critical points: {crit}'
ymax, ymin = y.subs(x, m), y.subs(x, -m)
assert sp.simplify(ymax - 1 / (2 * m)) == 0 and sp.simplify(ymin + 1 / (2 * m)) == 0
assert sp.simplify(ymax - ymin - 1 / m) == 0
assert sp.limit(y, x, sp.oo) == 0 and sp.limit(y, x, -sp.oo) == 0
for mv in range(2, 10):
    yv = y.subs(m, mv)
    assert sp.diff(yv, x, 2).subs(x, mv) < 0 and sp.diff(yv, x, 2).subs(x, -mv) > 0
print('VERIFIED_OK: CALC-MVT-06')
