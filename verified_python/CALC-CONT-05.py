import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
alpha = sp.tan(m * x) - sp.sin(m * x)
ser = sp.series(alpha, x, 0, 5).removeO()
assert sp.simplify(ser.coeff(x, 1)) == 0 and sp.simplify(ser.coeff(x, 2)) == 0
C = sp.simplify(ser.coeff(x, 3))
assert sp.simplify(C - m**3 / 2) == 0, f'Coefficient mismatch: {C}'
assert sp.simplify(sp.limit(alpha / x**3, x, 0) - m**3 / 2) == 0
for mv in range(2, 10):
    opts = [sp.Rational(mv**3, 2), 3 * mv**3, sp.Rational(3 * mv**3, 2), mv**3]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-CONT-05')
