import math
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
L = sp.limit(sp.sin(m * x) / x, x, 0)
assert sp.simplify(L - m) == 0, f'Limit mismatch: {L}'
for mv in range(2, 10):
    assert abs(math.sin(mv * 1e-6) / 1e-6 - mv) < 1e-6
    opts = [1, mv, 1 / mv, mv**2]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-LIM-04')
