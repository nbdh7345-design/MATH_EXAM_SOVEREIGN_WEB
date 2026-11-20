import sympy as sp

x, y, k = sp.symbols('x y k', real=True)
m = sp.symbols('m', positive=True)
g = m * x * y / (x**2 + y**2)
along = sp.simplify(g.subs(y, k * x))
assert sp.simplify(along - m * k / (1 + k**2)) == 0, f'Path value mismatch: {along}'
assert along.subs(k, 0) != along.subs(k, 1)

f = x**2 * y + m * y**3
grad = [sp.diff(f, x).subs({x: 1, y: 1}), sp.diff(f, y).subs({x: 1, y: 1})]
assert grad[0] == 2 and sp.simplify(grad[1] - (1 + 3 * m)) == 0
u = (sp.Rational(3, 5), sp.Rational(4, 5))
D = grad[0] * u[0] + grad[1] * u[1]
assert sp.simplify(D - (12 * m + 10) / 5) == 0

t = sp.symbols('t', real=True)
for mv in range(2, 10):
    ft = f.subs(m, mv).subs({x: 1 + t * u[0], y: 1 + t * u[1]})
    assert sp.simplify(sp.diff(ft, t).subs(t, 0) - sp.Rational(12 * mv + 10, 5)) == 0

print('VERIFIED_OK: CALC-MV2-03')
