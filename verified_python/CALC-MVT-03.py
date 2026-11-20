import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
f = x**3 - 3 * m * x**2 + 2
assert sp.simplify(f.subs(x, 0) - f.subs(x, 3 * m)) == 0
crit = sp.solve(sp.diff(f, x), x)
inside = [c for c in crit if sp.simplify(c) != 0]
assert len(inside) == 1 and sp.simplify(inside[0] - 2 * m) == 0, f'Rolle point mismatch: {crit}'
infl = sp.solve(sp.diff(f, x, 2), x)
assert len(infl) == 1 and sp.simplify(infl[0] - m) == 0
assert sp.simplify(f.subs(x, m) - (2 - 2 * m**3)) == 0

for mv in range(2, 10):
    fv = f.subs(m, mv)
    d2 = sp.diff(fv, x, 2)
    assert d2.subs(x, mv - sp.Rational(1, 2)) < 0 and d2.subs(x, mv + sp.Rational(1, 2)) > 0
    assert fv.subs(x, mv) == 2 - 2 * mv**3

print('VERIFIED_OK: CALC-MVT-03')
