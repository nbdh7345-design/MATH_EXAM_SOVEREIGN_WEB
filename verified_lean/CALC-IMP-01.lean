-- Core Lean 4 verification for CALC-IMP-01 (no Mathlib, no sorry)
def I1 (m : Nat) : Nat := 2 * m
def I2 (_m : Nat) : Nat := 2
def I_total (m : Nat) : Nat := I1 m + I2 m

theorem calc_imp_01_default : I_total 3 = 8 := by decide
theorem calc_imp_01_formula (m : Nat) : I_total m = 2 * m + 2 := by rfl
theorem calc_imp_01_pos (m : Nat) (h : m >= 2) : I_total m >= 6 := by
  unfold I_total I1 I2
  omega

#eval (List.range 8).map (fun k => let m := k + 2; (m, I_total m))
