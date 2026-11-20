-- Lean 4 Core verification for CALC-MUL-03 (No Mathlib, No sorry)
def f3_val (m x y z : Int) : Int :=
  x^2 + 2*y^2 + 2*z^2 + 2*x*y + 2*x*z + 2*y*z - 2*m*x - 6*m*y + 7*m^2

def f3_sos (m x y z : Int) : Int :=
  (x + y + z - m)^2 + (y - 2*m)^2 + (z + m)^2 + m^2

def D1 : Int := 2
def D2 : Int := 2 * 4 - 2 * 2
def D3 : Int := 2 * (4 * 4 - 2 * 2) - 2 * (2 * 4 - 2 * 2) + 2 * (2 * 2 - 4 * 2)

theorem sylvester_positive_definite : D1 = 2 ∧ D2 = 4 ∧ D3 = 8 ∧ D1 > 0 ∧ D2 > 0 ∧ D3 > 0 := by
  decide

theorem calc_mul_03_grid_check :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      let x0 : Int := 0
      let y0 : Int := 2 * m
      let z0 : Int := -m
      f3_val m x0 y0 z0 == m^2 &&
      f3_sos m x0 y0 z0 == m^2 &&
      (f3_val m x0 y0 z0 + D1 + D2 + D3) == m^2 + 14) = true := by
  decide

#eval (List.range 8).map (fun k => let m := Int.ofNat (k + 2); (m, f3_val m 0 (2*m) (-m) + D1 + D2 + D3))
