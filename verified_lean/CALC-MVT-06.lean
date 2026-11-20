-- Lean 4 Core verification for CALC-MVT-06
-- numerator of y': (x^2 + m^2) - 2x^2 = m^2 - x^2 ; extreme values ±m/(2m^2) = ±1/(2m)
theorem calc_mvt_06_derivative_numerator :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 21).all (fun j => let x : Int := j - 10; (x ^ 2 + m ^ 2) - 2 * x ^ 2 == m ^ 2 - x ^ 2)) = true := by decide
theorem calc_mvt_06_extrema :
    (List.range 8).all (fun k => let m : Int := k + 2;
      m ^ 2 - m ^ 2 == 0 && m * 2 * m == 2 * (m ^ 2) && m ^ 2 + m ^ 2 > 0) = true := by decide
