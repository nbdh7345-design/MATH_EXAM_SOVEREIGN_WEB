import sympy as sp

x, y = sp.symbols('x y', real=True)
for mv in range(2, 10):
    f = x**3 + y**3 - 3 * mv * x * y
    crit = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
    real_crit = {(c[x], c[y]) for c in crit if c[x].is_real and c[y].is_real}
    assert real_crit == {(0, 0), (mv, mv)}, f'Critical points mismatch at m={mv}: {real_crit}'
    H = sp.hessian(f, (x, y))
    H0, Hm = H.subs({x: 0, y: 0}), H.subs({x: mv, y: mv})
    assert H0.det() < 0
    assert Hm.det() > 0 and Hm[0, 0] > 0
    assert f.subs({x: mv, y: mv}) == -mv**3
    opts = [-2 * mv**3, mv**3, -mv**3, -3 * mv**3]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-MUL-05')
