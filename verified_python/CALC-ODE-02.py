import sympy as sp

def verify_calc_ode_02():
    x = sp.Symbol('x', real=True)
    m = sp.Symbol('m', integer=True, positive=True)
    y = m * sp.exp(m * x) + sp.exp(2 * m * x)
    ode_res = sp.simplify(sp.diff(y, x, 2) - 3 * m * sp.diff(y, x) + 2 * m**2 * y)
    ic0_res = sp.simplify(y.subs(x, 0) - (m + 1))
    ic1_res = sp.simplify(sp.diff(y, x).subs(x, 0) - (m**2 + 2 * m))
    assert ode_res == 0, f'ODE residual: {ode_res}'
    assert ic0_res == 0, f'IC y(0) residual: {ic0_res}'
    assert ic1_res == 0, f'IC y_prime(0) residual: {ic1_res}'
    S_expr = sp.simplify(y.subs(x, sp.log(2) / m))
    assert sp.simplify(S_expr - (2 * m + 4)) == 0
    for m_val in range(2, 10):
        assert int(S_expr.subs(m, m_val)) == 2 * m_val + 4
    print('VERIFIED_OK: CALC-ODE-02 | S(3) =', int(S_expr.subs(m, 3)))

if __name__ == '__main__':
    verify_calc_ode_02()
