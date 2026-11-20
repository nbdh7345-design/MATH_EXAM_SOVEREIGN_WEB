import sympy as sp
import mpmath

t = sp.symbols('theta', real=True)
m = sp.symbols('m', positive=True)
r = m * (1 + sp.cos(t))
dr = sp.diff(r, t)

# Rút gọn r^2 + r'^2 = 2 m^2 (1 + cos theta) = 4 m^2 cos^2(theta/2)
assert sp.simplify(sp.trigsimp(r**2 + dr**2) - 2 * m**2 * (1 + sp.cos(t))) == 0
for tv in [-3.0, -1.2, 0.0, 0.7, 2.5]:
    assert abs(2 * (1 + mpmath.cos(tv)) - 4 * mpmath.cos(tv / 2)**2) < 1e-12

S = sp.integrate(r**2 / 2, (t, -sp.pi, sp.pi))
assert sp.simplify(S - 3 * sp.pi * m**2 / 2) == 0, f'Area mismatch: {S}'
L = sp.integrate(2 * m * sp.cos(t / 2), (t, -sp.pi, sp.pi))
assert sp.simplify(L - 8 * m) == 0, f'Length mismatch: {L}'

for mv in range(2, 10):
    Ln = mpmath.quad(lambda th: mpmath.sqrt((mv * (1 + mpmath.cos(th)))**2 + (mv * mpmath.sin(th))**2),
                     [-mpmath.pi, 0, mpmath.pi])
    assert abs(Ln - 8 * mv) < 1e-8 * mv, f'Numeric length failed at m={mv}'
    Sn = mpmath.quad(lambda th: (mv * (1 + mpmath.cos(th)))**2 / 2, [-mpmath.pi, mpmath.pi])
    assert abs(Sn - 1.5 * mpmath.pi * mv**2) < 1e-8 * mv**2, f'Numeric area failed at m={mv}'

print('VERIFIED_OK: CALC-APP-03')
