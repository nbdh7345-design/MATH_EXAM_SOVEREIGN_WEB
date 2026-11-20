-- Lean 4 Core verification for CALC-MUL-05 (second derivative test)
def f (m x y : Int) : Int := x ^ 3 + y ^ 3 - 3 * m * x * y
def fx (m x y : Int) : Int := 3 * x ^ 2 - 3 * m * y
def fy (m x y : Int) : Int := 3 * y ^ 2 - 3 * m * x
def hessDet (m x y : Int) : Int := (6 * x) * (6 * y) - (3 * m) ^ 2

theorem calc_mul_05_critical :
    (List.range 8).all (fun k => let m : Int := k + 2;
      fx m 0 0 == 0 && fy m 0 0 == 0 && fx m m m == 0 && fy m m m == 0) = true := by decide
theorem calc_mul_05_classify :
    (List.range 8).all (fun k => let m : Int := k + 2;
      hessDet m 0 0 < 0 && hessDet m m m == 27 * m ^ 2 && 6 * m > 0 && f m m m == -m ^ 3) = true := by decide
