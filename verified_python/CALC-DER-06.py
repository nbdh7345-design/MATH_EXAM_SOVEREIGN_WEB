import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
d10 = sp.diff(x**2 * sp.exp(m * x), x, 10).subs(x, 0)
assert sp.simplify(d10 - 90 * m**8) == 0, f'10th derivative mismatch: {d10}'
assert sp.binomial(10, 2) == 45
for mv in range(2, 10):
    opts = [45 * mv**8, 90 * mv**10, 90 * mv**8, 180 * mv**8]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-DER-06')
