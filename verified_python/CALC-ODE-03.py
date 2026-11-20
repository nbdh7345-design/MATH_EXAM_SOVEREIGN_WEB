import sympy as sp

def verify_calc_ode_03():
    t = sp.Symbol('t', real=True)
    m = sp.Symbol('m', integer=True, positive=True)
    x_sol = m + 2 * m * sp.exp(2 * m * t)
    y_sol = -m + 2 * m * sp.exp(2 * m * t)
    res1 = sp.simplify(sp.diff(x_sol, t) - (m * x_sol + m * y_sol))
    res2 = sp.simplify(sp.diff(y_sol, t) - (m * x_sol + m * y_sol))
    assert res1 == 0 and res2 == 0, f'System ODE residuals: {res1}, {res2}'
    assert sp.simplify(x_sol.subs(t, 0) - 3 * m) == 0
    assert sp.simplify(y_sol.subs(t, 0) - m) == 0
    t0 = sp.log(2) / (2 * m)
    P_expr = sp.simplify(x_sol.subs(t, t0) * y_sol.subs(t, t0))
    assert sp.simplify(P_expr - 15 * m**2) == 0
    for m_val in range(2, 10):
        assert int(P_expr.subs(m, m_val)) == 15 * m_val**2
    print('VERIFIED_OK: CALC-ODE-03 | P(3) =', int(P_expr.subs(m, 3)))

if __name__ == '__main__':
    verify_calc_ode_03()
