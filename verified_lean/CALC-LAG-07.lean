-- Lean 4 Core verification for CALC-LAG-07 (z = xy on x^2 + y^2 = 2 m^2)
def onCircle (m x y : Int) : Bool := x ^ 2 + y ^ 2 == 2 * m ^ 2

theorem calc_lag_07_points :
    (List.range 8).all (fun k => let m : Int := k + 2;
      onCircle m m m && onCircle m (-m) (-m) && onCircle m m (-m) && onCircle m (-m) m
        && m * m - m * (-m) == 2 * m ^ 2) = true := by decide
-- 2|xy| ≤ x^2 + y^2 = 2 m^2 on integer points of the circle
theorem calc_lag_07_bound :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 31).all (fun a => (List.range 31).all (fun b =>
        let x : Int := a - 15; let y : Int := b - 15;
        !(onCircle m x y) || (x * y ≤ m ^ 2 && x * y ≥ -m ^ 2)))) = true := by decide
