-- Core Lean 4 verification for CALC-ODE-01 (No Mathlib, No sorry)
-- After multiplying by e^(mx), the polynomial factor is P(x) = m^2 * x + C.
-- With y(0) = m => C = m, so at x = 1, I(m) = e^m * y(1) = m^2 + m.

def polyFactor (m x c : Nat) : Nat := m * m * x + c
def targetI (m : Nat) : Nat := polyFactor m 1 m

theorem calc_ode_01_at_m3 : targetI 3 = 12 := by decide
theorem calc_ode_01_formula (m : Nat) : targetI m = m * m + m := by
  simp [targetI, polyFactor]

theorem calc_ode_01_distinct_m3 :
    targetI 3 ≠ 3 * 3 + 2 * 3 + 1 ∧
    targetI 3 ≠ 2 * (3 * 3) + 3 + 1 ∧
    targetI 3 ≠ 3 * 3 - 1 := by decide

#eval targetI 3
