# -*- coding: utf-8 -*-
import sympy as sp
import numpy as np

def verify_calc_mulint_03():
    m = sp.Symbol('m', positive=True, integer=True)
    r, phi, z = sp.symbols('r phi z', real=True)

    # 1. Symbolic iterated integrals in cylindrical coordinates
    V_sym = sp.integrate(
        sp.integrate(
            sp.integrate(r, (z, r**2, m**2)),
            (r, 0, m)
        ),
        (phi, 0, 2 * sp.pi)
    )
    M_xy_sym = sp.integrate(
        sp.integrate(
            sp.integrate(z * r, (z, r**2, m**2)),
            (r, 0, m)
        ),
        (phi, 0, 2 * sp.pi)
    )

    target_V = sp.pi * m**4 / 2
    target_M = sp.pi * m**6 / 3
    target_zbar = sp.Rational(2, 3) * m**2

    assert sp.simplify(V_sym - target_V) == 0, f"Volume mismatch: {V_sym} != {target_V}"
    assert sp.simplify(M_xy_sym - target_M) == 0, f"Moment mismatch: {M_xy_sym} != {target_M}"
    assert sp.simplify(M_xy_sym / V_sym - target_zbar) == 0, "Centroid z_bar mismatch"

    # 2. Also verify by changing integration order (z outer, r inner)
    M_xy_reordered = sp.integrate(
        sp.integrate(
            sp.integrate(z * r, (r, 0, sp.sqrt(z))),
            (z, 0, m**2)
        ),
        (phi, 0, 2 * sp.pi)
    )
    assert sp.simplify(M_xy_reordered - target_M) == 0, "Fubini reordered integral mismatch"

    # 3. Numerical cylindrical grid quadrature check across m in [2, 3, 4]
    for m_val in [2, 3, 4]:
        r_grid = np.linspace(0.0, m_val, 2000)
        integrand_r = 2.0 * np.pi * r_grid * 0.5 * (m_val**4 - r_grid**4)
        num_M = float(np.sum(0.5 * (integrand_r[:-1] + integrand_r[1:]) * np.diff(r_grid)))
        exact_M = float(target_M.subs(m, m_val).evalf())
        rel_err = abs(num_M - exact_M) / exact_M
        assert rel_err < 1e-5, f"Quadrature mismatch for m={m_val}: {num_M} vs {exact_M}"

    print(
        f"VERIFIED_OK: CALC-MULINT-03 | V(m) = {V_sym}, M_xy(m) = {M_xy_sym}, "
        f"z_bar(m) = {sp.simplify(M_xy_sym / V_sym)}"
    )

if __name__ == "__main__":
    verify_calc_mulint_03()
