-- Lean 4 Core verification for CALC-LIM-01 (Taylor coefficient arithmetic)
-- Numerator x^3 coefficient scaled by 6: 6 * (m^3 / 6 - (-m^3 / 6)) = 2 * m^3
def exp_coeff3_scaled6 (m : Int) : Int := m ^ 3
def sin_coeff3_scaled6 (m : Int) : Int := -(m ^ 3)
def limit_calc_lim_01 (m : Int) : Int := exp_coeff3_scaled6 m - sin_coeff3_scaled6 m

theorem calc_lim_01_at_m3 : limit_calc_lim_01 3 = 54 := by decide
theorem calc_lim_01_at_m5 : limit_calc_lim_01 5 = 250 := by decide
theorem calc_lim_01_distinct_m2 : limit_calc_lim_01 2 != 2^3 ∧ limit_calc_lim_01 2 != 3*(2^3) := by decide

#eval limit_calc_lim_01 3
