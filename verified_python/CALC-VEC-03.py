import sympy as sp

def verify_calc_vec_03():
    x, y, z, t, m = sp.symbols('x y z t m', real=True)

    # Part (a): Gauss - Ostrogradsky Flux vs 6 Surface Integrals
    F1 = m * x + y**2
    F2 = 2 * m * y + z**2
    F3 = 3 * m * z + x**2
    div_F = sp.diff(F1, x) + sp.diff(F2, y) + sp.diff(F3, z)
    flux_gauss = sp.integrate(sp.integrate(sp.integrate(div_F, (z, 0, 1)), (y, 0, 1)), (x, 0, 2))

    # Direct surface flux across 6 faces of [0, 2] x [0, 1] x [0, 1]
    flux_x2 = sp.integrate(sp.integrate(F1.subs(x, 2), (z, 0, 1)), (y, 0, 1))
    flux_x0 = sp.integrate(sp.integrate(-F1.subs(x, 0), (z, 0, 1)), (y, 0, 1))
    flux_y1 = sp.integrate(sp.integrate(F2.subs(y, 1), (z, 0, 1)), (x, 0, 2))
    flux_y0 = sp.integrate(sp.integrate(-F2.subs(y, 0), (z, 0, 1)), (x, 0, 2))
    flux_z1 = sp.integrate(sp.integrate(F3.subs(z, 1), (y, 0, 1)), (x, 0, 2))
    flux_z0 = sp.integrate(sp.integrate(-F3.subs(z, 0), (y, 0, 1)), (x, 0, 2))
    flux_faces = sp.simplify(flux_x2 + flux_x0 + flux_y1 + flux_y0 + flux_z1 + flux_z0)

    assert sp.simplify(flux_gauss - 12 * m) == 0
    assert sp.simplify(flux_faces - flux_gauss) == 0

    # Part (b): Stokes Circulation vs 4 Boundary Line Integrals on z = 1
    G1 = -m * y + z
    G2 = 2 * m * x + z**2
    G3 = x + y
    curl_G_z = sp.diff(G2, x) - sp.diff(G1, y)
    circ_stokes = sp.integrate(sp.integrate(curl_G_z.subs(z, 1), (y, 0, 1)), (x, 0, 2))

    # Direct line integral around [0, 2] x [0, 1] at z = 1
    c1 = sp.integrate(G1.subs({x: t, y: 0, z: 1}), (t, 0, 2))
    c2 = sp.integrate(G2.subs({x: 2, y: t, z: 1}), (t, 0, 1))
    c3 = sp.integrate(G1.subs({x: t, y: 1, z: 1}), (t, 2, 0))
    c4 = sp.integrate(G2.subs({x: 0, y: t, z: 1}), (t, 1, 0))
    circ_line = sp.simplify(c1 + c2 + c3 + c4)

    assert sp.simplify(circ_stokes - 6 * m) == 0
    assert sp.simplify(circ_line - circ_stokes) == 0

    total_T = sp.simplify(flux_gauss + circ_stokes)
    assert sp.simplify(total_T - 18 * m) == 0

    for m_val in range(2, 10):
        assert int(total_T.subs(m, m_val)) == 18 * m_val

    print(f"VERIFIED_OK: CALC-VEC-03 | Phi(m)={flux_gauss}, C(m)={circ_stokes}, T(m)={total_T} | T(3)={total_T.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_vec_03()
