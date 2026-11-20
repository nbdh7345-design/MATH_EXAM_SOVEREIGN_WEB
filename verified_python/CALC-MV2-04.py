import math
import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', positive=True)
f = x**2 + m * y
g = [sp.diff(f, v).subs({x: 1, y: 0}) for v in (x, y)]
assert sp.simplify(sp.sqrt(g[0]**2 + g[1]**2) - sp.sqrt(m**2 + 4)) == 0
for mv in range(2, 10):
    opts = [mv + 2, math.sqrt(mv**2 + 4), math.sqrt(mv**2 + 2), mv**2 + 4]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-MV2-04')
