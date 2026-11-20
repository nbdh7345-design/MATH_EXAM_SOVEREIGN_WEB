import math
import sympy as sp

x, y, lam = sp.symbols('x y lambda', real=True)
m = sp.symbols('m', positive=True)
L = x * y + lam * (2 * m**2 - x**2 - y**2)
sols = sp.solve([sp.diff(L, v) for v in (x, y, lam)], [x, y, lam], dict=True)
vals = {sp.simplify((x * y).subs(s)) for s in sols}
assert vals == {m**2, -m**2}, f'Stationary values: {vals}'
for mv in range(2, 10):
    r = math.sqrt(2) * mv
    samples = [r * math.cos(t) * r * math.sin(t) for t in [2 * math.pi * i / 2000 for i in range(2000)]]
    assert max(samples) <= mv**2 + 1e-9 and min(samples) >= -mv**2 - 1e-9
    assert abs(max(samples) - mv**2) < 1e-3 * mv**2
print('VERIFIED_OK: CALC-LAG-07')
