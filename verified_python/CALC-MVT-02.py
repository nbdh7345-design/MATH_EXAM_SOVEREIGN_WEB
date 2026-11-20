import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
y = (x**2 + m * x + 1) / (x - 1)
a = sp.limit(y / x, x, sp.oo)
b = sp.limit(y - a * x, x, sp.oo)
assert a == 1 and sp.simplify(b - (m + 1)) == 0, f'Asymptote mismatch: a={a}, b={b}'
assert sp.limit(y / x, x, -sp.oo) == 1 and sp.simplify(sp.limit(y - x, x, -sp.oo) - (m + 1)) == 0
q, r = sp.div(sp.Poly(x**2 + m * x + 1, x), sp.Poly(x - 1, x))
assert sp.simplify(q.as_expr() - (x + m + 1)) == 0 and sp.simplify(r.as_expr() - (m + 2)) == 0

for mv in range(2, 10):
    yv = lambda t: (t**2 + mv * t + 1) / (t - 1)
    assert abs(yv(1e7) - (1e7 + mv + 1)) < 1e-5
    opts = [mv + 1, mv, mv + 3, mv + 2]
    assert len(set(opts)) == 4

print('VERIFIED_OK: CALC-MVT-02')
