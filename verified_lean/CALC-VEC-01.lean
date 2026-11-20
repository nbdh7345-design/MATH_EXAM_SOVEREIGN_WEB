-- Lean 4 Core Verification for CALC-VEC-01 (Green's Theorem on D = [0,2]x[0,3])
def greenCurlDensity (m : Nat) : Nat := 2 * m
def rectArea : Nat := 2 * 3
def lineIntegralGreen (m : Nat) : Nat := greenCurlDensity m * rectArea

theorem calc_vec_01_formula (m : Nat) : lineIntegralGreen m = 12 * m := by
  unfold lineIntegralGreen greenCurlDensity rectArea
  omega

theorem calc_vec_01_m3 : lineIntegralGreen 3 = 36 := by
  decide

theorem calc_vec_01_grid :
    (List.range 8).all (fun k =>
      let m := k + 2
      lineIntegralGreen m == 12 * m) = true := by
  decide

#eval lineIntegralGreen 3
