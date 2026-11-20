-- Lean 4 Core verification for CALC-DER-03: Quartic Biquadratic Extrema Invariant
def f_quartic (m x : Int) : Int := x^4 - 2 * (m^2) * (x^2) + (m^4)
def T_invariant (m : Int) : Int := f_quartic m 0 + (m^2) * ((-m)^2 + (m^2))

theorem calc_der_03_min_val : (List.range 10).all (fun k => let m := Int.ofNat (k + 1); f_quartic m m == 0) = true := by decide
theorem calc_der_03_m2 : T_invariant 2 = 48 := by decide
theorem calc_der_03_m3 : T_invariant 3 = 243 := by decide

#eval T_invariant 3
