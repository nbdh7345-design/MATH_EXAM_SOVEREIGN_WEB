import sympy as sp

def verify_calc_ode_01():
    x = sp.Symbol('x', real=True)
    m = sp.Symbol('m', integer=True, positive=True)
    y = (m**2 * x + m) * sp.exp(-m * x)
    ode_res = sp.simplify(sp.diff(y, x) + m * y - m**2 * sp.exp(-m * x))
    ic_res = sp.simplify(y.subs(x, 0) - m)
    assert ode_res == 0, f'ODE residual non-zero: {ode_res}'
    assert ic_res == 0, f'IC residual non-zero: {ic_res}'
    I_expr = sp.simplify(sp.exp(m) * y.subs(x, 1))
    assert sp.simplify(I_expr - (m**2 + m)) == 0
    for m_val in range(2, 10):
        y_num = y.subs(m, m_val)
        assert sp.simplify(sp.diff(y_num, x) + m_val * y_num - m_val**2 * sp.exp(-m_val * x)) == 0
        assert int(I_expr.subs(m, m_val)) == m_val**2 + m_val
    print('VERIFIED_OK: CALC-ODE-01 | I(3) =', int(I_expr.subs(m, 3)))

if __name__ == '__main__':
    verify_calc_ode_01()
