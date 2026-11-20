-- Lean 4 Core verification for CALC-MVT-03 (Rolle point & inflection point)
def f (m x : Int) : Int := x ^ 3 - 3 * m * x ^ 2 + 2
def df (m x : Int) : Int := 3 * x ^ 2 - 6 * m * x
def d2f (m x : Int) : Int := 6 * x - 6 * m

theorem calc_mvt_03_rolle :
    (List.range 8).all (fun k => let m : Int := k + 2;
      f m 0 == f m (3 * m) && df m (2 * m) == 0 && 0 < 2 * m && 2 * m < 3 * m) = true := by decide
theorem calc_mvt_03_inflection :
    (List.range 8).all (fun k => let m : Int := k + 2;
      d2f m m == 0 && d2f m (m - 1) < 0 && d2f m (m + 1) > 0 && f m m == 2 - 2 * m ^ 3) = true := by
  decide

#eval (f 3 (2 * 3), f 3 3)
