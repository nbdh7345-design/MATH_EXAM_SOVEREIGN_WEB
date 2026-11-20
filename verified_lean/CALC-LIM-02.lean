-- Lean 4 Core verification for CALC-LIM-02 (4th-order Taylor cancellation)
-- Scaled by 24: 12 * (3 * m^4 / 24 - 1 * m^4 / 24) = m^4
def gauss_coeff4_scaled24 (m : Int) : Int := 3 * (m ^ 4)
def cos_coeff4_scaled24 (m : Int) : Int := 1 * (m ^ 4)
def limit_calc_lim_02 (m : Int) : Int :=
  (12 * (gauss_coeff4_scaled24 m - cos_coeff4_scaled24 m)) / 24

theorem calc_lim_02_at_m3 : limit_calc_lim_02 3 = 81 := by decide
theorem calc_lim_02_at_m4 : limit_calc_lim_02 4 = 256 := by decide

#eval limit_calc_lim_02 3
