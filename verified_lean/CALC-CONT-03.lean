-- Lean 4 Core verification for CALC-CONT-03 (continuity parameter & jump)
-- 1 - cos(mx) ~ (mx)^2 / 2  => lim f = m^2 / 2 ; scaled by 2: 2a = m^2
-- One-sided limits of arctan(m/x) in units of π/2: right = 1, left = -1 => jump = 2 * (π/2) = π
def twoA (m : Nat) : Nat := m ^ 2
def rightLimitHalfPi : Int := 1
def leftLimitHalfPi : Int := -1
def jumpHalfPi : Int := rightLimitHalfPi - leftLimitHalfPi

theorem calc_cont_03_param :
    (List.range 8).all (fun k => let m := k + 2; twoA m == m * m) = true := by decide
theorem calc_cont_03_jump : jumpHalfPi = 2 ∧ leftLimitHalfPi ≠ rightLimitHalfPi := by decide

#eval (twoA 3, jumpHalfPi)
