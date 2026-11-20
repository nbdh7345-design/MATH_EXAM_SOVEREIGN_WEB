import math
import sympy as sp

n, m = sp.symbols('n m', positive=True)
L = sp.limit((1 + m / n)**(2 * n), n, sp.oo)
assert sp.simplify(L - sp.exp(2 * m)) == 0, f'Limit mismatch: {L}'

for mv in range(2, 10):
    N = 10**7
    approx = math.exp(2 * N * math.log1p(mv / N))
    assert abs(approx / math.exp(2 * mv) - 1) < 1e-4, f'Numeric check failed at m={mv}'
    opts = [math.exp(mv), math.exp(2 * mv), math.exp(mv / 2), math.exp(3 * mv)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-CONT-01')
