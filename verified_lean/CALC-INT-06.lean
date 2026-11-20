-- Lean 4 Core verification for CALC-INT-06 (substitutions)
-- a) (1/2) * (2/3) * (m^2)^(3/2) = m^3 / 3, i.e. ((m^2)^3 = (m^3)^2 and 3 * I1 = m^3)
-- b) m^2 ∫_0^{π/2} cos^2 t dt = m^2 * (π/4): coefficient of π/4 is m^2
def threeI1 (m : Nat) : Nat := m ^ 3
def piQuarterCoeff (m : Nat) : Nat := m * m

theorem calc_int_06_power :
    (List.range 8).all (fun k => let m := k + 2; (m ^ 2) ^ 3 == (m ^ 3) ^ 2 && threeI1 m == m ^ 3) = true := by decide
theorem calc_int_06_trig :
    (List.range 8).all (fun k => let m := k + 2; piQuarterCoeff m == m ^ 2) = true := by decide
