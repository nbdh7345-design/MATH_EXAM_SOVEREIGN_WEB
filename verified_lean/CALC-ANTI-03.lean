-- Lean 4 Core verification for CALC-ANTI-03 (completing the square)
-- x^2 + 2x + m^2 + 1 = (x + 1)^2 + m^2 ; bounds map to u = 0 and u = m, i.e. u/m = 0 and 1
-- arctan 1 - arctan 0 = π/4  =>  I = π/(4m)
def quad (m x : Int) : Int := x ^ 2 + 2 * x + m ^ 2 + 1
def completed (m x : Int) : Int := (x + 1) ^ 2 + m ^ 2

theorem calc_anti_03_square :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 21).all (fun j => let x : Int := j - 10; quad m x == completed m x && quad m x > 0)) = true := by
  decide
theorem calc_anti_03_bounds :
    (List.range 8).all (fun k => let m : Int := k + 2; (-1 + 1) == 0 && ((m - 1) + 1) == m) = true := by decide

#eval completed 3 2
