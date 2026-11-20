import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
coeff = sp.series(sp.exp(m * x), x, 0, 4).removeO().coeff(x, 3)
assert sp.simplify(coeff - m**3 / 6) == 0, f'Coefficient mismatch: {coeff}'
for mv in range(2, 10):
    c = sp.diff(sp.exp(mv * x), x, 3).subs(x, 0) / sp.factorial(3)
    assert c == sp.Rational(mv**3, 6)
    opts = [sp.Rational(mv**3, 3), sp.Rational(mv**3, 2), sp.Rational(mv**3, 6), sp.Rational(mv**2, 6)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-LIM-05')
