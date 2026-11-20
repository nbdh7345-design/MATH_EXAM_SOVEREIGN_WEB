import sympy as sp
import numpy as np

def verify_calc_lag_03():
    x, y, lam = sp.symbols('x y lam', real=True)
    m = sp.Symbol('m', positive=True)

    f = x**2 + y**2 - 2 * m * x + 2 * m**2
    g = x**2 + y**2 - 4 * m**2

    # 1. Điểm dừng miền trong
    int_sols = sp.solve([sp.diff(f, x), sp.diff(f, y)], (x, y), dict=True)
    candidates = []
    for s in int_sols:
        if sp.simplify(g.subs(s)).subs(m, 3) < 0:
            candidates.append(sp.simplify(f.subs(s)))

    # 2. Điểm dừng Lagrange trên biên
    L = f - lam * g
    bd_sols = sp.solve([sp.diff(L, x), sp.diff(L, y), g], (x, y, lam), dict=True)
    for s in bd_sols:
        candidates.append(sp.simplify(f.subs(s)))

    f_min_sym = min(candidates, key=lambda v: float(v.subs(m, 3)))
    f_max_sym = max(candidates, key=lambda v: float(v.subs(m, 3)))
    T_sym = sp.simplify(f_max_sym + f_min_sym)

    assert sp.simplify(f_min_sym - m**2) == 0, f"f_min mismatch: {f_min_sym}"
    assert sp.simplify(f_max_sym - 10 * m**2) == 0, f"f_max mismatch: {f_max_sym}"
    assert sp.simplify(T_sym - 11 * m**2) == 0, f"T(m) mismatch: {T_sym}"

    # 3. Kiểm chứng lưới tọa độ cực (r, theta) trên toàn miền compact D_m
    theta = np.linspace(0, 2 * np.pi, 1000)
    r_norm = np.linspace(0, 1.0, 500)
    R_grid, Th_grid = np.meshgrid(r_norm, theta)

    for m_val in range(2, 10):
        R = 2 * m_val * R_grid
        X = R * np.cos(Th_grid)
        Y = R * np.sin(Th_grid)
        F = X**2 + Y**2 - 2 * m_val * X + 2 * (m_val ** 2)
        assert abs(np.min(F) - (m_val ** 2)) < 1e-2, f"Grid min mismatch at m={m_val}"
        assert abs(np.max(F) - 10 * (m_val ** 2)) < 1e-2, f"Grid max mismatch at m={m_val}"

    print(f"VERIFIED_OK: CALC-LAG-03 | f_min={f_min_sym}, f_max={f_max_sym}, T(m)={T_sym} | T(3)={T_sym.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_lag_03()
