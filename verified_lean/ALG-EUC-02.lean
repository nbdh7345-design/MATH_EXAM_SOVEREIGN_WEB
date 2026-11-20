-- Lean 4 Core verification for ALG-EUC-02 (No Mathlib, No sorry)
def dot3 (x1 x2 x3 y1 y2 y3 : Int) : Int :=
  x1 * y1 + x2 * y2 + x3 * y3

def e2_vec (m : Int) : Int × Int × Int :=
  (2 * m - m * 1, 0 - m * 1, m - m * 0)

def e2_norm_sq (m : Int) : Int :=
  let (a, b, c) := e2_vec m
  dot3 a b c a b c

theorem alg_euc_02_orthogonal :
    (List.range 10).all (fun k => let m := Int.ofNat (k + 2); let (a, b, c) := e2_vec m; dot3 a b c 1 1 0 == 0) = true := by
  decide

theorem alg_euc_02_m3 : e2_norm_sq 3 = 3 * 3 * 3 := by decide
theorem alg_euc_02_m7 : e2_norm_sq 7 = 3 * 7 * 7 := by decide

#eval e2_norm_sq 3
