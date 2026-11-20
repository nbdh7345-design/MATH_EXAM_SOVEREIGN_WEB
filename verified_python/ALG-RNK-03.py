import sympy as sp
import numpy as np

def verify_alg_rnk_03():
    lam = sp.Symbol('lam')
    for m_val in range(2, 10):
        A_lam = sp.Matrix([
            [1, 1, 1, 1],
            [1, lam - m_val + 1, 1, (lam - m_val) * (lam - m_val - 1) + 1],
            [1, 1, (lam - m_val) * (lam - 2 * m_val) + 1, (lam - m_val) * (lam - 2 * m_val) + 1]
        ])
        for test_lam, expected_rank in [(m_val, 1), (2 * m_val, 2), (m_val + 1, 3), (0, 3)]:
            A_sub = A_lam.subs(lam, test_lam)
            rk_sym = A_sub.rank()
            rk_np = np.linalg.matrix_rank(np.array(A_sub.tolist(), dtype=float))
            assert rk_sym == expected_rank, f'SymPy rank mismatch at m={m_val}, lam={test_lam}'
            assert rk_np == expected_rank, f'NumPy rank mismatch at m={m_val}, lam={test_lam}'
        lam1, lam2 = m_val, 2 * m_val
        assert lam1 + 2 * lam2 == 5 * m_val
    print('VERIFIED_OK: ALG-RNK-03 passed across m in [2..9]')

if __name__ == '__main__':
    verify_alg_rnk_03()
