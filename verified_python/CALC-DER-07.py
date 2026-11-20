import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
f = x**3 - 3 * m**2 * x
crit = sp.solve(sp.diff(f, x), x)
assert set(crit) == {m, -m}, f'Critical points mismatch: {crit}'
for mv in range(2, 10):
    fv = f.subs(m, mv)
    cands = [fv.subs(x, 0), fv.subs(x, mv), fv.subs(x, 2 * mv)]
    M, n = max(cands), min(cands)
    assert M == 2 * mv**3 and n == -2 * mv**3 and M - n == 4 * mv**3
    grid = [fv.subs(x, sp.Rational(2 * mv * i, 400)) for i in range(401)]
    assert max(grid) <= M and min(grid) >= n
print('VERIFIED_OK: CALC-DER-07')
