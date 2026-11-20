# -*- coding: utf-8 -*-
import sympy as sp
import numpy as np

def verify_calc_mulint_02():
    m = sp.Symbol('m', positive=True, integer=True)
    rho, theta, phi = sp.symbols('rho theta phi', real=True)

    # Spherical integrand: z * (x^2 + y^2 + z^2) * Jacobian
    # z = rho * cos(theta), x^2+y^2+z^2 = rho^2, Jacobian = rho^2 * sin(theta)
    integrand = (rho * sp.cos(theta)) * (rho**2) * (rho**2 * sp.sin(theta))
    J_sym = sp.integrate(
        sp.integrate(
            sp.integrate(integrand, (rho, 0, m)),
            (theta, 0, sp.pi / 2)
        ),
        (phi, 0, 2 * sp.pi)
    )
    target_sym = sp.pi * m**6 / 6
    assert sp.simplify(J_sym - target_sym) == 0, f"Symbolic mismatch: {J_sym} != {target_sym}"

    # Also verify via cylindrical coordinates: r in [0, m], z in [0, sqrt(m^2 - r^2)], phi in [0, 2*pi]
    r, z = sp.symbols('r z', real=True)
    J_cyl = sp.integrate(
        sp.integrate(
            sp.integrate(z * (r**2 + z**2) * r, (z, 0, sp.sqrt(m**2 - r**2))),
            (r, 0, m)
        ),
        (phi, 0, 2 * sp.pi)
    )
    assert sp.simplify(J_cyl - target_sym) == 0, f"Cylindrical mismatch: {J_cyl} != {target_sym}"

    # Numerical 3D grid check for m = 2, 3
    for m_val in [2, 3]:
        n_pts = 80
        lin_xy = np.linspace(-m_val, m_val, n_pts)
        lin_z = np.linspace(0.0, m_val, n_pts // 2)
        dx = lin_xy[1] - lin_xy[0]
        dz = lin_z[1] - lin_z[0]
        X, Y, Z = np.meshgrid(lin_xy, lin_xy, lin_z, indexing='ij')
        R2 = X**2 + Y**2 + Z**2
        mask = R2 <= m_val**2
        integrand_vals = Z[mask] * R2[mask]
        num_val = np.sum(integrand_vals) * (dx * dx * dz)
        exact_val = float(target_sym.subs(m, m_val).evalf())
        rel_err = abs(num_val - exact_val) / exact_val
        assert rel_err < 2.5e-2, f"3D grid mismatch for m={m_val}: {num_val} vs {exact_val}"

    print(f"VERIFIED_OK: CALC-MULINT-02 | J(m) = {J_sym} | m=3 -> {target_sym.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_mulint_02()
