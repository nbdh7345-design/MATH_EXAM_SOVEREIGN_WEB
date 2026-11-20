-- Lean 4 Core verification for CALC-LAG-05 (min of x^2 + y^2 on x + y = 2m)
-- Identity: x^2 + (2m - x)^2 = 2 (x - m)^2 + 2 m^2
theorem calc_lag_05_identity :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 41).all (fun j => let x : Int := j - 20;
        x ^ 2 + (2 * m - x) ^ 2 == 2 * (x - m) ^ 2 + 2 * m ^ 2)) = true := by decide
theorem calc_lag_05_distinct :
    (List.range 8).all (fun k => let m : Int := k + 2; [2 * m ^ 2, 8 * m ^ 2, 4 * m ^ 2, m ^ 2].Nodup) = true := by decide
