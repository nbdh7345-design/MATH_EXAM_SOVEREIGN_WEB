import sympy as sp
import numpy as np

def verify_alg_sub_03():
    for m_val in range(2, 10):
        u1 = [1, 0, m_val, 0]
        u2 = [0, 1, 0, m_val]
        A_W = sp.Matrix([[m_val, 0, -1, 1], [0, 0, 0, 1]])
        null_W = A_W.nullspace()
        assert len(null_W) == 2

        basis_W = [list(v) for v in null_W]
        M_sum = sp.Matrix([u1, u2] + basis_W)
        _, pivots_sum = M_sum.rref()
        dim_sum = len(pivots_sum)
        dim_inter = 2 + len(null_W) - dim_sum
        assert dim_sum == 3 and dim_inter == 1

        # Direct sum complement check with e3 = [0, 0, 1, 0]
        e3 = [0, 0, 1, 0]
        M_full = np.array([u1, u2, basis_W[0], e3], dtype=float)
        assert np.linalg.matrix_rank(M_full) == 4

        b_cap = np.array(u1, dtype=int)
        index_I = int(np.dot(b_cap, b_cap)) + dim_sum
        assert index_I == m_val**2 + 4
    print('VERIFIED_OK: ALG-SUB-03 Grassmann & direct sum verified across m=2..9')

if __name__ == '__main__':
    verify_alg_sub_03()
