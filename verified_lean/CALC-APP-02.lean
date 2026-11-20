-- Lean 4 Core verification for CALC-APP-02 (solid of revolution, disc method)
-- Scaled by 30: 30 * (m^5/3 - m^5/2 + m^5/5) = 10 m^5 - 15 m^5 + 6 m^5 = m^5
def vol30 (m : Int) : Int := 10 * m ^ 5 - 15 * m ^ 5 + 6 * m ^ 5
def options60 (m : Int) : List Int := [4 * m ^ 5, m ^ 5, 2 * m ^ 5, 3 * m ^ 5]

theorem calc_app_02_volume :
    (List.range 8).all (fun k => let m : Int := k + 2; vol30 m == m ^ 5) = true := by decide
theorem calc_app_02_expand :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 10).all (fun j => let x : Int := j;
        x ^ 2 * (m - x) ^ 2 == m ^ 2 * x ^ 2 - 2 * m * x ^ 3 + x ^ 4)) = true := by decide
theorem calc_app_02_distinct :
    (List.range 8).all (fun k => let m : Int := k + 2; (options60 m).Nodup) = true := by decide

#eval vol30 3
