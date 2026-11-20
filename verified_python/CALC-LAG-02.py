import sympy as sp
import numpy as np

def verify_calc_lag_02():
    x, y, z, lam = sp.symbols('x y z lam', real=True)
    m = sp.Symbol('m', positive=True)

    f = x**2 + y**2 + z**2
    g = x + 2 * y + 2 * z - 9 * m
    L = f - lam * g

    sol = sp.solve([sp.diff(L, x), sp.diff(L, y), sp.diff(L, z), g], (x, y, z, lam), dict=True)[0]
    f_min_sym = sp.simplify(f.subs(sol))
    lam_sym = sp.simplify(sol[lam])
    P_sym = sp.simplify(f_min_sym + lam_sym)

    expected = 9 * m**2 + 2 * m
    assert sp.simplify(P_sym - expected) == 0, f"SymPy mismatch: {P_sym} != {expected}"

    # Kiểm chứng số học trên siêu phẳng x = 9m - 2y - 2z cho m = 2..9
    for m_val in range(2, 10):
        ys = np.linspace(2 * m_val - 3, 2 * m_val + 3, 401)
        zs = np.linspace(2 * m_val - 3, 2 * m_val + 3, 401)
        Y, Z = np.meshgrid(ys, zs)
        X = 9 * m_val - 2 * Y - 2 * Z
        F_val = np.min(X**2 + Y**2 + Z**2)
        assert abs(F_val - 9 * (m_val ** 2)) < 1e-8, f"NumPy mismatch at m={m_val}"

    print(f"VERIFIED_OK: CALC-LAG-02 | P(m) = {P_sym} | P(3) = {expected.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_lag_02()
