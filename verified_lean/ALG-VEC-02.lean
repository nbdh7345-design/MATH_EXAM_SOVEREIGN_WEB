-- Lean 4 Core verification for ALG-VEC-02 (Basis & Coordinates in R^3)
def detPm (m : Int) : Int :=
  1 * (1 * (m + 2) - 1 * m) - 1 * (0 * (m + 2) - 1 * 1) + 2 * (0 * m - 1 * 1)

def coordReconstruct (m x1 x2 x3 : Int) : Int × Int × Int :=
  (x1 + x2 + 2 * x3, x2 + x3, x1 + m * x2 + (m + 2) * x3)

theorem alg_vec_02_det_m3 : detPm 3 = 1 := by decide
theorem alg_vec_02_coords_m3 :
    coordReconstruct 3 3 2 4 = (3 * 3 + 4, 3 + 3, 3 * 3 + 6 * 3 + 2) := by decide
theorem alg_vec_02_sum (m : Int) : m + 2 + (m + 1) = 2 * m + 3 := by omega

#eval (detPm 3, coordReconstruct 3 3 2 4, 2 * 3 + 3)
