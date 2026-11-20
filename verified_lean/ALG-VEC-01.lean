-- Lean 4 Core verification for ALG-VEC-01 (Linear Combination in R^3)
def u1 : Int × Int × Int := (1, 2, -1)
def u2 : Int × Int × Int := (2, 3, 1)

def linComb (a1 a2 : Int) : Int × Int × Int :=
  (a1 * 1 + a2 * 2, a1 * 2 + a2 * 3, a1 * (-1) + a2 * 1)

def targetVec (m : Int) : Int × Int × Int :=
  (4 * m + 3, 7 * m + 4, 3 - m)

theorem alg_vec_01_m3 : linComb (2 * 3 - 1) (3 + 2) = targetVec 3 := by decide
theorem alg_vec_01_sum_m3 : (2 * 3 - 1) + (3 + 2) = 3 * 3 + 1 := by omega
theorem alg_vec_01_sum_general (m : Int) : (2 * m - 1) + (m + 2) = 3 * m + 1 := by omega

#eval (linComb (2 * 3 - 1) (3 + 2), targetVec 3, 3 * 3 + 1)
