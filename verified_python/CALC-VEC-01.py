import sympy as sp

def verify_calc_vec_01():
    x, y, t, m = sp.symbols('x y t m', real=True)
    P = x**2 * y - m * y
    Q = m * x + sp.Rational(1, 3) * x**3

    # 1. Double integral via Green's Theorem on D = [0, 2] x [0, 3]
    curl_z = sp.diff(Q, x) - sp.diff(P, y)
    I_green = sp.integrate(sp.integrate(curl_z, (y, 0, 3)), (x, 0, 2))

    # 2. Direct line integral over 4 boundary segments of D = [0, 2] x [0, 3]
    # C1: (t, 0), t in [0, 2]
    I1 = sp.integrate(P.subs({x: t, y: 0}), (t, 0, 2))
    # C2: (2, t), t in [0, 3]
    I2 = sp.integrate(Q.subs({x: 2, y: t}), (t, 0, 3))
    # C3: (t, 3), t from 2 to 0
    I3 = sp.integrate(P.subs({x: t, y: 3}), (t, 2, 0))
    # C4: (0, t), t from 3 to 0
    I4 = sp.integrate(Q.subs({x: 0, y: t}), (t, 3, 0))
    I_line = sp.simplify(I1 + I2 + I3 + I4)

    assert sp.simplify(I_green - 12 * m) == 0, f"Mismatch Green: {I_green}"
    assert sp.simplify(I_line - I_green) == 0, f"Mismatch Line vs Green: {I_line} != {I_green}"

    for m_val in range(2, 10):
        val_green = int(I_green.subs(m, m_val))
        val_line = int(I_line.subs(m, m_val))
        assert val_green == 12 * m_val == val_line

    print(f"VERIFIED_OK: CALC-VEC-01 | I(m) = {I_green} | I(3) = {I_green.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_vec_01()
