-- Core Lean 4 verification for CALC-ODE-02 (No Mathlib, No sorry)
-- Characteristic polynomial: r^2 - 3*m*r + 2*m^2 = (r - m)*(r - 2*m)
-- Evaluated at e^(m*x0) = 2: S(m) = C1 * 2 + C2 * 4 where C1 = m, C2 = 1.

def charPoly (m r : Int) : Int := r * r - 3 * m * r + 2 * m * m
def targetS (m : Nat) : Nat := m * 2 + 1 * 4

theorem calc_ode_02_roots_m3 : charPoly 3 3 = 0 ∧ charPoly 3 6 = 0 := by decide
theorem calc_ode_02_at_m3 : targetS 3 = 10 := by decide
theorem calc_ode_02_formula (m : Nat) : targetS m = 2 * m + 4 := by unfold targetS; omega

#eval targetS 3
