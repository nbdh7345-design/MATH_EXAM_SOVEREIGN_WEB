-- Lean 4 Core verification for CALC-MUL-01 (No Mathlib, No sorry)
def f_val (m x y : Int) : Int :=
  x^3 + y^3 - 3 * m * x * y + m^3

def grad_x (m x y : Int) : Int :=
  3 * x^2 - 3 * m * y

def grad_y (m x y : Int) : Int :=
  3 * y^2 - 3 * m * x

def hessian_det (m x y : Int) : Int :=
  (6 * x) * (6 * y) - (-3 * m)^2

def target_P (m : Int) : Int :=
  hessian_det m m m + f_val m m m

theorem calc_mul_01_stationary_m3 : grad_x 3 3 3 = 0 ∧ grad_y 3 3 3 = 0 := by
  decide

theorem calc_mul_01_grid_check :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      grad_x m m m == 0 && grad_y m m m == 0 &&
      hessian_det m m m > 0 && target_P m == 27 * m^2) = true := by
  decide

#eval (List.range 8).map (fun k => let m := Int.ofNat (k + 2); (m, target_P m))
