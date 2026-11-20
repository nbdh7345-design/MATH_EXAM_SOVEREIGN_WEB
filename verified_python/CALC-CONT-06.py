import sympy as sp

x, a, b = sp.symbols('x a b', real=True)
n = sp.symbols('n', positive=True)
m = sp.symbols('m', positive=True)
left = sp.limit(x**2 + a * x, x, 1, '-')
right = sp.limit(m * x + 3, x, 1, '+')
sol = sp.solve([sp.Eq(left, right), sp.Eq(right, b)], [a, b], dict=True)[0]
assert sp.simplify(sol[a] - (m + 2)) == 0 and sp.simplify(sol[b] - (m + 3)) == 0
assert sp.simplify(sol[a] + sol[b] - (2 * m + 5)) == 0
L = sp.limit(sp.sqrt(n**2 + m * n) - n, n, sp.oo)
assert sp.simplify(L - m / 2) == 0, f'Sequence limit mismatch: {L}'
print('VERIFIED_OK: CALC-CONT-06')
