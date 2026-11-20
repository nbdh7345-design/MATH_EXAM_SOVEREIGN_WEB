-- Lean 4 Core verification for CALC-APP-01 (area between y = x^2 and y = m x)
-- Scaled by 6: 6 * (m^3/2 - m^3/3) = 3 m^3 - 2 m^3 = m^3
def area6 (m : Int) : Int := 3 * m ^ 3 - 2 * m ^ 3
def options6 (m : Int) : List Int := [m ^ 3, 2 * m ^ 3, 3 * m ^ 3, m ^ 2]

theorem calc_app_01_area :
    (List.range 8).all (fun k => let m : Int := k + 2; area6 m == m ^ 3) = true := by decide
theorem calc_app_01_upper_line :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range (k + 3)).all (fun j => let x : Int := j; !(decide (x ≤ m)) || decide (m * x - x ^ 2 ≥ 0))) = true := by
  decide
theorem calc_app_01_distinct :
    (List.range 8).all (fun k => let m : Int := k + 2; (options6 m).Nodup) = true := by decide

#eval area6 3
