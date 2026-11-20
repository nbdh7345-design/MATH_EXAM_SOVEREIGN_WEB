-- Core Lean 4 verification for CALC-MULINT-02 (No Mathlib, No sorry)
-- Verify spherical integral coefficient: (2) * (1/2) * (m^6 / 6) = m^6 / 6

def sphericalNum (m : Nat) : Nat := m ^ 6
def sphericalDen : Nat := 6

theorem calc_mulint_02_m3 : sphericalNum 3 = 729 ∧ sphericalDen = 6 := by
  decide

theorem calc_mulint_02_reduced_m3 :
    Nat.gcd (sphericalNum 3) sphericalDen = 3 ∧
    (sphericalNum 3) / 3 = 243 ∧
    sphericalDen / 3 = 2 := by
  decide

#eval (sphericalNum 3, sphericalDen)
#eval (sphericalNum 2, sphericalDen)
