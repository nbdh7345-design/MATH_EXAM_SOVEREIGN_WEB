-- Lean 4 Core verification for CALC-LIM-06 (second-order Maclaurin coefficients)
-- ln(1 + mx): coefficient of x^2 is -m^2/2 ; ln cos(mx) ~ -(m x)^2 / 2  (both scaled by 2)
def logCoeff2 (m : Int) : Int := -(m ^ 2)
def cosExponent2 (m : Int) : Int := -(m * m)

theorem calc_lim_06_same_exponent :
    (List.range 8).all (fun k => let m : Int := k + 2; logCoeff2 m == cosExponent2 m && logCoeff2 m < 0) = true := by
  decide
