import math
import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', positive=True)
F = x * sp.exp(y) + y - m
assert sp.simplify(F.subs({x: 0, y: m})) == 0
yp = (-sp.diff(F, x) / sp.diff(F, y)).subs({x: 0, y: m})
assert sp.simplify(yp + sp.exp(m)) == 0, f'y prime mismatch: {yp}'
assert sp.simplify(sp.idiff(F, y, x).subs({x: 0, y: m}) + sp.exp(m)) == 0

def solve_y(xv, mv):
    yv = float(mv)
    for _ in range(100):
        g = xv * math.exp(yv) + yv - mv
        dg = xv * math.exp(yv) + 1
        yv -= g / dg
    return yv

for mv in range(2, 10):
    h = 1e-7
    num = (solve_y(h, mv) - solve_y(-h, mv)) / (2 * h)
    assert abs(num + math.exp(mv)) < 1e-3 * math.exp(mv), f'Numeric check failed at m={mv}'
    opts = [math.exp(mv), -math.exp(mv), -math.exp(-mv), -mv * math.exp(mv)]
    assert len(set(opts)) == 4

print('VERIFIED_OK: CALC-MV2-02')
