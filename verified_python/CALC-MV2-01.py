import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', positive=True)
u = x + m * y
v = m * x - y
z = u**2 * v
zx = sp.diff(z, x).subs({x: 1, y: 1})
assert sp.expand(zx - (m + 1) * (m**2 + 3 * m - 2)) == 0, f'z_x mismatch: {sp.factor(zx)}'

U, V = sp.symbols('U V')
Z = U**2 * V
chain = (sp.diff(Z, U) * sp.diff(u, x) + sp.diff(Z, V) * sp.diff(v, x)).subs({U: u, V: v})
assert sp.expand(chain - sp.diff(z, x)) == 0

for mv in range(2, 10):
    opts = [(mv + 1) * (mv**2 + 3 * mv - 2), (mv + 1) * (mv**2 + mv - 2), (mv + 1) * (mv**2 + 3 * mv), 2 * (mv + 1) * (mv - 1)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
    h = 1e-6
    zf = lambda a, b: (a + mv * b)**2 * (mv * a - b)
    num = (zf(1 + h, 1) - zf(1 - h, 1)) / (2 * h)
    assert abs(num - opts[0]) < 1e-4 * opts[0]

print('VERIFIED_OK: CALC-MV2-01')
