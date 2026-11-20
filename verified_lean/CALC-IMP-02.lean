-- Core Lean 4 verification for CALC-IMP-02 (no Mathlib, no sorry)
def p_max (m : Nat) : Nat := m - 1
def J_val (m : Nat) : Nat := m * (m + 1)
def S_val (m : Nat) : Nat := J_val m + p_max m

theorem calc_imp_02_default : S_val 3 = 14 := by decide
theorem calc_imp_02_grid_check :
  (List.range 8).map (fun k => let m := k + 2; S_val m == m * m + 2 * m - 1) =
  [true, true, true, true, true, true, true, true] := by decide
theorem calc_imp_02_bound (m : Nat) (h : m >= 2) : p_max m + 1 = m := by
  unfold p_max
  omega

#eval (List.range 8).map (fun k => let m := k + 2; (m, J_val m, p_max m, S_val m))
