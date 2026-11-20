-- Core Lean 4 verification for CALC-IMP-03 (no Mathlib, no sorry)
def N_conv (m : Nat) : Nat := 2 * m - 1
def L_euler (m : Nat) : Nat := 6 * m^4 + m^3
def T_total (m : Nat) : Nat := L_euler m + N_conv m

theorem calc_imp_03_default : T_total 3 = 518 := by decide
theorem calc_imp_03_euler_default : L_euler 3 = 513 := by decide
theorem calc_imp_03_count (m : Nat) (h : m >= 2) : N_conv m + 1 = 2 * m := by
  unfold N_conv
  omega

#eval (List.range 8).map (fun k => let m := k + 2; (m, N_conv m, L_euler m, T_total m))
