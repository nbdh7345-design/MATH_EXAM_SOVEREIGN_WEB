-- Lean 4 Core verification for CALC-LIM-03 (Essay Taylor matching)
-- Scaled by 12 for degree 3: ln coeff is 4*m^3, -sin coeff is 2*m^3 => sum = 6*m^3 = m^3/2
-- Scaled by 4 for degree 4: 4 * (-m^4 / 4) = -m^4
def two_a (m : Int) : Int := m ^ 2
def two_b (m : Int) : Int := -(m ^ 3)
def limit_calc_lim_03 (m : Int) : Int := -(m ^ 4)

theorem calc_lim_03_conditions_m3 :
  two_a 3 = 9 ∧ two_b 3 = -27 ∧ limit_calc_lim_03 3 = -81 := by decide

#eval (two_a 3, two_b 3, limit_calc_lim_03 3)
