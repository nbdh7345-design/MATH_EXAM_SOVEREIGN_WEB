import sympy as sp

t = sp.symbols('t', real=True)
m = sp.symbols('m', positive=True)
z = sp.exp(m * t + t**2)
d = sp.diff(z, t).subs(t, 0)
assert sp.simplify(d - m) == 0, f'Derivative mismatch: {d}'
for mv in range(2, 10):
    assert len({1, mv + 1, 2 * mv, mv}) == 4
print('VERIFIED_OK: CALC-MV2-05')
