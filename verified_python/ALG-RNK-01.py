import sympy as sp
import numpy as np

def verify_alg_rnk_01():
    k, m = sp.symbols('k m')
    for m_val in range(2, 10):
        k_crit = 2 * m_val
        A_sym_crit = sp.Matrix([
            [1, 2, -1, m_val],
            [2, 5, 1, 2 * m_val + 1],
            [3, 7, k_crit - 2 * m_val, 3 * m_val + 1]
        ])
        A_sym_noncrit = sp.Matrix([
            [1, 2, -1, m_val],
            [2, 5, 1, 2 * m_val + 1],
            [3, 7, (k_crit + 1) - 2 * m_val, 3 * m_val + 1]
        ])
        assert A_sym_crit.rank() == 2, f'SymPy rank failed at m={m_val}'
        assert A_sym_noncrit.rank() == 3, f'SymPy noncrit rank failed at m={m_val}'
        A_np_crit = np.array(A_sym_crit.tolist(), dtype=float)
        A_np_noncrit = np.array(A_sym_noncrit.tolist(), dtype=float)
        assert np.linalg.matrix_rank(A_np_crit) == 2
        assert np.linalg.matrix_rank(A_np_noncrit) == 3
    print('VERIFIED_OK: ALG-RNK-01 passed across m in [2..9]')

if __name__ == '__main__':
    verify_alg_rnk_01()
