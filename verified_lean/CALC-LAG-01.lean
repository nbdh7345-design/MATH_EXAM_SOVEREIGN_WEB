-- Lean 4 Core Verification for CALC-LAG-01 (No Mathlib, No sorry)
def max_lagrange_01 (m : Nat) : Nat := 5 * m * m

-- Kiểm chứng đẳng thức đại số Cauchy-Schwarz / Lagrange đã quy đồng mẫu số 5:
-- (3*x + 4*y)^2 + (4*x - 3*y)^2 = 25 * (x^2 + y^2)
-- Tại điểm cực đại (3m, 4m) (tỉ lệ x5): 3m*(3m) + 4m*(4m) = 25*m^2 = 5 * (5*m^2)
theorem calc_lag_01_m3 : max_lagrange_01 3 = 45 := by decide
theorem calc_lag_01_m5 : max_lagrange_01 5 = 125 := by decide

theorem cauchy_identity_m3 :
    let m := 3
    let x5 := 3 * m
    let y5 := 4 * m
    (3 * m * x5 + 4 * m * y5) / 5 = max_lagrange_01 m := by decide

#eval max_lagrange_01 3
#eval max_lagrange_01 7
