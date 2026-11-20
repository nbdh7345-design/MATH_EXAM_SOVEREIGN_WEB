import math
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
I = sp.integrate(sp.exp(m * x), (x, 0, 1))
assert sp.simplify(I - (sp.exp(m) - 1) / m) == 0, f'Integral mismatch: {I}'
for mv in range(2, 10):
    e = math.exp(mv)
    opts = [e - 1, (e - 1) / mv, mv * (e - 1), (e + 1) / mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-ANTI-04')
