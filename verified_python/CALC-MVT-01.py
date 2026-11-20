import sympy as sp

c, m = sp.symbols('c m', positive=True)
f = lambda t: t**3
sols = sp.solve(sp.Eq(sp.diff(c**3, c) * m, f(m) - f(0)), c)
assert sols == [sp.sqrt(3) * m / 3], f'Unexpected Lagrange points: {sols}'

for mv in range(2, 10):
    cv = mv * sp.sqrt(3) / 3
    assert 0 < cv < mv
    assert sp.simplify(3 * cv**2 * mv - mv**3) == 0
    opts = [mv * sp.sqrt(3) / 3, sp.Rational(mv, 2), sp.Rational(mv, 3), mv * sp.sqrt(2) / 2]
    assert len({float(o) for o in opts}) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-MVT-01')
