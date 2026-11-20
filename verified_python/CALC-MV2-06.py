import math
import sympy as sp

x, y, z = sp.symbols('x y z', real=True)
m = sp.symbols('m', positive=True)
F = sp.exp(z) + x * y * z - m
pt = {x: 0, y: 1, z: sp.log(m)}
assert sp.simplify(F.subs(pt)) == 0
zx = sp.simplify((-sp.diff(F, x) / sp.diff(F, z)).subs(pt))
assert sp.simplify(zx + sp.log(m) / m) == 0, f'z_x mismatch: {zx}'

def solve_z(xv, yv, mv):
    zv = math.log(mv)
    for _ in range(100):
        g = math.exp(zv) + xv * yv * zv - mv
        zv -= g / (math.exp(zv) + xv * yv)
    return zv

for mv in range(2, 10):
    h = 1e-7
    num = (solve_z(h, 1, mv) - solve_z(-h, 1, mv)) / (2 * h)
    assert abs(num + math.log(mv) / mv) < 1e-5, f'Numeric check failed at m={mv}'
    opts = [math.log(mv) / mv, -math.log(mv) / mv, -1 / mv, -mv * math.log(mv)]
    assert len({round(o, 12) for o in opts}) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-MV2-06')
