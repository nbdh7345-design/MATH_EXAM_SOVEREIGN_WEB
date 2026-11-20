-- Lean 4 Core verification for CALC-DER-02: Cubic Extrema Gap
def f_cubic (m x : Int) : Int := x^3 - 3 * m * (x^2) + 4 * (m^3)
def df_cubic (m x : Int) : Int := 3 * (x^2) - 6 * m * x
def delta_y (m : Int) : Int := f_cubic m 0 - f_cubic m (2 * m)

theorem calc_der_02_crit_0 : (List.range 10).all (fun k => df_cubic (Int.ofNat (k + 1)) 0 == 0) = true := by decide
theorem calc_der_02_m3 : delta_y 3 = 108 := by decide
theorem calc_der_02_m4 : delta_y 4 = 256 := by decide

#eval delta_y 3
