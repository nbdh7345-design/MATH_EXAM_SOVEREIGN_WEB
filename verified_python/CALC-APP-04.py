import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
S = sp.integrate(m * x**2, (x, 0, 1))
assert sp.simplify(S - m / 3) == 0, f'Area mismatch: {S}'
for mv in range(2, 10):
    opts = [sp.Rational(mv, 2), sp.Rational(mv, 3), mv, sp.Rational(mv, 6)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-APP-04')
