import sympy as sp

x, y, lam = sp.symbols('x y lambda', real=True)
m = sp.symbols('m', positive=True)
L = x * y + lam * (m - x - y)
sol = sp.solve([sp.diff(L, v) for v in (x, y, lam)], [x, y, lam], dict=True)
assert len(sol) == 1 and sp.simplify(sol[0][lam] - m / 2) == 0, f'Stationary point mismatch: {sol}'
for mv in range(2, 10):
    opts = [mv, sp.Rational(mv, 2), sp.Rational(mv, 4), 2 * mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-LAG-04')
