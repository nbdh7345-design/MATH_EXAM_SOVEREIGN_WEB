import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
y = (m * x + 1) / (x - m)
assert sp.simplify(sp.limit(y, x, sp.oo) - m) == 0 and sp.simplify(sp.limit(y, x, -sp.oo) - m) == 0
for mv in range(2, 10):
    opts = [-mv, 1, mv, sp.Rational(1, mv)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-MVT-04')
