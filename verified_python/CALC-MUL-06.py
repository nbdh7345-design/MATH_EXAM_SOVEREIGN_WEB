import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', positive=True)
f = x**2 * y + m * x * y**2
fx, fy = sp.diff(f, x).subs({x: 1, y: 1}), sp.diff(f, y).subs({x: 1, y: 1})
assert sp.simplify(fx - (m + 2)) == 0 and sp.simplify(fy - (2 * m + 1)) == 0
approx = f.subs({x: 1, y: 1}) + fx * sp.Rational(2, 100) + fy * sp.Rational(-1, 100)
assert sp.simplify(approx - (m + sp.Rational(103, 100))) == 0, f'Approximation mismatch: {approx}'
for mv in range(2, 10):
    exact = float(f.subs({m: mv, x: sp.Rational(102, 100), y: sp.Rational(99, 100)}))
    assert abs(exact - (mv + 1.03)) < 2e-3 * mv, f'Approximation too far at m={mv}: {exact}'
print('VERIFIED_OK: CALC-MUL-06')
