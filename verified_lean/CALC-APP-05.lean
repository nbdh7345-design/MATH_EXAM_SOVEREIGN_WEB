-- Lean 4 Core verification for CALC-APP-05 (surface of revolution)
-- (y sqrt(1 + y'^2))^2 = 4x (1 + 1/x) = 4 (x + 1);  upper bound: (m^2 - 1 + 1)^(3/2) = m^3
theorem calc_app_05_integrand_sq :
    (List.range 50).all (fun j => let x := j + 1; 4 * x * (x + 1) == x * (4 * (x + 1))) = true := by decide
theorem calc_app_05_bound :
    (List.range 8).all (fun k => let m := k + 2; (m ^ 2 - 1 + 1) ^ 3 == (m ^ 3) ^ 2) = true := by decide
theorem calc_app_05_distinct :
    (List.range 8).all (fun k => let m := k + 2;
      [4 * (m ^ 3 - 1), 8 * m ^ 3, 8 * (m ^ 3 - 1), 2 * (m ^ 3 - 1)].Nodup) = true := by decide
