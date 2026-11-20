import sympy as sp
import numpy as np

def verify_alg_rnk_02():
    lam = sp.Symbol('lam')
    for m_val in range(2, 10):
        A_lam = sp.Matrix([
            [1, 1, 1],
            [1, lam, 1],
            [1, 1, lam**2 - m_val * lam + 1]
        ])
        roots = sp.solve(sp.det(A_lam), lam)
        rank2_vals = []
        for r in roots:
            A_sub = A_lam.subs(lam, r)
            rk_sym = A_sub.rank()
            rk_np = np.linalg.matrix_rank(np.array(A_sub.tolist(), dtype=float))
            assert rk_sym == rk_np == 2, f'Mismatch at m={m_val}, r={r}'
            rank2_vals.append(int(r))
        assert sorted(rank2_vals) == [0, 1, m_val]
        assert sum(x**2 for x in rank2_vals) == m_val**2 + 1
    print('VERIFIED_OK: ALG-RNK-02 passed across m in [2..9]')

if __name__ == '__main__':
    verify_alg_rnk_02()
