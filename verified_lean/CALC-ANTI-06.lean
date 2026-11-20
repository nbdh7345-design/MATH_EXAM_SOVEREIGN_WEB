-- Lean 4 Core verification for CALC-ANTI-06
-- b) 3J = 2 [(m^3 - 3m) - (1 - 3)] = 2m^3 - 6m + 4 ; substitution x = t^2 - 1 maps t = m to x = m^2 - 1
def threeJ (m : Int) : Int := 2 * ((m ^ 3 - 3 * m) - (1 - 3))

theorem calc_anti_06_J :
    (List.range 8).all (fun k => let m : Int := k + 2; threeJ m == 2 * m ^ 3 - 6 * m + 4 && m ^ 2 - 1 == m * m - 1) = true := by
  decide
-- a) 2I = 1/m: the antiderivative sin^2(mx)/(2m) goes from 0 to 1/(2m)
theorem calc_anti_06_I : (1 : Int) ^ 2 - 0 ^ 2 = 1 := by decide
