-- Lean 4 Core verification for CALC-MUL-06 (linear approximation, values scaled by 100)
def fx11 (m : Int) : Int := 2 + m
def fy11 (m : Int) : Int := 1 + 2 * m
def approx100 (m : Int) : Int := 100 * (1 + m) + fx11 m * 2 + fy11 m * (-1)

theorem calc_mul_06_approx :
    (List.range 8).all (fun k => let m : Int := k + 2; approx100 m == 100 * m + 103) = true := by decide
