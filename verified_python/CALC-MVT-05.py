import sympy as sp

x = sp.symbols('x', real=True)
for mv in range(2, 10):
    f = sp.prod([x - k for k in range(1, mv + 1)])
    d2 = sp.Poly(sp.diff(f, x, 2), x)
    n_real = len(set(sp.real_roots(d2))) if d2.degree() > 0 else 0
    assert n_real == mv - 2, f'Root count mismatch at m={mv}: {n_real}'
    opts = [mv - 1, mv - 2, mv, mv + 1]
    assert len(set(opts)) == 4
print('VERIFIED_OK: CALC-MVT-05')
