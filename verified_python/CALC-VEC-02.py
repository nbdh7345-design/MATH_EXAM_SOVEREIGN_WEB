import sympy as sp

def verify_calc_vec_02():
    x, y, z, t, m = sp.symbols('x y z t m', real=True)
    P = 2 * m * x * y + z**2
    Q = m * x**2 + 2 * y * z
    R = y**2 + 2 * x * z + 3 * m * z**2

    # 1. Verify curl(F) == (0, 0, 0)
    curl_x = sp.simplify(sp.diff(R, y) - sp.diff(Q, z))
    curl_y = sp.simplify(sp.diff(P, z) - sp.diff(R, x))
    curl_z = sp.simplify(sp.diff(Q, x) - sp.diff(P, y))
    assert (curl_x, curl_y, curl_z) == (0, 0, 0), "Curl is not zero!"

    # 2. Verify scalar potential U
    U = m * x**2 * y + x * z**2 + y**2 * z + m * z**3
    assert sp.simplify(sp.diff(U, x) - P) == 0
    assert sp.simplify(sp.diff(U, y) - Q) == 0
    assert sp.simplify(sp.diff(U, z) - R) == 0

    W_pot = sp.simplify(U.subs({x: 1, y: 2, z: 1}) - U.subs({x: 0, y: 0, z: 0}))

    # 3. Verify path independence along two distinct paths from A(0,0,0) to B(1,2,1)
    # Path 1: straight line r1(t) = (t, 2t, t), t in [0, 1]
    integrand_1 = P.subs({x: t, y: 2*t, z: t}) * 1 + Q.subs({x: t, y: 2*t, z: t}) * 2 + R.subs({x: t, y: 2*t, z: t}) * 1
    W_path1 = sp.integrate(integrand_1, (t, 0, 1))

    # Path 2: parabolic curve r2(t) = (t, 2*t**2, t**3), t in [0, 1]
    integrand_2 = (
        P.subs({x: t, y: 2*t**2, z: t**3}) * 1
        + Q.subs({x: t, y: 2*t**2, z: t**3}) * (4*t)
        + R.subs({x: t, y: 2*t**2, z: t**3}) * (3*t**2)
    )
    W_path2 = sp.integrate(integrand_2, (t, 0, 1))

    assert sp.simplify(W_pot - (3 * m + 5)) == 0
    assert sp.simplify(W_path1 - W_pot) == 0
    assert sp.simplify(W_path2 - W_pot) == 0

    for m_val in range(2, 10):
        assert int(W_pot.subs(m, m_val)) == 3 * m_val + 5

    print(f"VERIFIED_OK: CALC-VEC-02 | W(m) = {W_pot} | W(3) = {W_pot.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_vec_02()
