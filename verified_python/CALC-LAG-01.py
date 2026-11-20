import sympy as sp
import numpy as np

def verify_calc_lag_01():
    x, y, lam = sp.symbols('x y lam', real=True)
    m = sp.Symbol('m', positive=True)

    f = 3 * m * x + 4 * m * y
    g = x**2 + y**2 - m**2
    L = f - lam * g

    eqs = [sp.diff(L, x), sp.diff(L, y), g]
    sols = sp.solve(eqs, (x, y, lam), dict=True)
    vals = [sp.simplify(f.subs(s)) for s in sols]
    sym_max = sp.simplify(max(vals, key=lambda v: float(v.subs(m, 3))))

    expected = 5 * m**2
    assert sp.simplify(sym_max - expected) == 0, f"SymPy mismatch: {sym_max} != {expected}"

    # Kiểm chứng số học trên lưới góc lượng giác cho mọi m từ 2 đến 9
    theta = np.linspace(0, 2 * np.pi, 20000)
    for m_val in range(2, 10):
        xs = m_val * np.cos(theta)
        ys = m_val * np.sin(theta)
        f_num = np.max(3 * m_val * xs + 4 * m_val * ys)
        f_exact = 5 * (m_val ** 2)
        assert abs(f_num - f_exact) < 1e-4, f"NumPy mismatch at m={m_val}: {f_num} vs {f_exact}"

    print(f"VERIFIED_OK: CALC-LAG-01 | M(m) = {sym_max} | M(3) = {expected.subs(m, 3)}")

if __name__ == "__main__":
    verify_calc_lag_01()
