# -*- coding: utf-8 -*-
import sympy as sp
import numpy as np

def verify_calc_mulint_01():
    m = sp.Symbol('m', positive=True, integer=True)
    r, phi = sp.symbols('r phi', real=True)

    # Symbolic iterated integral in polar coordinates (with Jacobian r)
    integrand_polar = (r**2) * r
    I_sym = sp.integrate(sp.integrate(integrand_polar, (r, 0, m)), (phi, 0, 2 * sp.pi))
    target_sym = sp.pi * m**4 / 2

    diff_sym = sp.simplify(I_sym - target_sym)
    assert diff_sym == 0, f"Symbolic mismatch: {I_sym} != {target_sym}"

    # Numerical grid quadrature check in Cartesian coordinates for m in [2, 3, 4]
    for m_val in [2, 3, 4]:
        n_grid = 400
        lin = np.linspace(-m_val, m_val, n_grid)
        dx = lin[1] - lin[0]
        X, Y = np.meshgrid(lin, lin, indexing='ij')
        R2 = X**2 + Y**2
        mask = R2 <= m_val**2
        num_val = np.sum(R2[mask]) * (dx * dx)
        exact_val = float(target_sym.subs(m, m_val).evalf())
        rel_err = abs(num_val - exact_val) / exact_val
        assert rel_err < 1e-2, f"Numerical mismatch for m={m_val}: {num_val} vs {exact_val}"

    print(f"VERIFIED_OK: CALC-MULINT-01 | I(m) = {I_sym} | m=3 -> {target_sym.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_mulint_01()
