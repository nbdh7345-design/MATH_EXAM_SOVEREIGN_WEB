import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', positive=True)
z = sp.log(x**2 + m * y**2)
zx, zy = sp.diff(z, x), sp.diff(z, y)
assert sp.simplify(x * zx + y * zy - 2) == 0
zyy = sp.diff(z, y, 2).subs({x: 1, y: 0})
assert sp.simplify(zyy - 2 * m) == 0, f'z_yy mismatch: {zyy}'
print('VERIFIED_OK: CALC-MV2-07')
