import sympy as sp

x, m = sp.symbols('x m', positive=True)
roots = sp.solve(sp.Eq(x**2, m * x), x)
assert set(roots) == {m}, f'Unexpected positive roots: {roots}'
S = sp.integrate(m * x - x**2, (x, 0, m))
assert sp.simplify(S - m**3 / 6) == 0, f'Area mismatch: {S}'

for mv in range(2, 10):
    # Kiểm tra số: tổng Riemann điểm giữa
    N = 20000
    h = mv / N
    approx = sum((mv * (h * (i + 0.5)) - (h * (i + 0.5))**2) * h for i in range(N))
    assert abs(approx - mv**3 / 6) < 1e-6 * mv**3, f'Numeric area failed at m={mv}'
    opts = [sp.Rational(mv**3, 6), sp.Rational(mv**3, 3), sp.Rational(mv**3, 2), sp.Rational(mv**2, 6)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-APP-01')
