-- Lean 4 Core verification for ALG-EUC-03 (No Mathlib, No sorry)
def dot4 (x1 x2 x3 x4 y1 y2 y3 y4 : Int) : Int :=
  x1 * y1 + x2 * y2 + x3 * y3 + x4 * y4

def dist_sq_W (m : Int) : Int :=
  let z1 := 3 * m - 2 * m
  let z2 := 4 * m - 4 * m
  let z3 := 0 - 0
  let z4 := m - 2 * m
  dot4 z1 z2 z3 z4 z1 z2 z3 z4

theorem alg_euc_03_z_orth_e1 (m : Int) :
    dot4 m 0 0 (-m) 1 1 1 1 = 0 := by
  unfold dot4; omega

theorem alg_euc_03_z_orth_e2 (m : Int) :
    dot4 m 0 0 (-m) 0 2 (-2) 0 = 0 := by
  unfold dot4; omega

theorem alg_euc_03_m3 : dist_sq_W 3 = 2 * 3 * 3 := by decide
theorem alg_euc_03_m6 : dist_sq_W 6 = 2 * 6 * 6 := by decide

#eval dist_sq_W 3
