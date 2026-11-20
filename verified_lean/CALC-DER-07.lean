-- Lean 4 Core verification for CALC-DER-07 (extrema of x^3 - 3 m^2 x on [0, 2m])
def f (m x : Int) : Int := x ^ 3 - 3 * m ^ 2 * x
def df (m x : Int) : Int := 3 * x ^ 2 - 3 * m ^ 2

theorem calc_der_07_values :
    (List.range 8).all (fun k => let m : Int := k + 2;
      df m m == 0 && f m 0 == 0 && f m m == -2 * m ^ 3 && f m (2 * m) == 2 * m ^ 3
        && f m (2 * m) - f m m == 4 * m ^ 3) = true := by decide
theorem calc_der_07_grid_bounds :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range (2 * k + 5)).all (fun j => let x : Int := j;
        f m m ≤ f m x && f m x ≤ f m (2 * m))) = true := by decide
