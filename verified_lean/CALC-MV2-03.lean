-- Lean 4 Core verification for CALC-MV2-03 (path-dependent limit & directional derivative)
-- Along y = kx the expression equals m k / (1 + k^2): k = 0 gives 0, k = 1 gives m/2 (scaled by 2: m)
def pathLimit2 (m k : Nat) : Nat := 2 * m * k / (1 + k ^ 2)
def gradX : Int := 2
def gradY (m : Int) : Int := 1 + 3 * m
def dirDeriv5 (m : Int) : Int := 3 * gradX + 4 * gradY m

theorem calc_mv2_03_paths :
    (List.range 8).all (fun k => let m := k + 2; pathLimit2 m 0 != pathLimit2 m 1) = true := by decide
theorem calc_mv2_03_direction :
    (List.range 8).all (fun k => let m : Int := k + 2; dirDeriv5 m == 12 * m + 10) = true := by decide
theorem calc_mv2_03_unit : 3 ^ 2 + 4 ^ 2 = 5 ^ 2 := by decide

#eval dirDeriv5 3
