-- Lean 4 Core Verification for CALC-LAG-02 (No Mathlib, No sorry)
def f_min_02 (m : Nat) : Nat := 9 * m * m
def lambda_star_02 (m : Nat) : Nat := 2 * m
def P_02 (m : Nat) : Nat := f_min_02 m + lambda_star_02 m

theorem calc_lag_02_constraint (m : Nat) :
    let x := m
    let y := 2 * m
    let z := 2 * m
    x + 2 * y + 2 * z = 9 * m := by omega

theorem calc_lag_02_m3 : P_02 3 = 87 := by decide
theorem calc_lag_02_m4 : P_02 4 = 152 := by decide

#eval P_02 3
#eval P_02 5
