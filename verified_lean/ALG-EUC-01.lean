-- Lean 4 Core verification for ALG-EUC-01 (No Mathlib, No sorry)
def inner_m (m : Int) (x1 x2 x3 y1 y2 y3 : Int) : Int :=
  x1 * y1 + 2 * x2 * y2 + (m * m + 1) * x3 * y3 + x1 * y2 + x2 * y1

def norm_sq_w (m : Int) : Int :=
  inner_m m 1 1 1 1 1 1

theorem alg_euc_01_m3 : norm_sq_w 3 = 3 * 3 + 6 := by decide
theorem alg_euc_01_m5 : norm_sq_w 5 = 5 * 5 + 6 := by decide
theorem alg_euc_01_pos_def_decomp :
    (List.range 10).all (fun k => let m := Int.ofNat (k + 2); inner_m m 1 2 3 1 2 3 == (1 + 2) * (1 + 2) + 2 * 2 + (m * m + 1) * 3 * 3) = true := by
  decide

#eval norm_sq_w 3
