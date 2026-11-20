import sympy as sp
import numpy as np

def verify_alg_sub_02():
    m, k = sp.symbols('m k')
    for m_val in range(2, 10):
        v1 = [1, 2, m_val, 1]
        v2 = [2, 5, 2 * m_val + 1, 3]
        v3 = [3, 7, 3 * m_val + 1, 4]
        k_good = m_val**2 + 2
        w_good = [1, 3, m_val + 1, k_good - m_val**2]
        M_good = sp.Matrix([v1, v2, v3, w_good])
        _, pivots_good = M_good.rref()
        assert len(pivots_good) == 2

        # Nullspace of transpose confirms linear dependence
        ns = M_good.T.nullspace()
        assert len(ns) == 2

        # Distractor check
        w_bad = [1, 3, m_val + 1, (m_val**2 + 1) - m_val**2]
        np_rank_bad = np.linalg.matrix_rank(np.array([v1, v2, v3, w_bad], dtype=float))
        assert int(np_rank_bad) == 3
    print('VERIFIED_OK: ALG-SUB-02 span condition verified across m=2..9')

if __name__ == '__main__':
    verify_alg_sub_02()
