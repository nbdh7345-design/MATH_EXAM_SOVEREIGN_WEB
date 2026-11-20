import sympy as sp

x, t = sp.symbols('x t', real=True)
m = sp.symbols('m', positive=True)
G = sp.integrate((x - t) * sp.sin(m * t), (t, 0, x))
Gp = sp.simplify(sp.diff(G, x))
assert sp.simplify(Gp - (1 - sp.cos(m * x)) / m) == 0, f'G prime mismatch: {Gp}'
assert sp.simplify(Gp.subs(x, sp.pi / m) - 2 / m) == 0
for mv in range(2, 10):
    opts = [sp.Rational(1, mv), sp.Rational(2, mv), sp.Rational(1, mv**2), 2]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-ANTI-05')
