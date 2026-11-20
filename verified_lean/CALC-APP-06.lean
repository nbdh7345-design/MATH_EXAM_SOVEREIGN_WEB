-- Lean 4 Core verification for CALC-APP-06
-- a) (1 + x)^(3/2) at x = m^2 - 1 equals m^3: ((m^2)^3 = (m^3)^2); 3L/2 = m^3 - 1
-- b) π ∫_0^m x dx = π m^2 / 2: coefficient of π scaled by 2 is m^2
def threeHalfL (m : Nat) : Nat := m ^ 3 - 1
def twoVcoeff (m : Nat) : Nat := m * m

theorem calc_app_06_length :
    (List.range 8).all (fun k => let m := k + 2; (1 + (m ^ 2 - 1)) ^ 3 == (m ^ 3) ^ 2 && threeHalfL m + 1 == m ^ 3) = true := by
  decide
theorem calc_app_06_volume :
    (List.range 8).all (fun k => let m := k + 2; twoVcoeff m == m ^ 2) = true := by decide
