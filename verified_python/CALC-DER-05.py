import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
d2 = sp.diff(x * sp.exp(m * x), x, 2).subs(x, 0)
assert sp.simplify(d2 - 2 * m) == 0, f'Second derivative mismatch: {d2}'
for mv in range(2, 10):
    opts = [3 * mv, 2 * mv, mv, mv**2 + 2 * mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-DER-05')
