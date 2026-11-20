import sympy as sp

x, y, lam = sp.symbols('x y lambda', real=True)
m = sp.symbols('m', positive=True)
L = x**2 + y**2 + lam * (2 * m - x - y)
sol = sp.solve([sp.diff(L, v) for v in (x, y, lam)], [x, y, lam], dict=True)
assert len(sol) == 1 and sol[0][x] == m and sol[0][y] == m
fmin = (x**2 + y**2).subs({x: m, y: m})
assert sp.expand(x**2 + (2 * m - x)**2 - (2 * (x - m)**2 + 2 * m**2)) == 0
assert sp.simplify(fmin - 2 * m**2) == 0
for mv in range(2, 10):
    opts = [mv**2, 4 * mv**2, 2 * mv**2, sp.Rational(mv**2, 2)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-LAG-05')
