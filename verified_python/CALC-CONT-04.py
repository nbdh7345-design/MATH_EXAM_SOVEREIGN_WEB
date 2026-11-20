import sympy as sp

n = sp.symbols('n', positive=True)
m = sp.symbols('m', positive=True)
L = sp.limit((m * n**2 + 1) / (n**2 + n), n, sp.oo)
assert sp.simplify(L - m) == 0, f'Limit mismatch: {L}'
for mv in range(2, 10):
    N = 10**7
    assert abs((mv * N**2 + 1) / (N**2 + N) - mv) < 1e-5 * mv
    assert len({1, mv, 0, mv + 1}) == 4
print('VERIFIED_OK: CALC-CONT-04')
