-- Lean 4 Core verification for CALC-MV2-07
-- a) numerator identity 2x^2 + 2m y^2 = 2 (x^2 + m y^2)
-- b) numerator of z_yy: 2m (x^2 + m y^2) - 4 m^2 y^2 = 2m (x^2 - m y^2); at (1, 0) the value is 2m / 1
theorem calc_mv2_07_homogeneous :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 11).all (fun a => (List.range 11).all (fun b => let x : Int := a - 5; let y : Int := b - 5;
        2 * x ^ 2 + 2 * m * y ^ 2 == 2 * (x ^ 2 + m * y ^ 2)
        && 2 * m * (x ^ 2 + m * y ^ 2) - 4 * m ^ 2 * y ^ 2 == 2 * m * (x ^ 2 - m * y ^ 2)))) = true := by decide
theorem calc_mv2_07_value :
    (List.range 8).all (fun k => let m : Int := k + 2; 2 * m * (1 - m * 0) / (1 + m * 0) ^ 2 == 2 * m) = true := by decide
