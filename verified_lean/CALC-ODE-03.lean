-- Core Lean 4 verification for CALC-ODE-03 (No Mathlib, No sorry)
-- System at t0 = ln(2)/(2m) has e^(2m*t0) = 2, C1 = m, C2 = 2m.
-- x(t0) = C1 + 2*C2 = 5m, y(t0) = -C1 + 2*C2 = 3m, P(m) = 15*m^2.

def xAtT0 (m : Nat) : Nat := m + 2 * (2 * m)
def yAtT0 (m : Nat) : Nat := 2 * (2 * m) - m
def targetP (m : Nat) : Nat := xAtT0 m * yAtT0 m

theorem calc_ode_03_components (m : Nat) : xAtT0 m = 5 * m ∧ yAtT0 m = 3 * m := by
  unfold xAtT0 yAtT0; constructor <;> omega

theorem calc_ode_03_at_m3 : targetP 3 = 135 := by decide

#eval targetP 3
