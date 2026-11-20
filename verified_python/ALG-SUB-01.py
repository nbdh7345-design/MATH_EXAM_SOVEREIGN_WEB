import sympy as sp
import numpy as np

def verify_alg_sub_01():
    for m_val in range(2, 10):
        u1 = [1, 0, m_val, 1]
        u2 = [0, 1, 1, m_val]
        u3 = [1, 1, m_val + 1, m_val + 1]
        M_U = sp.Matrix([u1, u2, u3])
        rref_U, pivots_U = M_U.rref()
        dim_U = len(pivots_U)
        assert dim_U == 2

        A_W = sp.Matrix([[m_val, 1, -1, 0]])
        null_W = A_W.nullspace()
        dim_W = len(null_W)
        assert dim_W == 3

        basis_W = [list(v) for v in null_W]
        M_sum = sp.Matrix([u1, u2] + basis_W)
        _, pivots_sum = M_sum.rref()
        dim_sum = len(pivots_sum)
        dim_inter = dim_U + dim_W - dim_sum

        np_rank_sum = np.linalg.matrix_rank(np.array([u1, u2] + basis_W, dtype=float))
        assert dim_sum == int(np_rank_sum) == 3
        assert dim_inter == 2
        val = m_val * dim_sum + dim_inter
        assert val == 3 * m_val + 2
    print('VERIFIED_OK: ALG-SUB-01 Grassmann dimensions verified across m=2..9')

if __name__ == '__main__':
    verify_alg_sub_01()
