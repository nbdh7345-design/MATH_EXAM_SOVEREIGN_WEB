-- Lean 4 Core Verification for CALC-LAG-03 (No Mathlib, No sorry)
def f_max_03 (m : Nat) : Nat := 10 * m * m
def f_min_03 (m : Nat) : Nat := m * m
def T_03 (m : Nat) : Nat := f_max_03 m + f_min_03 m

theorem calc_lag_03_formula : (List.range 10).all (fun k => let m := k + 1; T_03 m == 11 * m * m) = true := by
  decide

theorem calc_lag_03_m3 : T_03 3 = 99 := by decide
theorem calc_lag_03_m5 : T_03 5 = 275 := by decide

#eval T_03 3
#eval T_03 6
