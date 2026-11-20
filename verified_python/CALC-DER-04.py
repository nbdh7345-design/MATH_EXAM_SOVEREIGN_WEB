import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
d = sp.diff(sp.log(1 + m * x), x).subs(x, 0)
assert sp.simplify(d - m) == 0, f'Derivative mismatch: {d}'
for mv in range(2, 10):
    opts = [sp.Rational(1, mv), 1, mv**2, mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-DER-04')
