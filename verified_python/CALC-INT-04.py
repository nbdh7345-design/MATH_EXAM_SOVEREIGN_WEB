import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
I = sp.integrate(2 * x + 1, (x, 0, m))
assert sp.expand(I - (m**2 + m)) == 0, f'Integral mismatch: {I}'
for mv in range(2, 10):
    opts = [mv**2 + mv, mv**2, 2 * mv**2 + mv, mv**2 + 2 * mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-INT-04')
