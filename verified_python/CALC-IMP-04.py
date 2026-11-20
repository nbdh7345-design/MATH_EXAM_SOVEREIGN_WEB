import sympy as sp

x = sp.symbols('x', positive=True)
for mv in range(2, 10):
    I = sp.integrate(x**(-mv), (x, 1, sp.oo))
    assert I == sp.Rational(1, mv - 1), f'Integral mismatch at m={mv}: {I}'
    opts = [sp.Rational(1, mv), sp.Rational(mv, mv - 1), sp.Rational(1, mv - 1), sp.Rational(1, mv + 1)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-IMP-04')
